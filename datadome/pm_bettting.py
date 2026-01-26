import requests
import time
import json
import random

BASE_URL = "https://riskbypass.com"  # API base URL
TOKEN    = "your token"    # Access token (sent as x-api-key)
TIMEOUT  = 60                         # Timeout (seconds)
PROXY = f'http://username:password@host:port' # Must be India Proxy


def run_task(payload):
    """
    向RiskByPass提交任务并轮询结果
    
    Args:
        payload: 任务配置字典
        
    Returns:
        dict: 任务结果，失败返回None
    """
    session = requests.Session()
    headers = {
        "Content-Type": "application/json",
        "x-api-key": TOKEN
    }

    print("[*] 提交任务:", payload.get('task_type'))

    try:
        resp = session.post(
            f"{BASE_URL}/task/submit",
            headers=headers,
            json=payload,
            timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print("[!] 提交请求异常:", repr(e))
        return None

    if not data.get("ok"):
        print("[!] 提交失败:", data)
        return None

    task_id = data.get("task_id")
    if not task_id:
        print("[!] 响应中没有 task_id:", data)
        return None

    print(f"[+] 已提交，task_id = {task_id}")

    start_time = time.time()

    while True:
        # 超时检查
        if time.time() - start_time > TIMEOUT:
            print("[!] 任务超时")
            return None

        try:
            r = session.get(
                f"{BASE_URL}/task/result/{task_id}",
                headers={"Cache-Control": "no-cache", "x-api-key": TOKEN},
                timeout=30
            )
            r.raise_for_status()
            j = r.json()
        except Exception as e:
            print("[!] 轮询异常:", repr(e))
            time.sleep(1)
            continue

        st = j.get("status", "UNKNOWN")
        print(f"[*] 状态: {st}")

        if st in ("RUNNING", "QUEUED"):
            time.sleep(1)
            continue

        if st == "SUCCESS":
            result = j.get("result")
            print("[+] 成功:", json.dumps(result, ensure_ascii=False, indent=2))
            return result

        elif st == "FAILED":
            print("[!] 任务失败:", j.get("error", j))
            return None

        elif st == "NOT_FOUND":
            print("[!] 未找到任务")
            return None

        else:
            print("[!] 未知响应:", j)
            return None

from primp import Client

client = Client(impersonate='chrome_133', proxy=PROXY)

cookies = {
    'BETBOOK_LANGUAGE': 'en',
    'bdata': 'true',
    'entrance_url': 'https://pm-betting.com/',
    'dhash': '71c02b0c-3784-4106-a30b-a5580ef3ecde',
    'org': 'direct',
    'org_t': '1769394711349',
    '_gcl_au': '1.1.1262846614.1769394710',
    '_ga': 'GA1.1.766807661.1769394711',
    'fuid': '1.-5315659218856807583',
    'intercom-id-wn76kowe': 'c51ca463-b3e7-430f-9154-2ba3cc1f8fe8',
    'intercom-session-wn76kowe': '',
    'intercom-device-id-wn76kowe': 'f5dd5839-b3f0-432a-8b7f-309010183df7',
    '_sp_ses.63e3': '*',
    '_p_uid': 'uid-31dd226dc.34d93dc21.31202a273',
    '_hjSessionUser_1625208': 'eyJpZCI6IjViYTlhYTg0LTIxODAtNWE4Ny04M2Y3LTg2YWVkZWM2NWYwMCIsImNyZWF0ZWQiOjE3NjkzOTkwMzkzMDcsImV4aXN0aW5nIjpmYWxzZX0=',
    '_hjSession_1625208': 'eyJpZCI6ImUyYWM1YWRiLTNlZWItNDU4NC1hNDI4LTVjZWIxMjVkY2I3YyIsImMiOjE3NjkzOTkwMzkzMDgsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MX0=',
    'registerUrl': 'https://pm-betting.com/en/login',
    '_ga_F6MKFMM2K3': 'GS2.1.s1769399038$o2$g1$t1769399071$j27$l0$h0',
    '_sp_id.63e3': '7d2ed04c-7965-463f-95c0-661581781d97.1769394709.2.1769399072.1769394885.dd6ae04f-116c-40a6-90d1-1aece7dd0079.78a885a9-1edc-4c5d-bb66-f403000a73a1.3734bc31-cc6e-4ade-aea8-5736e5271c3c.1769399038617.25',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9',
    'baggage': 'sentry-environment=prod,sentry-release=2.238.0,sentry-public_key=bca98dae553e4242bbfceeeea05b7d6b,sentry-trace_id=a39ba7262bcb430cb8137d0fc624ef31,sentry-sampled=false,sentry-sample_rand=0.2247376642475366,sentry-sample_rate=0',
    'cache-control': 'no-cache',
    'content-type': 'application/json; charset=UTF-8',
    'origin': 'https://pm-betting.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://pm-betting.com/en/login',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': 'a39ba7262bcb430cb8137d0fc624ef31-9545e74019ce8433-0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'x-channel': 'DESKTOP_AIR_PM',
    'x-clientid': '6b0006a7ac9edb3e73ccbc62e9b53a16',
    'x-fe-module': 'login',
    'x-requested-with': 'XMLHttpRequest',
    'x-response-error': 'true',
    'x-twofa-ver': '2',
}


json_data = {
    'login': '+912132132454',
    'loginType': 'phone',
    'password': 'sadasdwq12.',
    'isPlayerAgree': True,
    'marketingMeta': {
        'mlv': 'v0.6.2',
        'registerURL': 'https://pm-betting.com/en/login',
        'dhash': '71c02b0c-3784-4106-a30b-a5580ef3ecde',
        'entrance_url': 'https://pm-betting.com/',
        'org': 'direct',
        'org_t': '1769394711349',
        'win_tag': 'direct',
        'win_tag_type': 'org',
        'wtl': 'aw',
    },
}

response = client.post('https://pm-betting.com/api/login', cookies=cookies, headers=headers, json=json_data)
print(response.text)
if response.status_code == 403:
    dd_url = response.json().get('url')
    print(dd_url)
    if 'captcha' in dd_url:
        task_type = 'datadome-slider'
    else:
        task_type = 'datadome-device-check'
    payload = {
        "task_type": task_type,
        "proxy": PROXY,
        "target_url": dd_url,
        "target_method": "GET"
    }
    # if 
    result = run_task(payload)
    if not result:
        raise Exception('Failed to submit task')
    cookies['datadome'] = result.get('datadome')
    headers['user-agent'] = result.get('ua')
    client = Client(impersonate='chrome_133', proxy=PROXY)
    response = client.post('https://pm-betting.com/api/login', cookies=cookies, headers=headers, json=json_data)

print(response.text)