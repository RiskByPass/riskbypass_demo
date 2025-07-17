import requests
from curl_cffi import request
import json

api_key = 'Your api key'
headers = {
    'Content-Type': 'application/json',
    'X-API-Key': api_key,
}
shape_js_url = 'https://www.starbucks.com/vendor/static/vendor2.js' # The shape headers of your want to request
target_api = 'https://www.starbucks.com/apiproxy/v1/account/create' # The api url of your want to request
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

response = requests.post('https://riskbypass.com/api/task/sync', headers=headers, json=json_data)
print(response.json())
shape_headers = response.json().get('result', {}).get('result') # The shape headers of your want to request
if not shape_headers:
    raise Exception('Unknown error')
else:
    for i in range(10):
        print(f'Request {i+1} times')
        target_data = json.dumps({
            'country': 'US',
            'locale': 'en-US',
            'registrationSource': 'Web',
            'reputation': {
                'ccAgentName': 'WebApp',
                'platform': 'Web',
                'market': 'US',
                'deviceFingerprint': '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;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',
            },
            'receiveStarbucksEmailCommunications': True,
            'emailAddress': '1234567890@gmail.com',
            'firstName': 'casa',
            'lastName': 'dsaf',
            'password': 'Risk123......',
            'termsAndConditions': True,
            'cardRewards': 'digitalCard',
        }, separators=(',', ':'))
        try:
            response = request(method=method, url=target_api, data=target_data, headers=json.loads(shape_headers), impersonate='chrome136', proxies={'https':proxy})
            print(response.json())
        except Exception as e:
            print(e)