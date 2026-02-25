# -*- coding: utf-8 -*-
# 由 RiskByPass 面板自动生成
# 依赖: pip install requests
import requests, time, json, random, base64
from urllib.parse import urlencode
from json import dumps as json_dumps
from curl_cffi import requests as c_requests

BASE_URL = "https://riskbypass.com"  # api端口地址
TOKEN = "your token"  # 访问令牌（作为 x-api-key 发送）
TIMEOUT = 60  # 超时时间（秒）
PROXY = f'http://username:password@host:port'
print(PROXY)

def run_task(payload):
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
            r = session.get(f"{BASE_URL}/task/result/{task_id}", headers={"Cache-Control": "no-cache"}, timeout=30)
            r.raise_for_status()
            j = r.json()
        except Exception as e:
            print("轮询异常：", repr(e))
            time.sleep(1)
            continue

        st = j.get("status", "UNKNOWN")
        print("状态：", st)

        if st in ("RUNNING", "QUEUED"):
            time.sleep(5)
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
    result = run_task(payload)
    if not result:
        raise Exception('TLS Forward Error')
    else:
        return RiskbypassResponse(result)

def tls_get(url, headers={}, json={}, data='', cookies={}, proxy=None, timeout=30, proxies={}, params={}):
    if isinstance(params, dict) and params:
        urlparams = urlencode(params)
        url += '?' + urlparams
    return tls_forward(url, 'GET', headers, json, data, cookies, proxy, timeout, proxies)


def tls_post(url, headers={}, json={}, data='', cookies={}, proxy=None, timeout=30, proxies={}, params={}):
    if isinstance(params, dict) and params:
        urlparams = urlencode(params)
        url += '?' + urlparams
    return tls_forward(url, 'POST', headers, json, data, cookies, proxy, timeout, proxies)
    

class RiskbypassResponse:
    def __init__(self, response_dict):
        # 将字典转换为响应对象
        self.body = base64.b64decode(response_dict.get('body_base64').encode())
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


if __name__ == "__main__":
    crawler_session = c_requests.Session(impersonate='firefox135')
    crawler_session.proxies = {
        'http': PROXY,
        'https': PROXY
    }
    random_search_param = random.randint(1, 999999)
    cloudflare_payload = {
        "task_type": "cloudflare_waf",
        "proxy": PROXY,
        "target_url": f"https://www.truepeoplesearch.com/InternalCaptcha?returnUrl=https%3A%2F%2Fwww.truepeoplesearch.com%2Fresults?name={random_search_param}&rrstamp=500",
        "target_method": "GET",
        "special": 'tps'
    }
    cf_results = run_task(cloudflare_payload)
    if not cf_results:
        cf_results = {"cookies": {}}

    cookies = cf_results.get("cookies")
    print(cookies)
    for k, v in cookies.items():
        crawler_session.cookies.set(k, v, domain='.truepeoplesearch.com')

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://www.truepeoplesearch.com/results?name=235648',
        'sec-ch-device-memory': '8',
        'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-full-version-list': '"Not:A-Brand";v="99.0.0.0", "Google Chrome";v="145.0.7632.110", "Chromium";v="145.0.7632.110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    }

    response = tls_get('https://www.truepeoplesearch.com/results?name=RHEA+RHINEHART&citystatezip=44060', headers=headers,
                                proxy=PROXY, cookies=cookies)

    with open('response.html', 'w', encoding='utf8') as f:
        f.write(response.text)


    print(response.status_code)
    print(response.url)
    with open('response.html', 'w', encoding='utf8') as f:
        f.write(response.text)

    
    response2 = tls_get('https://www.truepeoplesearch.com/find/person/p4ul60n4nur98r62u48n', headers=headers,
                                proxy=PROXY, cookies=cookies)
    print(response2.status_code)
    print(response2.url)
    with open('response2.html', 'w', encoding='utf8') as f:
        f.write(response2.text)
