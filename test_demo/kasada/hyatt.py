import requests
from curl_cffi import requests as crequests
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
    response = requests.post('https://riskbypass.com/api/task/sync', headers=headers, json=json_data)
    print(response.json())
    kasada_result = response.json().get('result', {}).get('result')
    return json.loads(kasada_result)

def get_index_page():
    proxy = 'http://127.0.0.1:8989' # Your proxy
    api_key = 'Your API Key' # Your api key
    site = 'www.hyatt.com' # The kasada protection site domain
    kasada_result = get_ct(site, proxy, api_key) # Get the x-kpsdk-ct
    ct = kasada_result['x-kpsdk-ct'] # Get the x-kpsdk-ct
    cookies = {
        'tkrm_alpekz_s1.3-ssn': ct,
        'tkrm_alpekz_s1.3': ct,
    }
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'sec-ch-ua': kasada_result['sec-ch-ua'], # Get the sec-ch-ua
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': kasada_result['sec-ch-ua-platform'], # Get the sec-ch-ua-platform
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': kasada_result['user-agent'], # Get the user-agent
    }
    for i in range(10):
        print(f'Request {i+1} times')
        response = crequests.get(
            'https://www.hyatt.com/zh-CN/shop/service/rooms/roomrates/nycph?&checkinDate=2025-08-09&checkoutDate=2025-08-10&rooms=1&adults=1&kids=0&corp_id=13717&rateFilte',
            cookies=cookies,
            headers=headers,
            impersonate='firefox133',
            proxies={'https': proxy}
        )
        print(response.text)

get_index_page()