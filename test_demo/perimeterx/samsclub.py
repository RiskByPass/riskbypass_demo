import requests
import json

api_key = 'Your API Key' # 你的API密钥/Your API Key, get it from https://riskbypass.com/dashboard
proxy = 'http://127.0.0.1:8989' # 代理/Proxy

headers = {
    'content-type': 'application/json',
    'x-api-key': api_key,
}

json_data = {
    'task_type': 'perimeterx-hard',
    'params': {
        "target_url": "https://www.samsclub.com/register", 
        "perimeterx_js_url": "https://www.samsclub.com/px/PXsLC3j22K/init.js", 
        "pxAppId": "PXsLC3j22K", 
        "proxy": proxy,
    },
}

response = requests.post('https://riskbypass.com/api/task/sync', headers=headers, json=json_data)
print(response.json())

px_cookie = json.loads(response.json().get('result', {}).get('result', '{}'))
print(px_cookie)