# -*- coding: utf-8 -*-
# Walmart PerimeterX demo by riskbypass
# Flow: invisible → API call → if 403 → hold → verify → reuse loop
import re, json, random
from riskbypass import RiskByPassClient

BASE_URL = "https://riskbypass.com"
TOKEN    = "your_token"
TIMEOUT  = 120
PROXY    = "http://user:pass@host:port"

client = RiskByPassClient(token=TOKEN, base_url=BASE_URL)

TARGET_URL = "https://identity.walmart.com/account/login?tp=AuthMiddlewareSsr&client_id=5f3fb121-076a-45f6-9587-249f0bc160ff&redirect_uri=https%3A%2F%2Fwww.walmart.com%2Faccount%2FverifyToken&scope=openid+email+offline_access&tenant_id=elh9ie&state=%2Faccount%2Fprofile&code_challenge=Kx6xtdm2gXBcSoIN6rAnU9BeG422Vb6CLUO8d6eO948"
API_URL    = "https://identity.walmart.com/orchestra/idp/graphql"
PX_APP_ID  = "PXu6b0qd2S"
PX_JS_URL  = "https://client.perimeterx.net/PXu6b0qd2S/main.min.js"

LOGIN_QUERY = """query GetLoginOptions($input:UserOptionsInput!){getLoginOptions(input:$input){loginOptions{...LoginOptionsFragment}canUseEmailOTP phoneCollectionRequired authCode errors{...LoginOptionsErrorFragment}}}fragment LoginOptionsFragment on LoginOptions{loginId loginIdType emailId phoneNumber{number countryCode isoCountryCode}canUsePassword canUsePhoneOTP canUseEmailOTP loginPhoneLastFour maskedPhoneNumberDetails{loginPhoneLastFour countryCode isoCountryCode}loginMaskedEmailId signInPreference loginPreference lastLoginPreference hasRemainingFactors isPhoneConnected otherAccountsWithPhone loginMaskedEmailId hasPasskeyOnProfile accountDomain residencyRegion{residencyCountryCode residencyRegionCode}isIdentityMergeRequired}fragment LoginOptionsErrorFragment on IdentityLoginOptionsError{code message version}"""


def new_proxy():
    return PROXY


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


def call_api(cookies, ua, proxy, email="asdasdsa@gmail.com"):
    version, platform = parse_ua(ua)
    sec_ch_ua = f'"Not(A:Brand";v="8", "Chromium";v="{version}", "Google Chrome";v="{version}"'

    resp = client.tls_post(
        API_URL,
        cookies=cookies,
        headers={
            "accept": "application/json",
            "accept-language": "en-US",
            "content-type": "application/json",
            "origin": "https://identity.walmart.com",
            "referer": TARGET_URL,
            "sec-ch-ua": sec_ch_ua,
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": f'"{platform}"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "tenant-id": "elh9ie",
            "user-agent": ua,
            "wm_mp": "true",
            "x-apollo-operation-name": "GetLoginOptions",
            "x-enable-server-timing": "1",
            "x-latency-trace": "1",
        },
        json={
            "query": LOGIN_QUERY,
            "variables": {
                "input": {
                    "loginId": email,
                    "loginIdType": "EMAIL",
                    "ssoOptions": {
                        "wasConsentCaptured": True,
                        "callbackUrl": "https://www.walmart.com/account/verifyToken",
                        "clientId": "5f3fb121-076a-45f6-9587-249f0bc160ff",
                        "scope": "openid email offline_access",
                        "state": "/account/profile",
                        "challenge": "Kx6xtdm2gXBcSoIN6rAnU9BeG422Vb6CLUO8d6eO948",
                    },
                },
            },
        },
        proxies={"https": proxy},
    )
    return resp


def run_invisible(proxy):
    print("=" * 50)
    print("[Step 1] PX Invisible")
    print("=" * 50)
    result = client.run_task({
        "task_type": "perimeterx_invisible",
        "proxy": proxy,
        "target_url": TARGET_URL,
        "perimeterx_js_url": PX_JS_URL,
        "pxAppId": PX_APP_ID,
    }, timeout=TIMEOUT)
    if not result:
        print("[-] Invisible failed")
        return None
    print(f"[+] Invisible OK, cookies: {list(result['cookies'].keys())}")
    return result


def html_to_xhr(html):
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
            fields[key] = (val == "true") if key == "firstPartyEnabled" else val
    if not fields.get("appId"):
        m = re.search(r'PX[A-Za-z0-9]{8,}', html)
        if m:
            fields["appId"] = m.group(0)
    if not fields.get("blockScript") and fields.get("appId"):
        fields["blockScript"] = f"https://captcha.px-cdn.net/{fields['appId']}/captcha.js"
    return json.dumps(fields)


def run_hold(api_response, proxy):
    print("=" * 50)
    print("[Step 3] PX Hold (Press & Hold)")
    print("=" * 50)
    content_type = api_response.headers.get("content-type", "")
    try:
        init_cookies = api_response.cookies.get_dict()
    except Exception:
        init_cookies = dict(api_response.cookies)

    if "application/json" in content_type:
        block_data = api_response.text
    else:
        block_data = html_to_xhr(api_response.text)
        print(f"    html→xhr: {block_data[:200]}")

    print(f"    init_cookies={list(init_cookies.keys())}")

    result = client.run_task({
        "task_type": "perimeterx_hold",
        "proxy": proxy,
        "target_url": TARGET_URL,
        "block_mode": "xhr",
        "block_data": block_data,
        "init_cookies": init_cookies,
        "pm": "us"
    }, timeout=TIMEOUT)
    if not result:
        print("[-] Hold failed")
        return None
    print(f"[+] Hold OK, cookies: {list(result['cookies'].keys())}")
    return result


def main():
    for i in range(100):
        proxy = new_proxy()

        # 1) Invisible
        inv = run_invisible(proxy)
        inv = {
            'cookies': {},
            'ua': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'
        }
        if not inv:
            continue
        cookies = inv["cookies"]
        ua = inv["ua"]

        # 2) Call API
        print("=" * 50)
        print("[Step 2] Call API")
        print("=" * 50)
        r = call_api(cookies, ua, proxy)
        print(f"    HTTP {r.status_code}: {r.text[:100]}...")

        current_cookies = cookies
        current_ua = ua

        if r.status_code == 412:
            print("[!] 412 → triggering hold")
            hold = run_hold(r, proxy)
            if not hold:
                continue
            current_cookies = {**cookies, **hold["cookies"]}
            current_ua = hold.get("ua", ua)

            print("=" * 50)
            print("[Step 4] Verify after hold")
            print("=" * 50)
            r = call_api(current_cookies, current_ua, proxy)
            print(f"    HTTP {r.status_code}: {r.text[:100]}...")
            if r.status_code != 200:
                print(f"[-] Still blocked: {r.status_code}")
                continue
        elif r.status_code != 200:
            print(f"[-] Unexpected status: {r.status_code}")
            continue

        print(f"\n[+] Login result: {r.text[:200]}...")


if __name__ == "__main__":
    main()
