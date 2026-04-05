# -*- coding: utf-8 -*-
# Canal+ Poland login demo by riskbypass
# Deps: pip install riskbypass
import json, random, re
from riskbypass import RiskByPassClient

BASE_URL = "https://riskbypass.com"
TOKEN    = "your_token"
TIMEOUT  = 120

client = RiskByPassClient(token=TOKEN, base_url=BASE_URL)

PROXY = "http://username:password@proxy_host:port" # poland proxy, use static proxy or sticky proxy, don't use dynamic proxy

TARGET_URL = ("https://logowanie.pl.canalplus.com/login?service=https%3A%2F%2F"
              "logowanie.pl.canalplus.com%2Foauth2.0%2FcallbackAuthorize%3F"
              "client_id%3Da0BUfO0bry.web.pass.canal-plus.com%26redirect_uri%3D"
              "https%253A%252F%252Fpass.canal-plus.com%252Fprovider%252Foauth2sp"
              "%252Fauth%252FCPPOL%26response_type%3Dcode%26state%3Dredirect_uri"
              "%253Dhttps%25253A%25252F%25252Fwww.canalplus.com%25252Fpl%25252F"
              "%2526platform%253Dweb%2526media%253Dweb%2526offerLocation%253Dpl"
              "%26client_name%3DCasOAuthClient&platform=web")

AKAMAI_JS_URL = ("https://logowanie.pl.canalplus.com/pQjnstTGr/ncrL/6t_/"
                 "EVJmNZFVFx0/YN5LrktQkGmQcJ9a1p/Dmt0/WwgnG/R09SygB")
PAGE_FP = ("42455e5a4e495c515f42475142475a4f444d4348424543475255414d4b"
           "4546454b5d5655405a425f4245434753554859405f4a5140475242")

USERNAME = "test123456789@gmail.com"
PASSWORD = "adnbsadh12312."
RECAPTCHA_TOKEN = "YOUR_RECAPTCHA_TOKEN"


def task():
    # ====== Step 1: GET Login page, get init_cookies + execution ======
    print("[1] GET Login page ...")
    resp = client.tls_get(
        TARGET_URL,
        proxies={"https": PROXY},
        headers={
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        },
    )
    try:
        init_cookies = resp.cookies.get_dict()
    except:
        init_cookies = dict(resp.cookies)
    print(f"    init_cookies: {list(init_cookies.keys())}")

    # Extract execution token
    m = re.search(r'name="execution"\s+value="([^"]+)"', resp.text)
    if not m:
        print("[-] Execution token not found")
        return
    execution = m.group(1)
    print(f"    execution = {execution[:60]}...")
    try:
        akamai_js_url = 'https://logowanie.pl.canalplus.com' + re.findall(r'<script type="text/javascript"  src="(.*?)"', resp.text)[-1]
    except:
        akamai_js_url = AKAMAI_JS_URL
    # ====== Step 2: Get akamai _abck ======
    print("[2] Get akamai _abck ...")
    payload = {
        "task_type": "akamai",
        "proxy": PROXY,
        "target_url": TARGET_URL,
        "akamai_js_url": akamai_js_url,
        "page_fp": PAGE_FP,
        "init_cookies": init_cookies,
        "pm": "poland"
    }
    result = client.run_task(payload, timeout=TIMEOUT)
    if not result:
        print("[-] Akamai task failed")
        return
    print(f"    _abck = {result['cookies_dict']['_abck'][:60]}...")

    # ====== Step 3: Merge cookies, send login request ======
    print("[3] Send login request ...")

    cookies = {}
    cookies.update(init_cookies)
    cookies.update(result["cookies_dict"])

    headers = {
        "User-Agent": result["ua"],
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://logowanie.pl.canalplus.com",
        "pragma": "no-cache",
        "referer": TARGET_URL,
        "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
    }

    params = {
        "service": "https://logowanie.pl.canalplus.com/oauth2.0/callbackAuthorize?client_id=a0BUfO0bry.web.pass.canal-plus.com&redirect_uri=https%3A%2F%2Fpass.canal-plus.com%2Fprovider%2Foauth2sp%2Fauth%2FCPPOL&response_type=code&state=redirect_uri%3Dhttps%253A%252F%252Fwww.canalplus.com%252Fpl%252F%26platform%3Dweb%26media%3Dweb%26offerLocation%3Dpl&client_name=CasOAuthClient",
        "platform": "web",
    }

    data = {
        "username": USERNAME,
        "password": PASSWORD,
        "g-recaptcha-token": RECAPTCHA_TOKEN,
        "execution": execution,
        "_eventId": "submit",
        "geolocation": "",
    }

    resp = client.tls_post(
        "https://logowanie.pl.canalplus.com/login",
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
        proxies={"https": PROXY},
    )

    print(f"    status = {resp.status_code}")


if __name__ == "__main__":
    task()
