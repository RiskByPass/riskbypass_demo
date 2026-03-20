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
PROXY = f"http://xxxxxxxxx__cr.de:xxxxxxxxxx@gw.dataimpulse.com:{random.randint(10000, 20000)}"

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

response = session.get('https://mtacc.mobilelegends.com/v2.1/inapp/login-new', headers=headers, proxies={'https': PROXY})
init_cookies = session.cookies.get_dict()
print('Step1: Get init_cookies over.')
akamai_payload = {
  "task_type": "akamai",
  "proxy": "http://username:password@ip:port",
  "target_url": "https://mtacc.mobilelegends.com/v2.1/inapp/login-new",
  "akamai_js_url": "https://mtacc.mobilelegends.com/uBrLodP2f/BXE/CJh/A0nh3VoN5vZo/hpXuX2XSVpcSJk/R05geBwNCA/ejl8UQU/IFFwB",
  "page_fp": "424543475255404d5e425e4442475242414d435f424543474f485c4c425f4252"
}
akamai_payload['proxy'] = PROXY
akamai_payload['init_cookies'] = init_cookies
akamai_payload['akamai_js_url'] = 'https://mtacc.mobilelegends.com' + re.findall(r'<script type="text/javascript"  src="(.*?)">', response.text)[-1]
result = client.run_task(akamai_payload, timeout=TIMEOUT)
print('Step2: Get akamai cookies over.')
akamai_cookies = result.get('cookies_dict')
ua = result.get('ua')

print(akamai_cookies['_abck'])
session.cookies.update(akamai_cookies)

state = response.url.split('=')[-1]

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://mtacc.mobilelegends.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://mtacc.mobilelegends.com/',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
}

json_data = {
    'op': 'login',
    'sign': 'a3c793772b2769309abcc995a9ca30fb',
    'params': {
        'account': 'asdsadsa@sdmk.com',
        'md5pwd': '122de02cca822111f13366b63c49a8f1',
        'game_token': '',
        'recaptcha_token': '',
        'e_captcha': 'CN31_PA4eaIngr6eAZZnb.2D2CxeEBHbqf9SFCM4Rg9tr2u3QplmQ13YHYvNZSe1FzM1VwR06JvnE.MnsjUWVaYBB2BBnunapJTzhPUNeFgt1n*veUcZ1iAnS3mojYUdcqYa.g63nQtDwyBdTa3eamDQy38e._0LUQbCxiYWdMqvDufxyePitJwG*OdOlivBstydRKNHBnoTyrfcWPqTj4*6iGEi3qbqAjNuN5KirjJI9ojt3iTS._Hd9K39Z6X4HndZ*FArsPjJc.Gb*o1pFLod8V4ArsjxqHT.DcfhA3KpQVM1g2OScxYQ*HiOkMrj6hAZ*zGjUNriZELn69eeauPI*GLG1Nyy4cv2Mn._VKyERQji.zQfPp_WZG9wx_YV1bLYRlxfG0xg*MITjshKpZ0TLCzafBjCrMXMC9.XcUbJiKDSYkXEl3MJAh3hhrfAdkmDi5qQwAUwRgcc1QsPuPd5PNWgy5RKmNe1RIirz6F9niPGmLYFoSCz6ST3CM8nwWLMwrToXPg77_v_i_1',
        'country': '',
    },
    'lang': 'en',
}

response = session.post('https://accountmtapi.mobilelegends.com/', headers=headers, json=json_data, proxies={'https':PROXY})

print('result: ', response.status_code, response.text)
