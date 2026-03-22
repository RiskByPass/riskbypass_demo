from riskbypass import RiskByPassClient

# -*- coding: utf-8 -*-
# 由 RiskByPass 面板自动生成
# 依赖: pip install riskbypass
import random
from riskbypass import RiskByPassClient

BASE_URL = "https://riskbypass.com"  # api端口地址
TOKEN    = "your token"    # 访问令牌（作为 x-api-key 发送）
TIMEOUT  = 120                         # 任务最大执行时间（秒）, 超出此时间将抛出异常
PROXY = f"http://xxxxxx__cr.us:xxxxxx@gw.dataimpulse.com:{random.randint(10000, 20000)}"

client = RiskByPassClient(token=TOKEN)

headers = {
    ":method": "GET",
    ":authority": "www.arrow.com",
    ":path": "/en/products/verdin-i-mx95-evaluation-kit/toradex-ag.html",
    ":scheme": "https",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Google Chrome\";v=\"146\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "sec-fetch-site": "none",
    "sec-fetch-mode": "navigate",
    "sec-fetch-user": "?1",
    "sec-fetch-dest": "document",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en",
    "priority": "u=0, i"
}

response = client.tls_get('https://www.arrow.com/en/products/verdin-i-mx95-evaluation-kit/toradex-ag.html', headers=headers, proxies={'https':PROXY})
print(response.text)
print(response.status_code)


cookies = {}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://www.arrow.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.arrow.com/en/search-result.html?keyword=ad&currPage=1',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
}

params = {
    'countryCode': 'US',
    'currency': 'USD',
    'lang': 'en',
}

json_data = {
    'pageSize': '',
    'currentPage': '1',
    'category': '',
    'manufacturer': [],
    'searchTerm': 'ad',
    'sort': '',
    'sortDirection': '',
    'filters': [],
}

response = client.tls_post(
    'https://www.arrow.com/experienceservices/search/',
    params=params,
    cookies=cookies,
    headers=headers,
    json=json_data,
    proxies={'https':PROXY}
)
print(response.text)
print(response.status_code)