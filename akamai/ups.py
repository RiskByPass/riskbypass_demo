# -*- coding: utf-8 -*-
import random
import re
import time
from urllib.parse import urljoin

from riskbypass import RiskByPassClient
from cycronet import CronetClient


BASE_URL = "https://riskbypass.com"
TOKEN = "your_token"
TIMEOUT = 120

UPS_HOME       = "https://www.ups.com/us/en/home"
UPS_LASSO      = "https://www.ups.com/lasso/login?loc=en_US"
UPS_LOGIN_PAGE = "https://id.ups.com/u/login/identifier"
UPS_LOGIN_POST = "https://id.ups.com/u/login/password"

EMAIL = "asdasd@sds.com"
PASSWORD = "sadasd2131."

PAGE_FP = "424541475255404d5e425e51455f4e484b505f415e595f5b4e4148525f4b4a5a5f5b59495c4c425f42454347504840595f4143594b475242"
DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"

client = RiskByPassClient(token=TOKEN, base_url=BASE_URL)


def make_proxy():
    return f"http://user:pass@host:port"


def extract_sbsd_js_url(html, base_url):
    m = re.search(r'<script[^>]*\bsrc="(/[^"?]+\?v=[^"]+)"[^>]*defer', html)
    if m:
        return urljoin(base_url, m.group(1))
    return None

def parse_ua(ua):
    m = re.search(r'Chrome/(\d+)', ua)
    version = m.group(1) if m else "149"
    if "Macintosh" in ua or "Mac OS X" in ua:
        platform = "macOS"
    elif "Linux" in ua and "Android" not in ua:
        platform = "Linux"
    else:
        platform = "Windows"
    return version, platform


def build_headers(ua, referer=None, content_type=None, origin=None):
    version, platform = parse_ua(ua)
    sec_ch_ua = f'"Chromium";v="{version}", "Google Chrome";v="{version}", "Not_A Brand";v="99"'
    h = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=0, i",
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
        h["referer"] = referer
        h["sec-fetch-site"] = "same-origin"
    if origin:
        h["origin"] = origin
    if content_type:
        h["content-type"] = content_type
    return h


def extract_akamai_js_url(html, base_url):
    scripts = re.findall(r'<script[^>]*\bsrc="([^"]+)"[^>]*>', html)
    candidates = []
    for src in scripts:
        if not src.startswith("/"):
            continue
        path = src.split("?")[0]
        last = path.rsplit("/", 1)[-1]
        if "." in last:
            continue
        if path.count("/") < 4 or len(path) < 30:
            continue
        candidates.append(src)
    if not candidates:
        return None
    src = candidates[-1]
    return urljoin(base_url, src)


def extract_state(url, html=""):
    m = re.search(r'state=([^&"\']+)', url)
    if m:
        return m.group(1)
    m = re.search(r'<input[^>]*name="state"[^>]*value="([^"]+)"', html)
    if m:
        return m.group(1)
    m = re.search(r'"state"\s*:\s*"([^"]+)"', html)
    if m:
        return m.group(1)
    return None


def solve_akamai(session, target_resp, proxy, label):
    js_url = extract_akamai_js_url(target_resp.text, target_resp.url)
    if not js_url:
        print(f"  [{label}] 找不到 akamai js url")
        print(target_resp.text[:400])
        return None, None
    init_cookies = session.cookies.get_dict()
    print(f"  [{label}] target_url = {target_resp.url[:100]}")
    print(f"  [{label}] akamai_js  = {js_url[:100]}")
    print(f"  [{label}] init_cookies = {list(init_cookies.keys())}")
    result = client.run_task({
        "task_type": "akamai",
        "proxy": proxy,
        "target_url": target_resp.url,
        "akamai_js_url": js_url,
        "sbsd_js_url": extract_sbsd_js_url(target_resp.text, target_resp.url),
        "page_fp": PAGE_FP,
        "init_cookies": init_cookies,
    }, timeout=TIMEOUT)
    if not result:
        return None, None
    cookies = result.get("cookies_dict") or result.get("cookies", {})
    ua = result.get("ua")
    print(f"  [{label}] solved, _abck={(cookies.get('_abck') or '')[:50]}...")
    return cookies, ua


def is_akamai_challenge(resp):
    return ("sec-if-cpt-container" in resp.text
            or "bm-verify" in resp.text
            or "akamai" in resp.text.lower() and "<script" in resp.text and len(resp.text) < 4000)


