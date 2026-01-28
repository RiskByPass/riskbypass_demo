import json
import re
import base64
import requests
import time
import random
from urllib.parse import urlencode
from json import dumps as json_dumps

# RiskByPass Configuration
BASE_URL = "https://riskbypass.com"
TOKEN = "your token"
TIMEOUT = 60
PROXY = "http://username:password@host:port" # sticky proxy

class MyResponse:
    def __init__(self, response_dict):
        # 将字典转换为响应对象
        self.body = base64.b64decode(response_dict.get('body_base64').encode())
        self.content = self.body
        self.cookies = response_dict.get('cookies', {})
        self.elapsed = response_dict.get('elapsed', 0)
        self.error = response_dict.get('error', None)
        self.headers = response_dict.get('headers', {})
        self.ok = response_dict.get('ok', False)
        self.reason = response_dict.get('reason', '')
        self.status_code = response_dict.get('status_code', 0)
        self.text = response_dict.get('text', '')
        self.url = response_dict.get('url', '')
    
    def json(self):
        return json.loads(self.body)

def run_riskbypass_task(payload):
    """Execute RiskByPass Task"""
    session = requests.Session()
    headers = {"Content-Type": "application/json", "x-api-key": TOKEN}

    print("Submitting RiskByPass task...")

    try:
        resp = session.post(f"{BASE_URL}/task/submit", headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print("Request submission exception:", repr(e))
        return None

    if not data.get("ok"):
        print("Submission failed:", data)
        return None

    task_id = data.get("task_id")
    if not task_id:
        print("No task_id in response:", data)
        return None

    print("Submitted, task_id =", task_id)

    start_time = time.time()

    while True:
        if time.time() - start_time > TIMEOUT:
            print("Task timeout")
            return None
        try:
            r = session.get(f"{BASE_URL}/task/result/{task_id}", headers={"Cache-Control": "no-cache"}, timeout=30)
            r.raise_for_status()
            j = r.json()
        except Exception as e:
            print("Polling exception:", repr(e))
            time.sleep(1)
            continue

        st = j.get("status", "UNKNOWN")
        print("Task status:", st)

        if st in ("RUNNING", "QUEUED"):
            time.sleep(1)
            continue

        if st == "SUCCESS":
            result = j.get("result", {})
            print("RiskByPass task successful")
            return result
        elif st == "FAILED":
            print("Task failed:", j.get("error", j))
            return None
        elif st == "NOT_FOUND":
            print("Task not found: possibly invalid task_id or recycled")
            return None
        else:
            print("Unknown response:", j)
            return None

def tls_forward(url, method="GET", headers={}, json={}, data='', cookies={}, proxy=None, timeout=30, proxies={}):
    use_proxy = proxies.get('all') or proxies.get('https') or proxy
    if json:
        data = json_dumps(json, separators=(', ', ':'), ensure_ascii=False)
    if type(data) == str:
        body_base64 = base64.b64encode(data.encode()).decode()
    elif type(data) == bytes:
        body_base64 = base64.b64encode(data).decode()
    elif type(data) == dict:
        network_data = urlencode(data)
        body_base64 = base64.b64encode(network_data.encode()).decode()
    else:
        body_base64 = None
    payload = {
        "task_type": "tls_forward",
        "proxy": use_proxy,
        "url": url,
        "method": method,
        "headers": headers,
        "body_base64": body_base64,
        "cookies_dict": cookies,
        "timeout": timeout
    }
    if headers.get('user-agent'):
        payload['user_agent'] = headers.get('user-agent')
    result = run_riskbypass_task(payload)
    if not result:
        raise Exception('TLS Forward Error')
    else:
        return MyResponse(result)

def tls_get(url, headers={}, json={}, data='', cookies={}, proxy=None, timeout=30, proxies={}, params={}):
    if isinstance(params, dict):
        urlparams = urlencode(params)
        url += '?' + urlparams
    return tls_forward(url, 'GET', headers, json, data, cookies, proxy, timeout, proxies)


def tls_post(url, headers={}, json={}, data='', cookies={}, proxy=None, timeout=30, proxies={}, params={}):
    if isinstance(params, dict) and params:
        urlparams = urlencode(params)
        url += '?' + urlparams
    return tls_forward(url, 'POST', headers, json, data, cookies, proxy, timeout, proxies)

if __name__ == "__main__":
    # Task JSON payload
    payload = {
        "task_type": "cloudflare_waf",
        "proxy": PROXY,
        "target_url": "https://wollongong.jinriaozhou.com/content-1026580752046006",
        "target_method": "GET"
    }
    result = run_riskbypass_task(payload)
    if not result:
        cookies = {}
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36'
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'referer': 'https://wollongong.jinriaozhou.com/?__cf_chl_tk=_s_vW6YvBXUaccPGTGuW0_DMLjGFjNX6GPnL9SJpgKQ-1769571627-1.0.1.1-9QwJsAPaCMysjAWnmjXx8ibBq9h4_dLBUNHUB7NpPfk',
            'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"144.0.7559.97"',
            'sec-ch-ua-full-version-list': '"Not(A:Brand";v="8.0.0.0", "Chromium";v="144.0.7559.97", "Google Chrome";v="144.0.7559.97"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': ua,
        }
        response = tls_get('https://wollongong.jinriaozhou.com/content-1026580752046006', cookies=cookies, headers=headers, proxies={'https':PROXY})
        print(response.text)
        print(response.status_code)
    else:
        cookies = result.get("cookies")
        ua = result.get('ua')
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'referer': 'https://wollongong.jinriaozhou.com/?__cf_chl_tk=_s_vW6YvBXUaccPGTGuW0_DMLjGFjNX6GPnL9SJpgKQ-1769571627-1.0.1.1-9QwJsAPaCMysjAWnmjXx8ibBq9h4_dLBUNHUB7NpPfk',
            'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"144.0.7559.97"',
            'sec-ch-ua-full-version-list': '"Not(A:Brand";v="8.0.0.0", "Chromium";v="144.0.7559.97", "Google Chrome";v="144.0.7559.97"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': ua,
        }
        from tls_client import Session
        session = Session(random_tls_extension_order=True)
        response = session.get('https://wollongong.jinriaozhou.com/content-1026580752046006', cookies=cookies, headers=headers, proxy={'https':PROXY})
        print(response.text)
        print(response.status_code)