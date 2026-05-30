# -*- coding: utf-8 -*-
# Champs Sports — Auth (Kasada-protected)
# Deps: pip install requests curl_cffi
import requests, time, json
from curl_cffi import requests as c_requests

BASE_URL = "https://riskbypass.com"
TOKEN    = "your_token"
TIMEOUT  = 60
PROXY    = "http://user:pass@host:port"

def get_ct():
    payload = {
        "task_type": "kasada",
        "proxy": PROXY,
        "target_url": "https://www.champssports.com/",
        "protected_api_domain": "www.champssports.com",
        "kasada_js_domain": "www.champssports.com",
        "pm": "us"
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
    # FC = base64 encoded crypto challenge config (hardcoded per Kasada deployment)
    # Decoded: {"dynamicConfig":{"frontend":{"cryptoChallenge":{"currentParameters":{"difficulty":75,"subchallengeCount":4,"seedSuffix":"hi-there!"}}}}}
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
        'ak_bmsc_chmps-ssn': ct,
        'ak_bmsc_chmps': ct,
        'JSESSIONID': 'your-jsessionid',
        'ZGWID': 'your-zgwid',
    }

    headers = {
        'accept': 'application/json',
        'accept-language': 'undefined',
        'content-type': 'application/json',
        'origin': 'https://www.champssports.com',
        'priority': 'u=1, i',
        'referer': 'https://www.champssports.com/',
        'sec-ch-ua': sec_ch_ua,
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': sec_ch_ua_platform,
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': user_agent,
        'x-api-lang': 'en-US',
        'x-csrf-token': '06cb2230-1e1a-4060-aa15-a4271fefd47b',
        'x-fl-request-id': '99726da0-5c23-11f1-aa7f-2db9ebc2497b',
        'x-kpsdk-cd': cd,
        'x-kpsdk-ct': ct,
        'x-kpsdk-h': h,
        'x-kpsdk-v': v,
    }

    json_data = {
        'uid': 'test@example.com',
        'password': 'TestPassword123.',
    }

    response = c_requests.post(
        'https://www.champssports.com/zgw/auth',
        cookies=cookies,
        headers=headers,
        json=json_data,
        proxies={'http': PROXY, 'https': PROXY},
        impersonate='chrome136',
    )
    print(f'Status: {response.status_code}')
    print(response.text[:500])

    # Refresh CT from response cookie if present
    next_ct = dict(response.cookies).get('KP_UIDz')
    if next_ct:
        ct = next_ct
        print(f'CT refreshed from KP_UIDz cookie')
