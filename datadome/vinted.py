# -*- coding: utf-8 -*-
# Vinted OAuth — riskbypass custom_task (datadome + DD challenge) + tls_client OAuth
import re
import tls_client
from riskbypass import RiskByPassClient

BASE_URL = "https://riskbypass.com"
TOKEN = "your_token"
PROXY = "http://user:pass@host:port"
TARGET_URL = "https://www.vinted.com/member/signup/select_type?ref_url=%2F"
OAUTH_URL = "https://www.vinted.com/web/api/auth/oauth"

client = RiskByPassClient(token=TOKEN, base_url=BASE_URL)

OAUTH_PARAMS = {
    "client_id": "web",
    "scope": "user",
    "username": "17969327as92@qq.com",
    "password": "dssada21.",
    "fingerprint": "ea4615708522163b7cff8f3cdedd8c4b",
    "grant_type": "password",
}

HEADER_ORDER = [
    "content-length",
    "sec-ch-ua-platform",
    "x-csrf-token",
    "accept-language",
    "sec-ch-ua",
    "sec-ch-ua-mobile",
    "user-agent",
    "accept",
    "content-type",
    "locale",
    "origin",
    "sec-fetch-site",
    "sec-fetch-mode",
    "sec-fetch-dest",
    "referer",
    "accept-encoding",
    "cookie",
    "priority",
]

COOKIES_BASE = {
    "v_udt": "eEhxZk1ucHZYYXZ5N1dKclRQL0ZILzlyZDhWLy0tTythM1p1dHhtUFdEMnNMbi0tZ0JBU2cvOHF6ekl3NDRzcGd1bGJTdz09",
    "anon_id": "679d17bd-c565-464c-be05-abd79b776ce8",
    "anonymous-locale": "en-us-fr",
    "anonymous-iso-locale": "en-US",
    "non_dot_com_www_domain_cookie_buster": "1",
    "refresh_token_web": "eyJhbGciOiJQUzI1NiIsImtpZCI6IkU1N1lkcnVIcGxBanUyY05vMURvckgzajI3QnU1LXNfT1A1UHdQaWhuNU0ifQ.eyJhcHBfaWQiOjQsImF1ZCI6ImZyLmNvcmUuYXBpLnZpbnRlZC5jb20iLCJjbGllbnRfaWQiOiJ3ZWIiLCJleHAiOjE3ODExMDY1MzcsImlhdCI6MTc4MTA2MzMzNiwiaXNzIjoidmludGVkLWlhbS1zZXJ2aWNlIiwicHVycG9zZSI6InJlZnJlc2giLCJzY29wZSI6InB1YmxpYyIsInNpZCI6ImQyMDQ4Njg3LTE3ODEwNjMzMzYifQ.F5KudoWRRjCLCzVXPqlTw7Od3uz3DDOrZO6HRuT1ssl0wGMrKyyfEd1YieDOx80yKpmYErIOrpw52yaFUTQqwfsbSUJP_JRrvhPOSqARvjzDm28s6Ue6IaencQiO6j6Pje_o6jkytt-rQnNnK3Ce1_dNZdcAsc-U6BKkZ7dhGSWa4xgStS0eNmAu9D1fX0GbJ0yd64mXBoLbquF3x1bHhk97QV_vTU3c-Le4VPDVYwAv3Kz5jeNdm7sCmcPZrC5D2Vu-dfCIWmj6LaRVImGm4aRbIuDoE5Eb-Zac7n9UUvIauSQTO9peJ0jjtBOdF1qjTvuaE3NRT_BXuAhXSW0cRw",
    "access_token_web": "eyJhbGciOiJQUzI1NiIsImtpZCI6IkU1N1lkcnVIcGxBanUyY05vMURvckgzajI3QnU1LXNfT1A1UHdQaWhuNU0ifQ.eyJhcHBfaWQiOjQsImF1ZCI6ImZyLmNvcmUuYXBpLnZpbnRlZC5jb20iLCJjbGllbnRfaWQiOiJ3ZWIiLCJleHAiOjE3ODExMDY1MzcsImlhdCI6MTc4MTA2MzMzNiwiaXNzIjoidmludGVkLWlhbS1zZXJ2aWNlIiwicHVycG9zZSI6ImFjY2VzcyIsInNjb3BlIjoicHVibGljIiwic2lkIjoiZDIwNDg2ODctMTc4MTA2MzMzNiJ9.UYS6YpBikV7KnMKLJPqFS8Bq4diJ3SK5oUueCSHJejLW8tPhRvFtdazSv7jyZTXhRcnBk9cGkJgnoGVWuFGRNAxwgJPvjLWuAqp1UWzXnDdH683YmDB17C180578NbC49i3UEFARb12BYZYrIaEBnyQiD2pzUC26JDMkXM0pArse77Yy2pMhpCK6-SUgtqomOYeve-GqC7G31Y0qLmvJdUBiwCUli5D4J7co_xcXKKEyXsn3UfzrPvcI2bTC7i5yIRVzJxbmL-tUY3SbO7YyqNE257zDzG9mbYXg685VnayhAe5aBIBixu2twgtRA6atiByQLZ-Qr1BjTkS3Phc3Ug",
    "consent_version": "eu",
    "viewport_size": "1920",
    "cf_clearance": "NrL9cIuEgVjBdaYJ8VG6hWQBpzkrPOtL2cCdeikJa8E-1781063341-1.2.1.1-UO7MrIReVZcUysZ_yb5yeD8EoBib8eCeLGXXBV.c6oevSZazTIqZivDbMbJ2tNt2W8JkcEjSlf2AtLKdH2xZ4UbTtQCJkA1SJGdb4KPKL38ijeg8PlsaSrVJMXVz3D6uJf85cjkqt31UXMU_SdZbdB2y9rID.LD..p0AMjhLSakaHJ8XO2mNLqbTCK4kp_.9CVg.Kx_xSe8IDqIX_bP6IwG_9rNfgLOlbhCvauENHSAvfja_gZKW_8NPSDdJHmHI2j02ZOr9tDhJ3p8tGhNCvQL.A013l.57mRxXkedNYaBTYG7bJublyXDXxbDxATiowDap.en2ImmUR5PJpu.JVg",
    "__cf_bm": "8_QKGyIC_VNkbSc7Ot.2ouO2FwztIrY0P.qyYIRQwTo-1781063341.2634256-1.0.1.1-HqKc4STaTzZX5UNabe.VAHEsTn.WF4VFhd12m6bVv2z65Bnl9aXOi_MT_PSUDWT6WEErBNQRF2rO4Wbh9BiXmfkT_sp41DTsjbj8NUulndcoAR_nf4FNscRpyLH1wDDmfweSNOaVgz8Mo7g5ISnc6A",
    "domain_selected": "true",
    "OptanonAlertBoxClosed": "2026-06-10T03:48:22.220Z",
    "OptanonConsent": "isGpcEnabled=0&datestamp=Tue+Jun+09+2026+23%3A48%3A22+GMT-0400+(Eastern+Daylight+Time)&version=202602.1.0&browserGpcFlag=0&isIABGlobal=false&consentId=679d17bd-c565-464c-be05-abd79b776ce8&isAnonUser=1&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0004%3A1%2CC0002%3A1%2CSPD_BG%3A1%2CC0003%3A1%2CC0035%3A1",
    "_vinted_fr_session": "S252NElIZEhqWDJsK09GeXRpOWhyUXRTTHJmVElOY09kdTY2aEFzOTNpRXFiS08yMWhtQVEveitVZUJObDBzTkc1djBKN21OendZZ09QMDAzcUNRMk1Nalo3aVJSNW5aSDdMRjdZeUkzbU9EU3Y0eGxFRWkvbzRJbklIV1FlWTFFTlpVRVNDN0plaEE3bkRWdVJ4NDQzYXdycmZOWS82V1BsZFcxUnYxd09OMnZoZEpDSTdaN2RQdk5WYUkySVhQdEkxVHB1M2F2YW4vZ3YxVHdsMER4Q3JON0FLdTEvMVhJUEp6a3l5Wm01S0krSVBYSzhzUk5WeUNpTEpDZHVPWS0teG13WW1Bemk0YzY5TW9xU2d0QzgvQT09--582f98b93390222ae1e9483778c9aa48af53ca16",
}


