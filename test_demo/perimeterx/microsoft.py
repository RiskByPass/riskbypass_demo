import requests
import json

api_key = 'Your API Key' # 你的API密钥/Your API Key, get it from https://riskbypass.com/dashboard
session_id = 'a94cb90c4bdd47a0b047880b441af06c' # 微软注册时iframe的session_id/session_id of iframe when you register on microsoft
proxy = 'http://127.0.0.1:8989' # 代理/Proxy

headers = {
    'content-type': 'application/json',
    'x-api-key': api_key,
}

json_data = {
    'task_type': 'perimeterx-hard',
    'params': {
        'target_url': f'https://iframe.hsprotect.net/index.html?app_id=PXzC5j78di&session_id={session_id}',
        'perimeterx_js_url': 'https://client.hsprotect.net/PXzC5j78di/main.min.js',
        'pxAppId': 'PXzC5j78di',
        'proxy': proxy,
    },
}

proxies = {
    'http': proxy,
    'https': proxy,
}

response = requests.post('https://riskbypass.com/api/task/sync', headers=headers, json=json_data, proxies=proxies)

px_cookie = json.loads(response.json().get('result', {}).get('result'))
print(px_cookie)