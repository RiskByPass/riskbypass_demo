# -*- coding: utf-8 -*-
# PrizePicks PerimeterX demo by riskbypass
# Flow: invisible → API call → if 403 → hold (press & hold captcha)
import re, json
from riskbypass import RiskByPassClient
import requests

BASE_URL = "https://riskbypass.com"
TOKEN    = "your_token"
TIMEOUT  = 120
PROXY    = "http://user:pass@host:port"

client = RiskByPassClient(token=TOKEN, base_url=BASE_URL)

TARGET_URL   = "https://app.prizepicks.com/"
API_URL      = "https://api.prizepicks.com/core/streaks/milestones"
PX_APP_ID    = "PXZNeitfzP"
PX_JS_URL    = "https://client.perimeterx.net/PXZNeitfzP/main.min.js"


def parse_ua(ua: str):
    version = "148"
    m = re.search(r'Chrome/(\d+)', ua)
    if m:
        version = m.group(1)
    if "Macintosh" in ua or "Mac OS X" in ua:
        platform = "macOS"
    elif "Linux" in ua and "Android" not in ua:
        platform = "Linux"
    else:
        platform = "Windows"
    return version, platform


def call_api(cookies, ua, proxy):
    version, platform = parse_ua(ua)
    sec_ch_ua = f'"Chromium";v="{version}", "Google Chrome";v="{version}", "Not/A)Brand";v="99"'

    resp = requests.get(
        API_URL,
        cookies=cookies,
        headers={
            "accept": "*/*",
            "accept-language": "en",
            "cache-control": "no-cache",
            "origin": "https://app.prizepicks.com",
            "pragma": "no-cache",
            "referer": "https://app.prizepicks.com/",
            "sec-ch-ua": sec_ch_ua,
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": f'"{platform}"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": ua,
            "x-device-id": "aff4eae8-5663-4ec0-b594-806d11b3da42",
            "x-device-info": "anonymousId=,name=,os=windows,osVersion=Windows NT 10.0; Win64; x64,platform=,appVersion=,gameMode=,stateCode=",
        },
        proxies={"https": proxy},
    )
    return resp


def run_invisible():
    print("=" * 50)
    print("[Step 1] PX Invisible")
    print("=" * 50)
    result = client.run_task({
        "task_type": "perimeterx_invisible",
        "proxy": PROXY,
        "target_url": TARGET_URL,
        "perimeterx_js_url": PX_JS_URL,
        "pxAppId": PX_APP_ID,
    }, timeout=TIMEOUT)
    if not result:
        print("[-] Invisible failed")
        return None
    print(f"[+] Invisible OK, cookies: {list(result['cookies'].keys())}")
    return result


def html_to_xhr(html: str) -> str:
    """从 PX HTML 拦截页提取参数，转为 xhr JSON 格式"""
    fields = {}
    patterns = {
        "appId": r"_pxAppId\s*[=:]\s*['\"]([^'\"]+)",
        "jsClientSrc": r"_pxJsClientSrc\s*[=:]\s*['\"]([^'\"]+)",
        "firstPartyEnabled": r"_pxFirstPartyEnabled\s*[=:]\s*(true|false)",
        "vid": r"_pxVid\s*[=:]\s*['\"]([^'\"]+)",
        "uuid": r"_pxUuid\s*[=:]\s*['\"]([^'\"]+)",
        "hostUrl": r"_pxHostUrl\s*[=:]\s*['\"]([^'\"]+)",
        "blockScript": r"_pxBlockScript\s*[=:]\s*['\"]([^'\"]+)",
    }
    for key, pat in patterns.items():
        m = re.search(pat, html)
        if m:
            val = m.group(1)
            if key == "firstPartyEnabled":
                fields[key] = val == "true"
            else:
                fields[key] = val

    if not fields.get("appId"):
        m = re.search(r'PX[A-Za-z0-9]{8,}', html)
        if m:
            fields["appId"] = m.group(0)

    if not fields.get("blockScript") and fields.get("appId"):
        fields["blockScript"] = f"https://captcha.px-cdn.net/{fields['appId']}/captcha.js"

    return json.dumps(fields)


def run_hold(api_response):
    print("=" * 50)
    print("[Step 3] PX Hold (Press & Hold)")
    print("=" * 50)
    content_type = api_response.headers.get("content-type", "")
    try:
        init_cookies = api_response.cookies.get_dict()
    except:
        init_cookies = dict(api_response.cookies)

    if "application/json" in content_type:
        block_data = api_response.text
    else:
        block_data = html_to_xhr(api_response.text)
        print(f"    html→xhr: {block_data[:200]}")
    block_mode = "xhr"

    print(f"    block_mode={block_mode}, init_cookies={list(init_cookies.keys())}")

    result = client.run_task({
        "task_type": "perimeterx_hold",
        "proxy": PROXY,
        "target_url": TARGET_URL,
        "block_mode": block_mode,
        "block_data": block_data,
        "init_cookies": init_cookies,
        "pm":"us"
    }, timeout=TIMEOUT)
    if not result:
        print("[-] Hold failed")
        return None
    print(f"[+] Hold OK, cookies: {list(result['cookies'].keys())}")
    return result


def main():
    # 1) Invisible
    # inv = run_invisible()
    inv = {
        'cookies': {},
        'ua': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'
    }
    if not inv:
        return

    cookies = inv["cookies"]
    ua = inv["ua"]

    # 2) Call API
    print("=" * 50)
    print("[Step 2] Call API")
    print("=" * 50)
    r = call_api(cookies, ua, PROXY)
    print(f"    HTTP {r.status_code}: {r.text[:100]}...")

    current_cookies = cookies
    current_ua = ua

    if r.status_code == 403:
        print("[!] 403 → triggering hold")
        hold = run_hold(r)
        if not hold:
            return
        current_cookies = {**cookies, **hold["cookies"]}
        current_ua = hold.get("ua", ua)

        print("=" * 50)
        print("[Step 4] Verify after hold")
        print("=" * 50)
        r = call_api(current_cookies, current_ua, PROXY)
        print(f"    HTTP {r.status_code}: {r.text[:100]}...")
        if r.status_code != 200:
            print(f"[-] Still blocked: {r.status_code}")
            return
    elif r.status_code != 200:
        print(f"[-] Unexpected status: {r.status_code}")
        return

    # Reuse loop
    print("=" * 50)
    print("[Reuse] Testing cookie reuse")
    print("=" * 50)
    reuse = 0
    for i in range(500):
        try:
            r2 = call_api(current_cookies, current_ua, PROXY)
            if r2.status_code == 200:
                reuse += 1
                print(f"  [{i+1}] OK: {r2.text[:80]}...")
            elif r2.status_code == 403:
                print(f"  [{i+1}] 403 → hold")
                hold = run_hold(r2)
                if hold:
                    current_cookies = {**current_cookies, **hold["cookies"]}
                    current_ua = hold.get("ua", current_ua)
                    reuse += 1
                else:
                    break
            else:
                print(f"  [{i+1}] HTTP {r2.status_code}")
                break
        except Exception as e:
            print(f"  [{i+1}] Error: {e}")
            break
    print(f"Reuse: {reuse}/500")


if __name__ == "__main__":
    main()
