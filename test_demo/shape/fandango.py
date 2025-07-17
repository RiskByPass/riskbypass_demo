from curl_cffi import request
import json

api_key = 'Your API Key'
proxy = "http://username:password@ip:port" # Your proxy

headers = {
    'Content-Type': 'application/json',
    'X-API-Key': api_key,
}
target_api = 'https://tickets.fandango.com/commerce/payment-methods/balance' # The api url of your want to request
shape_js_url = 'https://images.fandango.com/r2.0.1.1226/assets/fandango-common.js?async' # Your target website shape js url
method = 'POST' # The api method of your want to request

json_data = {
    'task_type': 'shape-headers',
    'params': {
        'shape_js_url': shape_js_url,
        'target_api': target_api,
        'proxy': proxy,
        'method': method,
    },
}

response = request(method='POST', url='https://riskbypass.com/api/task/sync', headers=headers, json=json_data, proxy=proxy, timeout=50)
print(response.json())
shape_headers = json.loads(response.json().get('result', {}).get('result')) # The shape headers of your want to request
fandango_user_cookies = {
    'xxx': 'xxx',
} # The fandango's user cookies
if not shape_headers:
    raise Exception('未知错误')
else:
    for i in range(10):
        print(f'第{i+1}次请求')
        target_data = 'xxx'
        try:
            response = request(method=method, url=target_api, data=target_data, headers=shape_headers, impersonate='chrome136', proxies={'https':proxy}, cookies=fandango_user_cookies)
            print(response.json())
        except Exception as e:
            print(e)