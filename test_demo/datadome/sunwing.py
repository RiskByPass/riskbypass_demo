import requests
from curl_cffi import request
import json

# Your api key, get it from https://riskbypass.com
api_key = 'Your API Key'
headers = {
    'Content-Type': 'application/json',
    'X-API-Key': api_key,
}

# The website which your need bypass
# 需要过datadome的网站
target_url = 'https://book.sunwing.ca/cgi-bin/results.cgi'
# The datadome custom js url
# datadome主要的js url
datadome_js_url = 'https://js.datadome.co/tags.js'
# datadome js key, you can get it by entering window.ddjskey in F12 console, or by searching for ddjskey in the HTML source code
# datadome js key, 你可以使用F12控制台输入window.ddjskey获得, 或者在html源码中搜索ddjskey获得
ddjskey = 'E812CB49265F3F5AD3331EACED3A5C'
# datadome options, you can get it by entering window.ddoptions in F12 console, or by searching for ddoptions in the HTML source code
# datadome options, 你可以使用F12控制台输入window.ddoptions获得, 或者在html源码中搜索ddoptions获得
ddoptions = json.dumps({"ajaxListenerPath":True})
# proxy, format: https://username:password@ip:port
# 代理, 格式: https://username:password@ip:port
proxy = 'http://127.0.0.1:8989'

json_data = {
  "task_type": "datadome-hard",
  "params": {
    "target_url": target_url,
    "datadome_js_url": datadome_js_url,
    "ddjskey": ddjskey,
    "ddoptions": ddoptions,
    "proxy": proxy
  }
}

response = requests.post('https://riskbypass.com/api/task/sync', headers=headers, json=json_data)
print(response.json())
datadome_cookie = response.json().get('result', {}).get('result')
if not datadome_cookie:
    raise Exception('Unknown error')
else:
    for i in range(10):
        print(f'Request {i+1} times')
        headers = {
            'Accept': '*/*', 
            'Content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', 
            'referer': target_url,
            'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"', 
            'sec-ch-ua-mobile': '?0', 
            'sec-ch-ua-platform': '"Windows"'
        }
        try:
            url = "https://book.sunwing.ca/cgi-bin/results.cgi"
            # sid=c5dad7a7a314e1a529042350a85966c8&gateway_dep=YYZ&engines=S&date_ret=20250605&language=en&date_dep=20250602&dest_dep=LRM&nb_adult=2&code_ag=rds&searchtype=RE&flex=Y&nb_child=0&alias=btd
            data = {
                "sid": "c5dad7a7a314e1a529042350a85966c8",
                "gateway_dep": "YYZ",
                "engines": "S",
                "date_ret": "20250605",
                "language": "en",
                "date_dep": "20250602",
                "dest_dep": "LRM",
                "nb_adult": "2",
                "code_ag": "rds",
                "searchtype": "RE",
                "flex": "Y",
                "nb_child": "0",
                "alias": "btd"
            }
            response = request(method='POST', url=url, headers=headers, impersonate='chrome136', proxies={'https':proxy}, cookies=json.loads(datadome_cookie), data=data)
            print(response.text)
            # with open(f'sunwing_{i+1}.html', 'w', encoding='utf-8') as f:
            #     f.write(response.text)
        except Exception as e:
            print(e)