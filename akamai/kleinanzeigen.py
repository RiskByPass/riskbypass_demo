# -*- coding: utf-8 -*-
# 由 RiskByPass 面板自动生成
# 依赖: pip install riskbypass
import random, re
from riskbypass import RiskByPassClient
from requests_go import Session
from requests_go.tls_config import TLS_CHROME_LATEST

BASE_URL = "https://riskbypass.com"  # api端口地址
TOKEN    = "your token"    # 访问令牌（作为 x-api-key 发送）
TIMEOUT  = 120                         # 任务最大执行时间（秒）, 超出此时间将抛出异常
PROXY = f"http://xxxxxxxxxx__cr.de:xxxxxxxxxxx@gw.dataimpulse.com:{random.randint(10000, 20000)}"

email = 'asdmjkndjsad@smd.com'
password = 'sandjsn2131.'

client = RiskByPassClient(token=TOKEN, base_url=BASE_URL)

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
}

session = Session()
session.tls_config = TLS_CHROME_LATEST

response = session.get('https://www.kleinanzeigen.de/m-einloggen.html', headers=headers, proxies={'https': PROXY})
init_cookies = session.cookies.get_dict()
print('Step1: Get init_cookies over.')
akamai_payload = {
  "task_type": "akamai",
  "proxy": "http://username:password@ip:port",
  "target_url": "https://login.kleinanzeigen.de/u/login/identifier?state=hKFo2SBsTGpWNHVaMHZya3RuQmZHMEEzTV9kUExPYlNBYUF1daFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIG5UdDd3SUM3dEx0V3A2bEQwcFlOTHM3TzBmZTJ2UENYo2NpZNkgYU9xNzRDbTVmVUJvTTFKaWZIVGhIbFoySkhYbFZVQ3E",
  "akamai_js_url": "https://login.kleinanzeigen.de/t3fOH/TK/uyz/BX/EX3PIRxU/SEt70zwXXSphp8/MngDAQ/X0Bn/DV8pAFUB",
  "page_fp": "424541475255414d4b4546454b5d5655405a425f4245434752555d505f5e43454350"
}
akamai_payload['proxy'] = PROXY
akamai_payload['init_cookies'] = init_cookies
akamai_payload['akamai_js_url'] = 'https://login.kleinanzeigen.de' + re.findall(r'<script type="text/javascript" nonce=".*?" src="(.*?)">', response.text)[-1]
result = client.run_task(akamai_payload, timeout=TIMEOUT)
print('Step2: Get akamai cookies over.')
akamai_cookies = result.get('cookies_dict')
ua = result.get('ua')

print(akamai_cookies['_abck'])
session.cookies.update(akamai_cookies)

state = response.url.split('=')[-1]

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://login.kleinanzeigen.de',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': response.url,
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
}

params = {
    'state': state,
}

data = {
    'state': state,
    'username': email,
    'js-available': 'true',
    'webauthn-available': 'true',
    'is-brave': 'false',
    'webauthn-platform-available': 'true',
}

response = session.post(
    'https://login.kleinanzeigen.de/u/login/identifier',
    params=params,
    headers=headers,
    data=data,
    proxies={'https': PROXY}
)

print('identifier: ', response.status_code, response.url)

params = {
    'state': state,
}

data = {
    'state': state,
    'username': email,
    'password': password,
    'ulp-wenkse-session-id': 'e550bfa1-434e-458e-8e8c-26778fc2449c',
}

response = session.post(
    'https://login.kleinanzeigen.de/u/login/password',
    params=params,
    headers=headers,
    data=data,
    proxies={'https': PROXY},
    allow_redirects=True
)

print("password: ", response.status_code, response.url)
print('Email not reg: ', 'Die E-Mail-Adresse ist nicht registriert oder das Passwort ist falsch. Bitte überprüfe deine Eingaben.' in response.text)