from curl_cffi import requests
import json


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
    response = requests.post('https://riskbypass.com/api/task/sync', headers=headers, json=json_data, verify=False)
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
    response = requests.post('https://riskbypass.com/api/task/sync', headers=headers, json=json_data, verify=False)
    print(response.json())
    cd = response.json().get('result', {}).get('result')
    return cd

proxy = 'http://127.0.0.1:8989' # Your proxy
api_key = 'Your api key' # Your api key
site = 'arcteryx.com' # The kasada protection site domain

kasada_args = get_ct(site=site, proxy=proxy, api_key=api_key)
ct = kasada_args['x-kpsdk-ct'] # Get the x-kpsdk-ct
st = kasada_args['x-kpsdk-st'] # Get the x-kpsdk-st
v = kasada_args['x-kpsdk-v'] # Get the x-kpsdk-v
cd = get_cd(ct=ct, st=st, api_key=api_key) # Get the x-kpsdk-cd
user_agent = kasada_args['user-agent'] # Get the user-agent
sec_ch_ua = kasada_args['sec-ch-ua'] # Get the sec-ch-ua
sec_ch_ua_platform = kasada_args['sec-ch-ua-platform'] # Get the sec-ch-ua-platform

headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': f'https://{site}',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': f'https://{site}/',
        'sec-ch-ua': sec_ch_ua,
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': sec_ch_ua_platform,
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'store': 'arcteryx_zh',
        'user-agent': user_agent,
        'x-country-code': 'ca',
        'x-is-checkout': 'false',
        'x-jwt': '',
        'x-kpsdk-cd': cd,
        'x-kpsdk-ct': ct,
        'x-kpsdk-v': v,
        "traceparent": "00-10b8ac50f91aa080fc936005d2d834d3-e7eb4eee8588a751-01",
        "tracestate": "2478470@nr=0-1-2478470-367491848-e7eb4eee8588a751----1751426587746",
        "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjI0Nzg0NzAiLCJhcCI6IjM2NzQ5MTg0OCIsImlkIjoiZTdlYjRlZWU4NTg4YTc1MSIsInRyIjoiMTBiOGFjNTBmOTFhYTA4MGZjOTM2MDA1ZDJkODM0ZDMiLCJ0aSI6MTc1MTQyNjU4Nzc0Nn19",
    }
json_data = {
        'query': 'query gqlGetProductInventoryBySkus($productSkus: [String!]) { products(filter: { sku: { in: $productSkus } }, pageSize: 500) { items { name sku ...on ConfigurableProduct { variants { product { sku quantity_available } } } } } }',
        'variables': {
            'productSkus': [
                'X000009165',
            ],
        },
    }

for i in range(10):
    print(f'第{i+1}次请求')
    response = requests.post(
                url='https://arcteryx.com/api/mcgql',
                headers=headers,
                json=json_data,
                proxies={'http': proxy, 'https': proxy},
                impersonate='firefox135'
            )
    print(response.text)
    print(response.status_code)
    headers['x-kpsdk-ct'] = dict(response.cookies).get('KP_UIDz')
    ct = headers['x-kpsdk-ct']
    headers['x-kpsdk-cd'] = get_cd(ct=ct, st=st, api_key=api_key)