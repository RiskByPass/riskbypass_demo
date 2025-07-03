import requests
from curl_cffi import request
import json

api_key = 'Your api key'
proxy = 'http://127.0.0.1:8989' # Your proxy

headers = {
    'Content-Type': 'application/json',
    'X-API-Key': api_key,
}
target_api = 'https://apiw.westjet.com/ecomm/booktrip/flight-search-api/v1' # The api url of your want to request
shape_js_url = 'https://www.westjet.com/resources/js/wj_common.js' # Your target website shape js url
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
    raise Exception('未知错误')
else:
    for i in range(10):
        print(f'第{i+1}次请求')
        target_data = '{"appSource":"3rdparty:OW","bookId":"22-5-2025-4-55-33-95977","currency":"USD","currentFlightIndex":1,"guests":[{"type":"adult","count":"1"},{"type":"child","count":"0"},{"type":"infant","count":"0"}],"showMemberExclusives":false,"trips":[{"order":1,"departure":"LAX","arrival":"YFC","departureDate":"2025-08-27"}],"isCommissionable":false,"promoCode":""}'
        try:
            response = request(method=method, url=target_api, data=target_data, headers=json.loads(shape_headers), impersonate='chrome136', proxies={'https':proxy})
            print(response.json())
        except Exception as e:
            print(e)