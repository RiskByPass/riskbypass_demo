# -*- coding: utf-8 -*-
# UPS Login demo — Akamai Bot Manager bypass via RiskByPass
import re
from riskbypass import RiskByPassClient
from requests_go import Session
from requests_go.tls_config import TLS_CHROME_LATEST

BASE_URL = "https://riskbypass.com"
TOKEN    = "your_token"
TIMEOUT  = 120
PROXY    = "http://user:pass@host:port"

client = RiskByPassClient(token=TOKEN, base_url=BASE_URL)

UPS_HOME       = "https://www.ups.com/us/en/home"
UPS_LOGIN_PAGE = "https://id.ups.com/u/login/identifier"
UPS_LOGIN_POST = "https://id.ups.com/u/login/password"

USERNAME = "your_email@example.com"
PASSWORD = "your_password"

PAGE_FP = "424541475255404d4b4546454b5d5655405a425f4245434752555d505f5e4345435052555d505f435e595f595349484d414242515f5b59"
DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"


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


def build_headers(ua, referer=None, content_type=None):
    version, platform = parse_ua(ua)
    sec_ch_ua = f'"Chromium";v="{version}", "Google Chrome";v="{version}", "Not/A)Brand";v="99"'
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en,en-US;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": sec_ch_ua,
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": f'"{platform}"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": ua,
    }
    if referer:
        headers["referer"] = referer
        headers["sec-fetch-site"] = "same-origin"
    if content_type:
        headers["content-type"] = content_type
    return headers


def extract_akamai_js_url(html, domain="https://id.ups.com"):
    scripts = re.findall(r'<script[^>]*src="([^"]+)"[^>]*>', html)
    for src in reversed(scripts):
        if src.startswith("/") and len(src) > 30 and "." not in src.split("/")[-1]:
            return domain + src
    return "https://id.ups.com/5X7GjEHC/HsXgaSx/pbgI9Nv/uT/7D1V4SEYhi7OpSfi/MHNfInI/QjYwJ/XBiO2IB"


def main():
    session = Session()
    session.tls_config = TLS_CHROME_LATEST
    proxies = {"https": PROXY}

    # Step 1: Visit login page via Session (preserves cookies through redirects)
    print("=" * 50)
    print("[Step 1] Get Auth0 login page")
    print("=" * 50)

    resp = session.get(UPS_HOME, headers=build_headers(DEFAULT_UA), proxies=proxies)
    print(f"    Home HTTP {resp.status_code}")

    login_url = None
    m = re.search(r'href="([^"]*(?:lasso/login|lasso/signin)[^"]*)"', resp.text, re.I)
    if m:
        url = m.group(1)
        login_url = url if url.startswith("http") else "https://www.ups.com" + url
    login_url = login_url or (UPS_LOGIN_PAGE + "?ui_locales=en")
    print(f"    login_url: {login_url[:100]}...")

    for attempt in range(3):
        try:
            resp = session.get(login_url, headers=build_headers(DEFAULT_UA, referer=UPS_HOME), proxies=proxies)
            break
        except Exception as e:
            print(f"    attempt {attempt+1} failed: {str(e)[:80]}")
            if attempt == 2:
                print("[-] Failed to reach login page")
                return
    print(f"    Login page HTTP {resp.status_code}")
    print(f"    URL: {resp.url[:120]}...")

    init_cookies = session.cookies.get_dict()
    print(f"    init_cookies: {list(init_cookies.keys())}")

    # extract state
    state = None
    m = re.search(r'state=([^&"\']+)', resp.url)
    if m:
        state = m.group(1)
    if not state:
        m = re.search(r'<input[^>]*name="state"[^>]*value="([^"]+)"', resp.text)
        if m:
            state = m.group(1)
    if not state:
        print("[-] Could not extract state param")
        print(f"    Body: {resp.text[:500]}")
        return
    print(f"    state: {state[:50]}...")

    akamai_js_url = extract_akamai_js_url(resp.text)
    print(f"    akamai_js_url: {akamai_js_url}")

    target_url = f"{UPS_LOGIN_PAGE}?state={state}&ui_locales=en"

    # Step 2: Solve Akamai
    print("\n" + "=" * 50)
    print("[Step 2] Solve Akamai")
    print("=" * 50)
    akamai_result = client.run_task({
        "task_type": "akamai",
        "proxy": PROXY,
        "target_url": target_url,
        "akamai_js_url": akamai_js_url,
        "page_fp": PAGE_FP,
        "init_cookies": init_cookies,
    }, timeout=TIMEOUT)
    if not akamai_result:
        print("[-] Akamai solve failed")
        return
    solved_cookies = akamai_result.get("cookies_dict") or akamai_result.get("cookies", {})
    ua = akamai_result.get("ua", DEFAULT_UA)
    print(f"[+] Akamai OK, cookies: {list(solved_cookies.keys())}")
    print(f"    ua: {ua}")

    # inject solver cookies into session
    for k, v in solved_cookies.items():
        session.cookies.set(k, v)

    # Step 3: Submit username
    print("\n" + "=" * 50)
    print("[Step 3] Submit username")
    print("=" * 50)
    form_data = {
        "state": state,
        "username": USERNAME,
        "js-available": "true",
        "webauthn-available": "true",
        "is-brave": "false",
        "webauthn-platform-available": "true",
        "action": "default",
    }
    resp = session.post(
        target_url,
        headers=build_headers(ua, referer=target_url, content_type="application/x-www-form-urlencoded"),
        data=form_data,
        proxies=proxies,
    )
    print(f"    HTTP {resp.status_code}")
    print(f"    URL: {resp.url[:120]}...")

    if '/login/password' not in resp.url and '/login/password' not in resp.text:
        print(f"    Not redirected to password page (invalid username or blocked)")
        print(f"    Body: {resp.text[:300]}")
        return
    print("    → password page")

    m = re.search(r'state=([^&"\']+)', resp.url)
    if m:
        state = m.group(1)

    # Step 4: Submit password
    print("\n" + "=" * 50)
    print("[Step 4] Submit password")
    print("=" * 50)
    pw_form_data = {
        "state": state,
        "username": USERNAME,
        "password": PASSWORD,
        "js-available": "true",
        "webauthn-available": "true",
        "is-brave": "false",
        "webauthn-platform-available": "true",
        "action": "default",
    }
    password_post_url = f"{UPS_LOGIN_POST}?state={state}&ui_locales=en"
    resp = session.post(
        password_post_url,
        headers=build_headers(ua, referer=password_post_url, content_type="application/x-www-form-urlencoded"),
        data=pw_form_data,
        proxies=proxies,
    )
    print(f"    HTTP {resp.status_code}")
    final_url = resp.url
    print(f"    URL: {final_url}")

    if 'ups.com' in final_url and 'login' not in final_url:
        print("\n[+] Login success!")
        print(f"    Cookies: {list(session.cookies.get_dict().keys())}")
    else:
        print(f"\n[-] Login failed")
        print(f"    Body: {resp.text[:500]}")


if __name__ == "__main__":
    main()
