# -*- coding: utf-8 -*-
"""seatgeek — riskbypass API + cycronet verify"""
import re
import time
import cycronet
from riskbypass import RiskByPassClient

BASE_URL = "https://riskbypass.com"
TOKEN = "your_token"
PROXY = "http://user:pass@xxxxxxxxxxx.com:xxxx"
TARGET_URL = "https://seatgeek.com/"
OTPW_URL = "https://seatgeek.com/api/users/otpw?client_id=MTY2MnwxMzgzMzIwMTU4"

client = RiskByPassClient(token=TOKEN, base_url=BASE_URL)


def main():
    print("=== Step 1: solve datadome ===")
    start = time.time()
    result = client.run_task({
        "task_type": "custom_task",
        "proxy": PROXY,
        "target_url": TARGET_URL,
        "custom_event": "seatgeek"
    }, timeout=120)

    datadome = result.get("datadome")
    ua = result.get("ua")
    elapsed = time.time() - start
    print(f"耗时: {elapsed:.1f}s")
    print(f"ua: {ua}")
    print(f"datadome: {datadome[:80] if datadome else 'N/A'}...")

    if not datadome:
        print("[-] Failed — no datadome cookie")
        return

    # Step 2: cycronet
    print("\n=== Step 2: cycronet otpw ===")
    m = re.search(r'Chrome/(\d+)', ua)
    ver = m.group(1) if m else "144"
    plat = "macOS" if "Mac" in ua else ("Linux" if "Linux" in ua else "Windows")

    profiles = cycronet.get_tls_profiles()
    tls_id = f"chrome_{ver}" if f"chrome_{ver}" in profiles else "chrome_144"
    session = cycronet.CronetClient(verify=False, proxies={"https": PROXY, "http": PROXY}, chrometls=tls_id)

    cookie_str = f"datadome={datadome}; _ga=1"

    body = "email=asdasdas%40asds.com&otpw_type=code&mode=email&from_navbar=true"
    headers = [
        ("content-length", str(len(body))),
        ("x-sg-sift-session-id", "x"),
        ("sixpack-client-id", "x"),
        ("mparticle-session-id", "X"),
        ("x-sg-user-session-id", "x"),
        ("sec-ch-ua-platform", f'"{plat}"'),
        ("sec-ch-ua", f'"Chromium";v="{ver}", "Google Chrome";v="{ver}", "Not/A)Brand";v="99"'),
        ("sec-ch-ua-mobile", "?0"),
        ("x-sg-locale", "en-US"),
        ("x-sg-currency-code", "USD"),
        ("accept", "application/json, text/plain, */*"),
        ("content-type", "x-www-form-urlencoded"),
        ("user-agent", ua),
        ("x-sg-forter-token", ""),
        ("origin", "https://seatgeek.com"),
        ("sec-fetch-site", "same-origin"),
        ("sec-fetch-mode", "cors"),
        ("sec-fetch-dest", "empty"),
        ("referer", "https://seatgeek.com/"),
        ("accept-encoding", "gzip, deflate, br, zstd"),
        ("accept-language", "en"),
        ("cookie", cookie_str),
    ]

    try:
        resp = session.post(OTPW_URL, headers=headers, data=body)
        total = time.time() - start
        print(f"HTTP {resp.status_code}")
        print(f"Body: {resp.text[:300]}")
        if resp.status_code != 403 and "captcha-delivery.com" not in resp.text:
            print(f"\n[+] OK — Cost time: {total:.1f}s")
        else:
            print("\n[-] Failed — Use datadome slider bypass this captcha and get cookie requests again")
    except Exception as e:
        print(f"[-] cycronet error: {type(e).__name__}: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
