# -*- coding: utf-8 -*-
# Scheels login demo (Kasada) by riskbypass
# Deps: pip install riskbypass
import json, random
from riskbypass import RiskByPassClient

BASE_URL = "https://riskbypass.com"
TOKEN    = "your token"
TIMEOUT  = 60
PROXY    = "http://xxxxxxxx:xxxxxxxxx@xxx.xxx.xx.xxx:xxxx"

client = RiskByPassClient(token=TOKEN, base_url=BASE_URL)

KASADA_JS_DOMAIN = "apihub.scheels.com"
TARGET_URL = "https://www.scheels.com/"
EMAIL = "sadasd13232@asdsa.com"
PASSWORD = "sadasdasdas2."


def task():
    # ====== Step 1: Get Kasada tokens via RiskByPass ======
    print("[1] Get kasada tokens ...")
    payload = {
        "task_type": "kasada",
        "proxy": PROXY,
        "target_url": TARGET_URL,
        "kasada_js_domain": KASADA_JS_DOMAIN,
        "protected_api_domain": KASADA_JS_DOMAIN
    }
    result = client.run_task(payload, timeout=TIMEOUT)
    if not result:
        print("[-] Kasada task failed")
        return
    print(f"    x-kpsdk-ct = {result['x-kpsdk-ct'][:60]}...")

    kpsdk_ct = result["x-kpsdk-ct"]
    kpsdk_cd = result.get("x-kpsdk-cd", "")
    ua = result.get("ua", "")

    # ====== Step 2: Get kasada_cd answer ======
    print("[2] Get kasada_cd ...")
    cd_payload = {
        "task_type": "kasada_cd",
        "ct": kpsdk_ct,
        "st": result.get("x-kpsdk-st", ""),
        "fc": result.get("x-kpsdk-fc", ""),
        "s": "b5fd12002cb1f49362eac17a71b42911d23b5d00641c70e1e4b4050c46187a23",
    }
    kpsdk_cd = client.run_task(cd_payload, timeout=TIMEOUT)

    # ====== Step 3: Send login request ======
    print("[3] Send login request ...")

    headers = {
        "accept": "application/json",
        "accept-language": "en",
        "cache-control": "no-cache",
        "commercetools-frontend-extension-version": '"5b5c554"',
        "content-type": "application/json",
        "frontastic-currency": "USD",
        "frontastic-locale": "en_US",
        "origin": "https://www.scheels.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.scheels.com/",
        "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": ua or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        "x-frontastic-access-token": "APIKEY",
        "x-kpsdk-ct": kpsdk_ct,
        "x-kpsdk-cd": kpsdk_cd,
        "x-kpsdk-v": "j-1.2.430",
    }

    resp = client.tls_post(
        "https://apihub.scheels.com/frontastic/action/account/login",
        headers=headers,
        json={"email": EMAIL, "password": PASSWORD},
        proxies={"https": PROXY},
    )

    print(f"    status = {resp.status_code}")
    print(f"    body = {resp.text[:500]}")


if __name__ == "__main__":
    task()
