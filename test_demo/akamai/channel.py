import requests

# Your api key, get it from https://riskbypass.com
api_key = 'You api key'
headers = {
    'Content-Type': 'application/json',
    'X-API-Key': api_key,
}

# The akamai js url
# akamai的js url
akamai_js_url = 'https://www.chanel.com/8swFcK/_/S/DZAEIxJZosED/G1tihktcN2DLYGa3/R3weTgo7RAE/SFUN/JTxWdhgB'
# proxy, format: https://username:password@ip:port
# 代理, 格式: https://username:password@ip:port
proxy = 'http://127.0.0.1:8989'

json_data = {
    "task_type": "akamai2-hard",
    "params": {
        "akamai_js_url": akamai_js_url,
        "proxy": proxy
    }
}

response = requests.post('https://riskbypass.com/api/task/sync', headers=headers, json=json_data)
print(response.json())
akamai_cookie = response.json().get('result', {}).get('result')
if '~0~' in akamai_cookie:
    print('Success\n成功')
else:
    print('Failed\n失败')
