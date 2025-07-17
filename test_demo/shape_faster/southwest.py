from curl_cffi import request
import json
import base64
import time

api_key = 'Your API Key'
proxy = "http://username:password@ip:port" # Your proxy

def get_shape_params(shape_js_url, proxy):
    start_time = time.time()
    response = request(method='GET', url=shape_js_url, impersonate='chrome136', proxies={'https':proxy})
    end_time = time.time()
    print(f'Get shape js content success! Time cost: {end_time - start_time} seconds')
    shape_js_content = base64.b64encode(response.content).decode('utf-8')
    shape_js_cookie = dict(response.cookies)
    print(f'Get shape js cookie success!')
    return shape_js_content, shape_js_cookie

headers = {
    'Content-Type': 'application/json',
    'X-API-Key': api_key,
}
target_api = 'https://www.southwest.com/api/security/v4/security/token' # The api url of your want to request
shape_js_url = 'https://www.southwest.com/assets/app/scripts/swa-common.js' # Your target website shape js url
method = 'POST' # The api method of your want to request
print(f'Start get shape js content...')
shape_js_content, shape_js_cookie = get_shape_params(shape_js_url, proxy)
print(f'Get shape js content success!')

json_data = {
    'task_type': 'shape-headers',
    'params': {
        'shape_js_url': shape_js_url,
        'target_api': target_api,
        'proxy': proxy,
        'method': method,
        'shape_js_content': shape_js_content,
        'shape_js_cookie': shape_js_cookie,
    },
}

print(f'Start send task to riskbypass...')
start_time = time.time()
response = request(method='POST', url='https://riskbypass.com/api/task/no_access/sync', headers=headers, json=json_data)
end_time = time.time()
print(f'Send task to riskbypass success! Time cost: {end_time - start_time} seconds')
print(response.json())
shape_headers = json.loads(response.json().get('result', {}).get('result')) # The shape headers of your want to request
shape_headers.update({
    'x-api-key': 'l7xx944d175ea25f4b9c903a583ea82a1c4c',
    'x-app-id': 'air-booking',
    'x-channel-id': 'southwest',
    'x-user-experience-id': '371f78d2-ed3c-4123-a19c-c256116930c3',
}) # The southwest's custom headers
if not shape_headers:
    raise Exception('Unknown error')
else:
    for i in range(10):
        print(f'Request {i+1} times')
        target_data = 'username=RiskByPass&password=xxxxxxxx&scope=openid&client_id=6b6199ac-6726-4642-b5bd-86eb07062161&response_type=id_token+swa_token'
        try:
            response = request(method=method, url=target_api, data=target_data, headers=shape_headers, impersonate='chrome136', proxies={'https':proxy})
            print(response.json())
        except Exception as e:
            print(e)