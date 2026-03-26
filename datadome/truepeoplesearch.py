# -*- coding: utf-8 -*-
# 由 RiskByPass 面板自动生成
# 依赖: pip install requests
import random
from riskbypass import RiskByPassClient
from curl_cffi import requests as c_requests

BASE_URL = "https://riskbypass.com"  # api端口地址
TOKEN = "your token"  # 访问令牌（作为 x-api-key 发送）
TIMEOUT = 60  # 超时时间（秒）
PROXY = f'http://xxxxxxxxxxxx__cr.us:xxxxxxxxxxxxxxx@gw.dataimpulse.com:{random.randint(10000, 20000)}'

print(PROXY)

client = RiskByPassClient(token=TOKEN)

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
    cf_results = client.run_task(cloudflare_payload)
    if not cf_results:
        cf_results = {"cookies": {}}

    cookies = cf_results.get("cookies")
    print(cookies)
    ua = cf_results.get('ua', '')
    from pyquery import PyQuery as pq
    if ua:
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
            'user-agent': ua,
        }

        response = client.tls_get('https://www.truepeoplesearch.com/results?name=RHEA+RHINEHART&citystatezip=44060',
                           headers=headers,
                           proxy=PROXY, cookies=cookies)
        title1 = pq(response.text)('title').text().strip()
        print(title1)
        response2 = client.tls_get('https://www.truepeoplesearch.com/find/person/p4ul60n4nur98r62u48n', headers=headers,
                            proxy=PROXY, cookies=cookies)
        title2 = pq(response2.text)('title').text().strip()
        print(title2)