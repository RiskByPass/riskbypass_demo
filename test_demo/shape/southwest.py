from curl_cffi import request
import json

api_key = 'Your api key'
proxy = 'http://127.0.0.1:8989' # Your proxy

headers = {
    'Content-Type': 'application/json',
    'X-API-Key': api_key,
}
target_api = 'https://www.southwest.com/api/air-booking/v1/air-booking/page/air/booking/shopping' # The api url of your want to request
shape_js_url = 'https://www.southwest.com/assets/app/scripts/swa-common.js' # Your target website shape js url
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
shape_headers = json.loads(response.json().get('result', {}).get('result')) # The shape headers of your want to request
shape_headers.update({
    'x-api-key': 'l7xx944d175ea25f4b9c903a583ea82a1c4c',
    'x-app-id': 'air-booking',
    'x-channel-id': 'southwest',
    'x-user-experience-id': '371f78d2-ed3c-4123-a19c-c256116930c3',
}) # The southwest's custom headers
if not shape_headers:
    raise Exception('未知错误')
else:
    for i in range(10):
        print(f'第{i+1}次请求')
        target_data = '{"adultPassengersCount":"1","adultsCount":"1","departureDate":"2025-07-15","departureTimeOfDay":"ALL_DAY","destinationAirportCode":"OAK","fareType":"USD","from":"ISP,LGA","int":"HOMEQBOMAIR","originationAirportCode":"ISP","passengerType":"ADULT","promoCode":"","returnDate":"","returnTimeOfDay":"ALL_DAY","to":"OAK,SFO,SJC","tripType":"oneway","application":"air-booking","site":"southwest"}'
        try:
            response = request(method=method, url=target_api, data=target_data, headers=shape_headers, impersonate='chrome136', proxies={'https':proxy})
            print(response.json())
        except Exception as e:
            print(e)