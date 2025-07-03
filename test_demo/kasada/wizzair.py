import requests
from curl_cffi import requests as crequests
import json

api_url = 'http://spiderapi.zicp.fun/api/task/sync'
api_key = 'Your api key'

def get_datadome(api_key, target_url, datadome_js_url, ddjskey, ddoptions, proxy):
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': api_key,
    }
    json_data = {
        "task_type": "datadome-hard",
        "params": {
            "target_url": target_url, # The page url which your target api is in
            "datadome_js_url": datadome_js_url, # The datadome js url
            "ddjskey": ddjskey, # The datadome's window.ddjskey
            "ddoptions": ddoptions, # The datadome's window.ddoptions
            "proxy": proxy # Your proxy
        }
    }
    response = requests.post(api_url, headers=headers, json=json_data)
    print(response.json())
    datadome_cookie = response.json().get('result', {}).get('result')
    return json.loads(datadome_cookie)

def get_ct(site, proxy, api_key):
    headers = {
        'X-API-Key': api_key,
        'Content-Type': 'application/json',
    }
    json_data = {
        'task_type': 'kasada-common-ct',
        'params': {
            'site': site,
            'proxy': proxy,
        },
    }
    response = requests.post(api_url, headers=headers, json=json_data)
    print(response.json())
    kasada_result = response.json().get('result', {}).get('result')
    return json.loads(kasada_result)

def get_cd(ct, st, api_key):
    headers = {
        'X-API-Key': api_key,
        'Content-Type': 'application/json',
    }
    json_data = {
        "task_type": "kasada-common-cd",
        "params": {
            "ct": ct,
            "st": st
        }
    }
    response = requests.post(api_url, headers=headers, json=json_data)
    print(response.json())
    cd = response.json().get('result', {}).get('result')
    return cd

proxy = 'http://127.0.0.1:8989' # Your proxy
site = 'www.wizzair.com' # The kasada protection site domain
datadome_js_url = 'https://dd.wizzair.com/tags.js' # The datadome js url
ddjskey = '999D78C37FCDE5C93AA39F821E8377' # The datadome's window.ddjskey
ddoptions = json.dumps({"ajaxListenerPath": {"host": "be.wizzair.com"}, "withCredentials": True}) # The datadome's window.ddoptions

datadome_cookie = get_datadome(api_key=api_key, target_url=f'https://{site}/', datadome_js_url=datadome_js_url, ddjskey=ddjskey, ddoptions=ddoptions, proxy=proxy)
kasada_args = get_ct(site=site, proxy=proxy, api_key=api_key)
ct = kasada_args['x-kpsdk-ct'] # Get the x-kpsdk-ct
st = kasada_args['x-kpsdk-st'] # Get the x-kpsdk-st
v = kasada_args['x-kpsdk-v'] # Get the x-kpsdk-v
cd = get_cd(ct=ct, st=st, api_key=api_key) # Get the x-kpsdk-cd
user_agent = kasada_args['user-agent'] # Get the user-agent
sec_ch_ua = kasada_args['sec-ch-ua'] # Get the sec-ch-ua

csrf_token = '051c7d629a144b8298cb058b03ab62ec' # The csrf token
cookies = {
    'RequestVerificationToken': csrf_token,
    'ak_bm_vw_1.1-ssn': ct,
    'ak_bm_vw_1.1': ct,
    'datadome': datadome_cookie.get('datadome'),
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://www.wizzair.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.wizzair.com/',
    'sec-ch-ua': sec_ch_ua,
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': user_agent,
    'x-kpsdk-cd': cd,
    'x-kpsdk-ct': ct,
    'x-kpsdk-v': v,
    'x-requestverificationtoken': csrf_token,
}
json_data = {
    'isFlightChange': False,
    'flightList': [
        {
            'departureStation': 'TIA',
            'arrivalStation': 'VIE',
            'departureDate': '2025-06-22T00:00:00',
        },
    ],
    'adultCount': 1,
    'childCount': 0,
    'infantCount': 0,
    'wdc': True,
}

for i in range(10):
    print(f'第{i+1}次请求')
    response = crequests.post(
            url='https://be.wizzair.com/27.12.0/Api/search/search',
            headers=headers,
            json=json_data,
            proxies={'http': proxy, 'https': proxy},
            impersonate='chrome136',
            cookies=cookies
        )
    print(response.status_code)
    print(response.text)
    headers['x-kpsdk-cd'] = get_cd(ct=ct, st=st, api_key=api_key)