def parse_ua(ua: str):
    m = re.search(r'Chrome/(\d+)', ua)
    version = m.group(1) if m else "130"
    if "Macintosh" in ua or "Mac OS X" in ua:
        platform = "macOS"
    elif "Linux" in ua and "Android" not in ua:
        platform = "Linux"
    else:
        platform = "Windows"
    return version, platform


def build_headers(ua):
    version, platform = parse_ua(ua)
    sec_ch_ua = f'"Chromium";v="{version}", "Google Chrome";v="{version}", "Not/A)Brand";v="99"'
    return {
        "sec-ch-ua-platform": f'"{platform}"',
        "x-csrf-token": "75f6c9fa-dc8e-4e52-a000-e09dd4084b3e",
        "accept-language": "en-us-fr",
        "sec-ch-ua": sec_ch_ua,
        "sec-ch-ua-mobile": "?0",
        "user-agent": ua,
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "locale": "en-US",
        "origin": "https://www.vinted.com",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": TARGET_URL,
        "accept-encoding": "gzip, deflate, br, zstd",
        "priority": "u=1, i",
    }


def main():
    # Step 1: riskbypass custom_task → datadome (with DD challenge pass)
    print("=== Step 1: RiskBypass Custom Task (datadome + DD challenge) ===")
    result = client.run_task({
        "task_type": "custom_task",
        "proxy": PROXY,
        "target_url": TARGET_URL,
    }, timeout=120)

    if not result:
        print("[-] Custom task failed")
        return

    datadome = result.get("datadome")
    ua = result.get("ua")
    print(f"datadome: {datadome[:60] if datadome else 'N/A'}...")
    print(f"ua: {ua}")

    if not datadome:
        print("[-] No datadome cookie")
        return

    # Step 2: OAuth via tls_client with upgraded datadome
    print("\n=== Step 2: OAuth via tls_client ===")
    cookies = {**COOKIES_BASE, "datadome": datadome}
    session = tls_client.Session(
        client_identifier="chrome_120",
        random_tls_extension_order=True,
        header_order=HEADER_ORDER,
    )
    r = session.post(
        OAUTH_URL,
        headers=build_headers(ua),
        cookies=cookies,
        json=OAUTH_PARAMS,
        proxy=PROXY,
    )
    print(f"HTTP {r.status_code}")
    print(f"Body: {r.text[:500]}")

    if r.status_code == 200:
        print("\n[+] OAuth OK")
    elif r.status_code == 401:
        print("\n[+] Datadome passed (401 = wrong credentials)")
    elif r.status_code == 403:
        print("\n[!] 403 — still blocked")
    else:
        print(f"\n[-] HTTP {r.status_code}")


if __name__ == "__main__":
    main()