def main(proxy):
    """返回最后一步的 HTTP 状态码（int），异常/中途失败返回 None"""
    proxies = {"http": proxy, "https": proxy}
    session = CronetClient(
        chrometls="chrome_147",
        proxies=proxies,
        verify=False,
        timeout_ms=30000,
    )
    ua = DEFAULT_UA

    print("=" * 60)
    print("[Step 1] Home")
    print("=" * 60)
    resp = session.get(UPS_HOME, headers=build_headers(ua), timeout=30)
    print(f"  HTTP {resp.status_code}  URL={resp.url[:80]}")
    print(f"  cookies: {list(session.cookies.get_dict().keys())}")

    print("\n" + "=" * 60)
    print("[Step 2] /lasso/login (过 www.ups.com 的 Akamai)")
    print("=" * 60)
    resp = session.get(UPS_LASSO,
                       headers=build_headers(ua, referer=UPS_HOME),
                       timeout=30, allow_redirects=True)
    print(f"  HTTP {resp.status_code}  URL={resp.url[:120]}")

    if "id.ups.com" not in resp.url:
        if not is_akamai_challenge(resp):
            print(f"[-] 既没跳到 id.ups.com 又不像挑战页，body:\n{resp.text[:600]}")
            return None
        print("  → 命中 www.ups.com Akamai 挑战，开始 solve")
        cookies, new_ua = solve_akamai(session, resp, proxy, "www.ups.com")
        if not cookies:
            print("[-] www.ups.com Akamai solve 失败")
            return None
        for k, v in cookies.items():
            session.cookies.set(k, v)
        if new_ua:
            ua = new_ua

        resp = session.get(UPS_LASSO,
                           headers=build_headers(ua, referer=UPS_HOME),
                           timeout=30, allow_redirects=True)
        print(f"  retry HTTP {resp.status_code}  URL={resp.url[:120]}")
        if "id.ups.com" not in resp.url:
            print("[-] 过完 www Akamai 仍未跳到 id.ups.com")
            print(resp.text[:600])
            return None

    print("\n" + "=" * 60)
    print("[Step 3] id.ups.com identifier 页 (过 id.ups.com 的 Akamai)")
    print("=" * 60)

    if is_akamai_challenge(resp):
        print("  → 命中 id.ups.com Akamai 挑战，开始 solve")
        cookies, new_ua = solve_akamai(session, resp, proxy, "id.ups.com (challenge)")
        if not cookies:
            print("[-] id.ups.com Akamai solve 失败")
            return None
        for k, v in cookies.items():
            session.cookies.set(k, v)
        if new_ua:
            ua = new_ua
        resp = session.get(resp.url,
                           headers=build_headers(ua, referer=UPS_HOME),
                           timeout=30, allow_redirects=True)
        print(f"  retry HTTP {resp.status_code}  URL={resp.url[:120]}")

    state = extract_state(resp.url, resp.text)
    if not state:
        print("[-] 拿不到 state")
        print(resp.text[:600])
        return None
    print(f"  state: {state[:60]}...")

    print("  → 正常 identifier 页，对 id.ups.com 再 solve 一次拿业务态 _abck")
    cookies, new_ua = solve_akamai(session, resp, proxy, "id.ups.com (form)")
    if not cookies:
        print("[-] id.ups.com 业务态 Akamai solve 失败")
        return None
    for k, v in cookies.items():
        session.cookies.set(k, v)
    if new_ua:
        ua = new_ua

    identifier_url = f"{UPS_LOGIN_PAGE}?state={state}&ui_locales=zh-CN"

    print("\n" + "=" * 60)
    print("[Step 4] POST username")
    print("=" * 60)
    form_data = {
        "state": state,
        "username": EMAIL,
        "js-available": "true",
        "webauthn-available": "true",
        "is-brave": "false",
        "webauthn-platform-available": "true",
        "action": "default",
    }
    resp = session.post(
        identifier_url,
        headers=build_headers(ua, referer=identifier_url,
                              content_type="application/x-www-form-urlencoded",
                              origin="https://id.ups.com"),
        data=form_data,
        timeout=30,
        allow_redirects=True,
    )
    print(f"  HTTP {resp.status_code}  URL={resp.url[:120]}")

    if "/login/password" not in resp.url and "/login/password" not in resp.text:
        print("[-] 没进入 password 页（用户名无效 或 被风控）")
        print(resp.text[:600])
        return resp.status_code

    new_state = extract_state(resp.url, resp.text)
    if new_state:
        state = new_state
    print(f"  state (post-identifier): {state[:60]}...")

    print("\n" + "=" * 60)
    print("[Step 5] POST password")
    print("=" * 60)
    password_url = f"{UPS_LOGIN_POST}?state={state}&ui_locales=zh-CN"
    pw_form_data = {
        "state": state,
        "username": EMAIL,
        "password": PASSWORD,
        "js-available": "true",
        "webauthn-available": "true",
        "is-brave": "false",
        "webauthn-platform-available": "true",
        "action": "default",
    }
    resp = session.post(
        password_url,
        headers=build_headers(ua, referer=password_url,
                              content_type="application/x-www-form-urlencoded",
                              origin="https://id.ups.com"),
        data=pw_form_data,
        timeout=30,
        allow_redirects=True,
    )
    print(f"  HTTP {resp.status_code}")
    print(f"  Final URL: {resp.url}")
    print(f"  Body: {resp.text[:300]}")
    return resp.status_code


if __name__ == "__main__":
    proxy = make_proxy()
    print(f"proxy={proxy}\n")
    try:
        status = main(proxy)
    except Exception as e:
        print(f"[!] crashed: {e}")
        status = None

    if status == 400:
        print("\n>>> 结果: SUCCESS(400)")
    elif status == 403:
        print("\n>>> 结果: FAIL(403)")
    else:
        print(f"\n>>> 结果: OTHER({status})")