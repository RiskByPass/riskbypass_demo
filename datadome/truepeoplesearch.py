# -*- coding: utf-8 -*-
# 由 RiskByPass 面板自动生成
# 依赖: pip install requests
import requests, time, json, random, string
from curl_cffi import requests as c_requests

BASE_URL = "https://riskbypass.com"  # api端口地址
TOKEN    = "your token"    # 访问令牌（作为 x-api-key 发送）
TIMEOUT  = 60                         # 超时时间（秒）
PROXY = 'http://username:password@host:port'

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

if __name__ == "__main__":
    datadome_payload = {
        "task_type": "datadome-device-check",
        "proxy": PROXY,
        "target_url": "https://www.truepeoplesearch.com/resultphone?phoneno=(213)937-9027",
        "target_method": "GET"
    }
    dd_results = run_task(datadome_payload)
    if not dd_results:
        raise Exception('DataDome绕过失败')

    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    cookies = {
        'datadome': dd_results.get('datadome')
    }
    response = c_requests.get('https://www.truepeoplesearch.com/resultphone?phoneno=(213)937-9027', headers=headers, cookies=cookies, proxy=PROXY, impersonate='chrome136')
    with open('response.html', 'w', encoding='utf8') as f:
        f.write(response.text)

    print(response.status_code)
    print(response.url)