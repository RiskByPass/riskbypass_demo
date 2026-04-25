# -*- coding: utf-8 -*-
# Footlocker France — Add to Cart (Kasada-protected)
# Deps: pip install requests curl_cffi
import requests, time, json, random
from curl_cffi import requests as c_requests

BASE_URL = "https://riskbypass.com"
TOKEN    = "your token"
TIMEOUT  = 60
PROXY    = "http://username:password@host:port"

def get_ct():
    payload = {
        "task_type": "kasada",
        "proxy": PROXY,
        "target_url": "https://www.footlocker.fr/fr/product/nike-x-fff-air-max-tuned-1-homme-chaussures/314218233204.html",
        "protected_api_domain": "www.footlocker.fr",
        "kasada_js_domain": "www.footlocker.fr",
    }

    session = requests.Session()
    headers = {"Content-Type": "application/json", "x-api-key": TOKEN}

    print("Submitting CT task…")

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
            print("Timeout")
            return
        try:
            r = session.get(f"{BASE_URL}/task/result/{task_id}", headers={"Cache-Control": "no-cache"}, timeout=30)
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
            print("CT SUCCESS:", json.dumps(j.get("result"), ensure_ascii=False, indent=4))
            return j.get("result")
        elif st == "FAILED":
            print("FAILED:", j.get("error", j))
            return
        elif st == "NOT_FOUND":
            print("NOT_FOUND: maybe invalid or recycled task_id")
            return
        else:
            print("UNKNOWN:", j)
            return

def get_cd(ct, st, fc, s):
    payload = {
        "task_type": "kasada_cd",
        "ct": ct,
        "st": st,
        "fc": fc,
        "s": s,
    }

    session = requests.Session()
    headers = {"Content-Type": "application/json", "x-api-key": TOKEN}

    print("Submitting CD task…")

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
            print("Timeout")
            return
        try:
            r = session.get(f"{BASE_URL}/task/result/{task_id}", headers={"Cache-Control": "no-cache"}, timeout=30)
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
            print("CD SUCCESS:", json.dumps(j.get("result"), ensure_ascii=False, indent=4))
            return j.get("result")
        elif st == "FAILED":
            print("FAILED:", j.get("error", j))
            return
        elif st == "NOT_FOUND":
            print("NOT_FOUND: maybe invalid or recycled task_id")
            return
        else:
            print("UNKNOWN:", j)
            return


if __name__ == "__main__":
    FC = "eyJkeW5hbWljQ29uZmlnIjp7ImZyb250ZW5kIjp7ImNyeXB0b0NoYWxsZW5nZSI6eyJjdXJyZW50UGFyYW1ldGVycyI6eyJkaWZmaWN1bHR5Ijo3NSwic3ViY2hhbGxlbmdlQ291bnQiOjQsInNlZWRTdWZmaXgiOiJoaS10aGVyZSEifX19fX0="
    S  = "d49a6b7bf59bb6f5ff2a17caae757f01bc7f5509551e2b34fa641922ca147525"

    kasada_args = get_ct()
    if not kasada_args:
        raise Exception("Failed to get CT")

    ct = kasada_args['x-kpsdk-ct']
    st = kasada_args['x-kpsdk-st']
    v  = kasada_args['x-kpsdk-v']
    h  = kasada_args.get('x-kpsdk-h') or ''
    user_agent = kasada_args['user-agent']
    sec_ch_ua = kasada_args['sec-ch-ua']
    sec_ch_ua_platform = kasada_args['sec-ch-ua-platform']

    cd = get_cd(ct=ct, st=st, fc=FC, s=S)
    if not cd:
        raise Exception("Failed to get CD")

    cookies = {
        'ak_bmsc_flfr-ssn': ct,
        'ak_bmsc_flfr': ct,
        'JSESSIONID': 'your-jsessionid',
        'ZGWID': 'your-zgwid',
    }

    headers = {
        'accept': 'application/json',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.footlocker.fr',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.footlocker.fr/fr/product/nike-x-fff-air-max-tuned-1-homme-chaussures/314218233204.html',
        'sec-ch-ua': sec_ch_ua,
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': sec_ch_ua_platform,
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': user_agent,
        'x-api-lang': 'fr-FR',
        'x-csrf-token': 'b65741ed-498a-4993-a911-ebce0469bffa',
        'x-fl-request-id': '485cd910-0236-11f1-b540-cf0d6df02ecc',
        'x-kpsdk-cd': cd,
        'x-kpsdk-ct': ct,
        'x-kpsdk-h': h,
        'x-kpsdk-v': v,
    }

    json_data = {
        'size': '43',
        'sku': '314218233204',
        'productQuantity': 1,
        'fulfillmentMode': 'SHIP',
        'sizeGroup': 'eu',
        'responseFormat': 'AllItems',
    }

    for i in range(10):
        print(f'\n--- Request {i + 1} ---')
        response = c_requests.post(
            'https://www.footlocker.fr/zgw/carts/co-cart-aggregation-service/site/flfr/cart/cartItems/addCartItem',
            cookies=cookies,
            headers=headers,
            json=json_data,
            proxies={'http': PROXY, 'https': PROXY},
            impersonate='chrome136',
        )
        print(f'Status: {response.status_code}')
        print(response.text[:500])

        next_ct = dict(response.cookies).get('KP_UIDz')
        if next_ct:
            ct = next_ct
            headers['x-kpsdk-ct'] = ct
            cookies['ak_bmsc_flfr-ssn'] = ct
            cookies['ak_bmsc_flfr'] = ct

        cd = get_cd(ct=ct, st=st, fc=FC, s=S)
        if cd:
            headers['x-kpsdk-cd'] = cd
