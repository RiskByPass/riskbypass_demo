# -*- coding: utf-8 -*-
"""
Garena SSO prelogin full chain -- standard riskbypass usage:

  Step1  datadome-tags          -> initial datadome cookie + ua
  Step2  tls_forward            -> hit prelogin with tags cookie -> 403, get challenge url
  Step3  datadome-interstitial  -> (target=challenge url, init_cookies=tags cookie) -> trusted cookie
  Step4  tls_forward            -> hit prelogin with trusted cookie -> 200

Key points:
  - Business request MUST go through tls_forward so the fingerprint matches the solver.
  - The datadome-interstitial task takes the challenge url + init_cookies (cid is bound to the tags cookie).
  - Keep the same proxy exit IP across all steps (cid is bound to the IP).
"""
import requests_go as requests
import time
import json
import base64
from urllib.parse import urlencode

# ---------------------------------------------------------------------------
BASE_URL = "http://riskbypass.com"
TOKEN = "your token"                       # x-api-key
TIMEOUT = 120
PROXY = "http://username:password@host:port"

DDJSKEY = "AE3F04AD3F0D3A462481A337485081"
TAGS_URL = "https://datadome.garena.com/tags.js"
PAGE_URL = ("https://sso.garena.com/universal/login?app_id=10100"
            "&redirect_uri=https%3A%2F%2Faccount.garena.com%2F%3Flocale_name%3DVN"
            "&locale=vi-VN")
DDOPTIONS = {
    "abortAsyncOnCaptchaDisplay": False,
    "ajaxListenerPathExclusion": [
        "https://www.google-analytics.com", "api-js.datadome.co", "datadome.garena.com",
    ],
    "disableAutoRefreshOnCaptchaPassed": True,
    "enableTagEvents": True,
    "endpoint": "https://datadome.garena.com/js/",
    "sessionByHeader": False,
    "ajaxListenerPath": True,
}
ACCOUNT = "asdasd@asd.com"


def prelogin_url():
    return (f"https://sso.garena.com/api/prelogin?app_id=10100"
            f"&account={ACCOUNT.replace('@', '%40')}&format=json&id={int(time.time()*1000)}")


