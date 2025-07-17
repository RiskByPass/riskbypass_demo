from curl_cffi import request
import json

api_key = 'Your api key'
headers = {
    'Content-Type': 'application/json',
    'X-API-Key': api_key,
}
shape_js_url = 'https://www.nordstrom.com/mwp/integration/ns_common.js?async' # Your target website shape js url
target_api = 'https://www.nordstrom.com/review/review?apikey=sGJGRvnBEzn4qvQyGZe7prihKstgGXXT&styleid=8133121&page=1&pagesize=6&starrating=&sortby=-positivefeedbackcount%2C-submissiontime&searchTerm=&feature=&hasPhotos=false&filterBySize=&filterByColor=&filterByWidth=&isVerifiedPurchase=false&includeCriticalPositiveReviews=true' # The api url of your want to request
proxy = 'http://127.0.0.1:8989' # Your proxy
method = 'GET' # The api method of your want to request

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
if not shape_headers:
    raise Exception('Unknown error')
else:
    shape_headers = json.loads(shape_headers) # The shape headers of your want to request
    shape_headers['accept'] = 'application/vnd.nord.review.default.v1+json' # The nordstrom's custom headers
    shape_headers['content-type'] = 'application/vnd.nord.review.default.v1+json'
    for i in range(10):
        print(f'Request {i+1} times')
        try:
            response = request(method=method, url=target_api, headers=shape_headers, impersonate='chrome136', proxies={'https':proxy})
            print(response.json())
        except Exception as e:
            print(e)