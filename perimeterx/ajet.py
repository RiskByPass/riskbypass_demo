# -*- coding: utf-8 -*-
# Ajet PerimeterX demo by riskbypass
# Flow: invisible → API call → if 403 → hold (press & hold captcha)
# Deps: pip install riskbypass
import json, re
from datetime import datetime, timedelta
from riskbypass import RiskByPassClient
import random
import string

BASE_URL = "https://riskbypass.com"
TOKEN    = "your token"
TIMEOUT  = 120

client = RiskByPassClient(token=TOKEN, base_url=BASE_URL)

new_session = "".join(random.choices(string.ascii_letters + string.digits, k=9))
print(new_session)
PROXY = f"http://xxxxxxxxx-zone-custom-region-us-session-{new_session}-sessTime-60:xxxxxxxxxxxxx@xxxxxxxxx.xxxxx.xxxxx.xxxxxxxxxxxx.net:2333"


AJET_TARGET_URL = "https://ajet.com/booking/availability"
AJET_PX_APP_ID  = "PXGw9AVGdM"
AJET_PX_JS_URL  = "https://client.perimeterx.net/PXGw9AVGdM/main.min.js"
AJET_API_URL    = "https://gatewayweb.cloud.ajet.com/availability/availability/getavailability"


def parse_ua(ua: str):
    version = "131"
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
    flight_date = (datetime.utcnow() + timedelta(days=3)).strftime("%d.%m.%Y")
    version, platform = parse_ua(ua)
    sec_ch_ua = f'"Chromium";v="{version}", "Google Chrome";v="{version}", "Not/A)Brand";v="99"'

    resp = client.tls_post(
        AJET_API_URL,
        cookies=cookies,
        headers={
            "accept": "application/json",
            "content-type": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "origin": "https://ajet.com",
            "referer": "https://ajet.com/booking/availability",
            "sec-ch-ua": sec_ch_ua,
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": f'"{platform}"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": ua,
        },
        json={
            "flights": [{"departurePort": "SAW", "departureDate": flight_date, "arrivalPort": "ADF"}],
            "passengers": [{"passengerType": "ADLT", "passengerSubType": None, "quantity": 1}],
            "tripType": "ONE_WAY",
            "currencyCode": "TRY",
        },
        proxies={"https": PROXY},
    )
    return resp


def run_invisible():
    print("=" * 50)
    print("[Step 1] PX Invisible")
    print("=" * 50)
    payload = {
        "task_type": "perimeterx_invisible",
        "proxy": PROXY,
        "target_url": AJET_TARGET_URL,
        "perimeterx_js_url": AJET_PX_JS_URL,
        "pxAppId": AJET_PX_APP_ID,
    }
    result = client.run_task(payload, timeout=TIMEOUT)
    if not result:
        print("[-] Invisible failed")
        return None
    print(f"[+] Invisible OK, cookies: {list(result['cookies'].keys())}")
    return result


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
        block_mode = "xhr"
        block_data = api_response.text
    else:
        block_mode = "html"
        block_data = api_response.text

    print(f"    block_mode={block_mode}, init_cookies={list(init_cookies.keys())}")

    payload = {
        "task_type": "perimeterx_hold",
        "proxy": PROXY,
        "target_url": AJET_TARGET_URL,
        "block_mode": block_mode,
        "block_data": block_data,
        "init_cookies": init_cookies
    }
    result = client.run_task(payload, timeout=TIMEOUT)
    if not result:
        print("[-] Hold failed")
        return None
    print(f"[+] Hold OK, cookies: {list(result['cookies'].keys())}")
    return result


def main():
    # 1) Invisible can be used too
    # inv = run_invisible()
    inv = {
        "cookies": {},
        "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36" # support any ua
    }
    if not inv:
        return

    # cookies = inv["cookies"]
    cookies = {}
    ua = inv["ua"]

    # 2) Call API with invisible cookies
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