# ---------------------------------------------------------------------------
# riskbypass standard helpers
# ---------------------------------------------------------------------------
def run_task(payload):
    session = requests.Session()
    headers = {"Content-Type": "application/json", "x-api-key": TOKEN}
    print("Submitting task...", payload.get("task_type"))
    try:
        resp = session.post(f"{BASE_URL}/task/submit", headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print("Submit request error:", repr(e))
        return
    if not data.get("ok"):
        print("Submit failed:", data)
        return
    task_id = data.get("task_id")
    if not task_id:
        print("No task_id in response:", data)
        return
    print("Submitted, task_id =", task_id)

    start_time = time.time()
    while True:
        if time.time() - start_time > TIMEOUT:
            print("Timeout (seconds)")
            return
        try:
            r = session.get(f"{BASE_URL}/task/result/{task_id}",
                            headers={"Cache-Control": "no-cache", "x-api-key": TOKEN}, timeout=30)
            r.raise_for_status()
            j = r.json()
        except Exception as e:
            print("Polling error:", repr(e))
            time.sleep(1)
            continue
        st = j.get("status", "UNKNOWN")
        print("status:", st)
        if st in ("RUNNING", "QUEUED"):
            time.sleep(1)
            continue
        if st == "SUCCESS":
            return j.get("result")
        print("task end:", st, j.get("error", j))
        return


class RiskbypassResponse:
    def __init__(self, d):
        self.body = base64.b64decode(d.get("body_base64").encode())
        self.cookies = d.get("cookies", {})
        self.elapsed = d.get("elapsed", 0)
        self.error = d.get("error", None)
        self.headers = d.get("headers", {})
        self.ok = d.get("ok", False)
        self.reason = d.get("reason", "")
        self.status_code = d.get("status_code", 0)
        self.text = d.get("text", "")
        self.url = d.get("url", "")

    def json(self):
        return json.loads(self.body)


def riskbypass_tls_forward(url, method, headers, data, cookies, proxy, timeout=30):
    if isinstance(data, str):
        body_base64 = base64.b64encode(data.encode()).decode()
    elif isinstance(data, bytes):
        body_base64 = base64.b64encode(data).decode()
    elif isinstance(data, dict):
        body_base64 = base64.b64encode(urlencode(data).encode()).decode()
    else:
        body_base64 = None
    payload = {
        "task_type": "tls_forward", "proxy": proxy, "url": url, "method": method,
        "headers": headers, "body_base64": body_base64, "cookies_dict": cookies, "timeout": timeout,
    }
    result = run_task(payload)
    if not result:
        raise Exception("TLS Forward Error")
    return RiskbypassResponse(result)


# ---------------------------------------------------------------------------
def biz_headers(ua):
    return {
        "sec-ch-ua": '"Not;A=Brand";v="8", "Chromium";v="151", "Google Chrome";v="151"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "user-agent": ua,
        "accept": "application/json, text/plain, */*",
        "referer": PAGE_URL,
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept-language": "zh-CN,zh;q=0.9",
    }


def main():
    # Step1: datadome-tags -> initial cookie
    print("=== Step1: datadome-tags ===")
    r1 = run_task({
        "task_type": "datadome-tags", "proxy": PROXY, "target_url": PAGE_URL,
        "datadome_js_url": TAGS_URL, "ddjskey": DDJSKEY, "ddoptions": DDOPTIONS,
    })
    if not r1 or not r1.get("datadome"):
        raise Exception("tags task failed")
    dd, ua = r1["datadome"], r1.get("ua")
    print("  tags datadome:", dd[:32], "...  ua:", ua)

    # Step2: tls_forward hits prelogin, get the challenge url
    print("=== Step2: tls_forward prelogin (tags cookie) ===")
    resp = riskbypass_tls_forward(
        url=prelogin_url(), method="GET",
        headers=biz_headers(ua), data="",
        cookies={"datadome": dd}, proxy=PROXY,
    )
    print(f"  HTTP {resp.status_code}  body={resp.text[:150]}")
    if resp.status_code == 200 and "captcha-delivery.com" not in resp.text:
        print("\nOK -> passed on first hit")
        return
    try:
        challenge_url = resp.json()["url"]
    except Exception:
        print("\nFailed -> no challenge url")
        return
    task_type = "datadome-slider" if "/captcha/" in challenge_url else "datadome-interstitial"
    print(f"  challenge url ({'captcha' if '/captcha/' in challenge_url else 'interstitial'}) -> {task_type}")

    # Step3: feed the challenge url to the slider / interstitial task
    print(f"=== Step3: {task_type} ===")
    r3 = run_task({
        "task_type": task_type, "proxy": PROXY,
        "target_url": challenge_url, "target_method": "GET",
        "init_cookies": {"datadome": dd},
    })
    if not r3 or not r3.get("datadome"):
        print("\nFailed -> challenge task returned no cookie")
        return
    dd = r3["datadome"]
    ua = r3.get("ua") or ua
    print("  trusted datadome:", dd[:32], "...")

    # Step4: tls_forward hits prelogin again with the trusted cookie
    print("=== Step4: tls_forward prelogin (trusted cookie) ===")
    resp2 = riskbypass_tls_forward(
        url=prelogin_url(), method="GET",
        headers=biz_headers(ua), data="",
        cookies={"datadome": dd}, proxy=PROXY,
    )
    print(f"  HTTP {resp2.status_code}  body={resp2.text[:200]}")
    if resp2.status_code == 200 and "captcha-delivery.com" not in resp2.text:
        print("\nOK -> passed DataDome, got business response")
    else:
        print("\nFailed -> still blocked")


if __name__ == "__main__":
    main()
