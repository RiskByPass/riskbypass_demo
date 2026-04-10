import re
import json
import random
from curl_cffi import requests
from riskbypass import RiskByPassClient

BASE_URL = "https://riskbypass.com"                     # API base URL
TOKEN    = "Your Token"                                 # Access token (sent as x-api-key)
TIMEOUT  = 60                                           # Timeout (seconds)
# TODO french proxy, session mode
PROXY    = "http://username:password@host:port"         # Proxy string

print(PROXY)
proxies = {
    'http': PROXY,
    'https': PROXY
}

requests = requests.Session(impersonate=random.choice(['chrome136', 'firefox135']))
requests.proxies = proxies
requests.verify = False

payload = {
    "task_type": "reese84", 
    "proxy": PROXY, 
    "reese84_js_url": "https://login.accor.com/d-Exit-as-I-stature-This-bed-gatend-I-on-vnusual"
}

# RiskByPassClient client instance
client = RiskByPassClient(token=TOKEN, base_url=BASE_URL)
result = client.run_task(payload, timeout=TIMEOUT)
print(json.dumps(result, indent=2))

# update cookies with the result
requests.cookies.update(
    {'reese84': result['reese84']}
)

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://login.accor.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': f'https://all.accor.com/',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceparent': '00-03edfadfcdaeaf5c45f091af8eae9244-4ad0e3916a5a0a82-01',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'x-xsrf-header': 'PingFederate',
}

params = {
    'appId': 'all.accor',
    'ui_locales': 'en',
    'redirect_uri': 'https://all.accor.com/loyalty-funnel/check-authent.html',
    'redirect_site_uri': 'https://all.accor.com/a/en.html',
}

response = requests.get(
    'https://api.accor.com/authentication/v2.0/authorization',
    params=params,
    headers=headers,
    allow_redirects=False,
)

print(response.headers['location'])

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://login.accor.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': f'https://all.accor.com/',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceparent': '00-03edfadfcdaeaf5c45f091af8eae9244-4ad0e3916a5a0a82-01',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'x-xsrf-header': 'PingFederate',
}

response = requests.get(response.headers['location'], params=params, headers=headers, allow_redirects=False)

print(response.headers['location'])

url_params =response.headers['location'].split('?')[-1]

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://login.accor.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': f'https://login.accor.com/pf-ws/authn/{url_params}',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceparent': '00-03edfadfcdaeaf5c45f091af8eae9244-4ad0e3916a5a0a82-01',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'x-xsrf-header': 'PingFederate',
}

params = {
    'action': 'checkUsernamePassword',
}

json_data = {   # Only email addresses that have already been registered can be used to log in successfully.
    'username': 'youremail@gmail.com',
    'password': 'yourpassword',
}
print(f'https://login.accor.com/pf-ws/authn/{url_params}'.replace('flowId=', 'flows/'))

response = requests.post(
    f'https://login.accor.com/pf-ws/authn/{url_params}'.replace('flowId=', 'flows/'),
    params=params,
    headers=headers,
    json=json_data,
)

print(response.text)
print(response.status_code)
