# -*- coding: utf-8 -*-
# 由 RiskByPass 面板自动生成
# 依赖: pip install requests
import requests, time, json, sys

BASE_URL = "https://riskbypass.com"  # api端口地址
TOKEN    = "Your Token"    # 访问令牌（作为 x-api-key 发送）
TIMEOUT  = 60                         # 超时时间（秒）
PROXY = "http://username:password@ip:port"

def run_task():
    # 任务 JSON
    payload = {
        "task_type": "shape",
        "proxy": PROXY,
        "target_url": "https://www.pokemoncenter-online.com/login/",
        "target_api": "https://www.pokemoncenter-online.com/on/demandware.store/Sites-POL-Site/ja_JP/Account-SubmitConfirmationEmail",
        "shape_js_url": "https://www.pokemoncenter-online.com/larkbileomet.js?single",
        "title": "ログイン｜【公式】ポケモンセンターオンライン",
        "method": "POST"
    }
    
    session = requests.Session()
    headers = {"Content-Type": "application/json", "x-api-key": TOKEN}

    print("开始提交任务…")

    try:
        resp = session.post(f"{BASE_URL}/task/submit", headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print("提交请求异常：", repr(e))
        return

    if not data.get("ok"):
        print("提交失败：", data)
        return

    task_id = data.get("task_id")
    if not task_id:
        print("响应中没有 task_id：", data)
        return

    print("已提交，task_id =", task_id)
    
    start_time = time.time()

    while True:
        if time.time() - start_time > TIMEOUT:
            print("超时时间（秒）")
            return
        try:
            r = session.get(f"{BASE_URL}/task/result/{task_id}", headers={"Cache-Control":"no-cache"}, timeout=30)
            r.raise_for_status()
            j = r.json()
        except Exception as e:
            print("轮询异常：", repr(e))
            time.sleep(1)
            continue

        st = j.get("status", "UNKNOWN")
        print("状态：", st)

        if st in ("RUNNING", "QUEUED"):
            time.sleep(1)
            continue

        if st == "SUCCESS":
            print("成功，结果：", json.dumps(j.get("result"), ensure_ascii=False, indent=4))
            return j.get("result")
        elif st == "FAILED":
            print("任务失败：", j.get("error", j))
            return
        elif st == "NOT_FOUND":
            print("未找到任务：可能 task_id 无效或已回收")
            return
        else:
            print("未知响应：", j)
            return

def pokemoncenter_test_online():
    from curl_cffi import requests as c_requests

    resp_headers =  run_task()
    print(resp_headers)

    cookies = {
        'dwanonymous_d9546c4257b7dca3cb860459ce2a1b5e': 'bcUykbOgfdaXqVWRtMHXK49Tqk',
        'gig_bootstrap_4_PlmTwFRPUWmTpGqjm31WOQ': 'id_ver4',
        'hoPvmDpa': 'A1hW-B-bAQAA_jCmCwZe6OjgSUXTb56eR9OOBTaMoTZHNM_xSC540vg9KV5EAVm5UK-ucl6ZwH8AAEB3AAAAAA|1|0|1c12cc3f233e77e63eeea66ec86e4310829fd8b9',
        'ktlvDW7IG5ClOcxYTbmY': 'a',
        '_ga': 'GA1.1.516125900.1765767935',
        '__cq_uuid': 'bcUykbOgfdaXqVWRtMHXK49Tqk',
        '__cq_seg': '0~0.00!1~0.00!2~0.00!3~0.00!4~0.00!5~0.00!6~0.00!7~0.00!8~0.00!9~0.00',
        '_fbp': 'fb.1.1765767937215.743283277482479252',
        '_gcl_au': '1.1.1684314501.1765767916.955200776.1765767960.1765767964',
        'dwac_932979fa30d640199e2bf9e27a': 'U26AdDCA7XqdB7dLQHKdQyQDB3hwM1eG8-o%3D|dw-only|||JPY|false|Asia%2FTokyo|true',
        'cqcid': 'bcUykbOgfdaXqVWRtMHXK49Tqk',
        'cquid': '||',
        'sid': 'U26AdDCA7XqdB7dLQHKdQyQDB3hwM1eG8-o',
        '__cq_dnt': '0',
        'dw_dnt': '0',
        'dwsid': 'wPnyNxewh5_IHtOBykEaFbeUdTtXAz1jpvN1VABwRITuLHZP9bP37QxzfCVePNAd5TL-3W_dALlp24pN3tRBdg==',
        '_ga_RT7LY1DC2Q': 'GS2.1.s1765815378$o3$g1$t1765815379$j59$l0$h1042232765',
        '_ga_WZVZ5W36T7': 'GS2.1.s1765815378$o3$g1$t1765815379$j59$l0$h813436566',
    }

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'ksl6nwtyby-a': resp_headers.get('KsL6nWTYBY-a') or resp_headers.get('ksl6nwtyby-a'),
        # 'ksl6nwtyby-a0': resp_headers.get('KsL6nWTYBY-a0') or resp_headers.get('ksl6nwtyby-a0'),
        'ksl6nwtyby-b': resp_headers.get('KsL6nWTYBY-b') or resp_headers.get('ksl6nwtyby-b'),
        'ksl6nwtyby-c': resp_headers.get('KsL6nWTYBY-c') or resp_headers.get('ksl6nwtyby-a'),
        'ksl6nwtyby-d': resp_headers.get('KsL6nWTYBY-d') or resp_headers.get('ksl6nwtyby-d'),
        'ksl6nwtyby-f': resp_headers.get('KsL6nWTYBY-f') or resp_headers.get('ksl6nwtyby-f'),
        'ksl6nwtyby-z': resp_headers.get('KsL6nWTYBY-z') or resp_headers.get('ksl6nwtyby-z'),
        'origin': 'https://www.pokemoncenter-online.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.pokemoncenter-online.com/login/',
        'sec-ch-ua': resp_headers.get('sec-ch-ua'),
        'sec-ch-ua-mobile': resp_headers.get('sec-ch-ua-mobile'),
        'sec-ch-ua-platform': resp_headers.get('sec-ch-ua-platform'),
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': resp_headers.get('User-Agent') or resp_headers.get('user-agent'),
        'x-requested-with': 'XMLHttpRequest',
    }

    # headers.update(resp_headers)
    ck_str = resp_headers.get('Cookie')

    ck_dict = {}
    for ck in ck_str.split(';'):
        k, v = ck.strip().split('=', maxsplit=1)
        ck_dict[k] = v

    cookies.update(ck_dict)

    params = {
        'rurl': '1',
    }

    data = {
        'dwfrm_profile_confirmationEmail_email': 'aclirc11345@gmail.com',
        'csrf_token': 'hyEEJtj5dkqSH0dJ-PFRebsIsAWQNtaKXO33DzUCRWsMbwEnUMtNsm_w9agkEgovnCzSE1QuKw24A2uym4IhZvPnhmyqh2y3fn8m2pgFj98SaYcoJmuU4DiV1KdH7cl3cUisICS3-Zx_WfOMGYs-JWbzsPCGuKCFgPaifsRb9qU0aVUAQPY=',
    }

    from primp import Client

    c_requests = Client(proxy=PROXY, impersonate='chrome_133')

    response = c_requests.post(
        'https://www.pokemoncenter-online.com/on/demandware.store/Sites-POL-Site/ja_JP/Account-SubmitConfirmationEmail',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
    )

    print(response.text)
    print(response.status_code)

if __name__ == "__main__":
    pokemoncenter_test_online()