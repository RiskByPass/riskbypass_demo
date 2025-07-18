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
    response = crequests.post('https://riskbypass.com/api/task/sync', headers=headers, json=json_data, timeout=30)
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
    response = crequests.post('https://riskbypass.com/api/task/sync', headers=headers, json=json_data, timeout=30)
    print(response.json())
    cd = response.json().get('result', {}).get('result')
    return cd

proxy = 'http://127.0.0.1:8989' # Your proxy
api_key = 'Your API Key' # Your api key
site = 'passport.twitch.tv' # The kasada protection site domain

kasada_args = get_ct(site=site, proxy=proxy, api_key=api_key)
ct = kasada_args['x-kpsdk-ct'] # Get the x-kpsdk-ct
st = kasada_args['x-kpsdk-st'] # Get the x-kpsdk-st
v = kasada_args['x-kpsdk-v'] # Get the x-kpsdk-v
cd = get_cd(ct=ct, st=st, api_key=api_key) # Get the x-kpsdk-cd
user_agent = kasada_args['user-agent'] # Get the user-agent
sec_ch_ua = kasada_args['sec-ch-ua'] # Get the sec-ch-ua
sec_ch_ua_platform = kasada_args['sec-ch-ua-platform'] # Get the sec-ch-ua-platform

cookies = {
    'unique_id': 'ktXuYfdjRxvDpUZ5HBoGmqNtpNfJywXA',
    'unique_id_durable': 'ktXuYfdjRxvDpUZ5HBoGmqNtpNfJywXA',
    'twitch.lohp.countryCode': 'SG',
    'experiment_overrides': '{%22experiments%22:{}%2C%22disabled%22:[]}',
    'api_token': 'twilight.6201d631f4d083a0a8c8fb5678b599ec',
    'ga__15_abel-ssn': ct,
    'ga__15_abel': ct,
    'server_session_id': '9c98c62199d848efab1967dfba591199',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Origin': f'https://www.twitch.tv',
    'Pragma': 'no-cache',
    'Referer': f'https://www.twitch.tv/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': user_agent,
    'sec-ch-ua': sec_ch_ua,
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': sec_ch_ua_platform,
    'x-kpsdk-cd': cd,
    'x-kpsdk-ct': ct,
    'x-kpsdk-v': v,
}
json_data = {"username":"sadsadghg","password":"Y8Dv*v$C:YyG<aK","email":"a12357mn2@gmail.com","birthday":{"day":12,"month":12,"year":1979,"isOver18":True},"client_id":"kimne78kx3ncx6brgo4mv6wki5h1ko","is_password_guide":"nist"}

for i in range(10):
    print(f'Request {i+1} times')
    response = crequests.post(
            url='https://passport.twitch.tv/protected_register',
            headers=headers,
            json=json_data,
            proxies={'http': proxy, 'https': proxy},
            impersonate='chrome136',
            cookies=cookies,
            timeout=30
        )
    print(response.text)
    headers['x-kpsdk-cd'] = get_cd(ct=ct, st=st, api_key=api_key)
