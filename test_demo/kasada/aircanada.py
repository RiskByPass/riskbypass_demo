from curl_cffi import requests
import requests as requests_normal
import json
import time

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
    response = requests_normal.post('https://riskbypass.com/api/task/sync', headers=headers, json=json_data, timeout=100)
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
            "ct": ct, # The x-kpsdk-ct of first request's response
            "st": st # The x-kpsdk-st of first request's response
        }
    }
    response = requests_normal.post(url='https://riskbypass.com/api/task/sync', headers=headers, json=json_data)
    print(response.json())
    cd = response.json().get('result', {}).get('result')
    return cd

proxy = 'http://127.0.0.1:8989' # Your proxy
site = 'akamai-gw.dbaas.aircanada.com' # The kasada protection site domain
api_key = 'Your API Key' # Your api key

res = get_ct(site, proxy, api_key) # Get the x-kpsdk-ct and x-kpsdk-st

ct = res['x-kpsdk-ct']
st = res['x-kpsdk-st']
v = res['x-kpsdk-v']
cd = get_cd(ct, st, api_key) # Get the x-kpsdk-cd

cookies = {
    'akm_bmcs_r2-ssn': ct,
    'akm_bmcs_r2': ct,
}

auth = 'Bearer eyJraWQiOiJVT3NQMkJHOVdrVlVobTNYMWtCWjh1NHVkSDlka2hZVU5ta1wvU1R0alUwYz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyMWI1ZDUxNi1jYmRiLTQ4MTAtYmE3OC0zZDgyMTA3MjI1NWYiLCJjb2duaXRvOmdyb3VwcyI6WyJ1cy1lYXN0LTJfSm5jQUVjeUM4X0dpZ3lhIl0sImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTIuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0yX0puY0FFY3lDOCIsInZlcnNpb24iOjIsImNsaWVudF9pZCI6IjVwdXQwcG8xanF0cmZpNGs5Zm00M3JvZmxnIiwidG9rZW5fdXNlIjoiYWNjZXNzIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSIsImF1dGhfdGltZSI6MTc1MTQ1MDQyOSwiZXhwIjoxNzUxNDUxMzI5LCJpYXQiOjE3NTE0NTA0MzAsImp0aSI6ImVhYmM1MDE4LWFhYWMtNDA3MS04MjkyLWUyMzM5ZWZlMzUzOSIsInVzZXJuYW1lIjoiR2lneWFfMWEyODM2YWQtNWJiYi00NTkzLWExZWEtNjUwM2U1MzczODYxIn0.NyXu9UTBeFh8zPa5KZxUftzgOzZiSs8_AqIdmNxIpn55iYJFhLMTJDQFZqd8ec_3t0eKpzc2r4biclvGpnUkefhrHZ3ciSYu6lJIjLDMwC9BCU-YvOHIkY3bjb9QS6QneN9Qp_8VXedBmAMgw62FP07-IE9yc67OtPIGJsjEu0CXs2seymMayg4n_rLrkXL4fTGYqdRl7W3DZj1Z-WrlwFvlPzGM6fgaYEtTnlwEE3AGWwNdVlf9pFW9rwoxS3041T6Mbvo6nlZHfrfXkZUtJTsZLltU77v3EBVamJOT7kRfKxSCKmyKPudwk7LSM3GUxlNBpj2WYySuxcPDrLZ-Fg'
headers = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9',
    'ama-session-token': 'bdKppDgDA4okrmPnD0IyZUGF2LYXSaRg9sMhklUhjDHAmr/DmT9jH9KvPtKTXUBtzk3n8IgP8kJiSC14rf5D+897pPS7XC1c+WnaSuxQgKhnTJZ6xIqYY00vaEOf+5M/immQxTaZsRjUBwwABQafYdEsqX0=',
    'authorization': auth,
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://www.aircanada.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.aircanada.com/',
    'sec-ch-ua': res['sec-ch-ua'], # The sec-ch-ua of first request's response
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': res['sec-ch-ua-platform'], # The sec-ch-ua-platform of first request's response
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': res['user-agent'], # The user-agent of first request's response
    'x-api-key': 'Z5R8Rm1sA37iC0gaS5kb69ltHwKBTYzUa89gQDwm',
    'x-custom-id-token': 'eyJraWQiOiJxVTNjRTdBNnk4NlF5ekRoR1dSUjVsY2FTSEMxZlBuTXRDSVVJVEVFQW1VPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiSE56RUJtbjB6S05vSF9vU0JlN1k2USIsImN1c3RvbTpjb3VudHJ5IjoiR0IiLCJzdWIiOiIyMWI1ZDUxNi1jYmRiLTQ4MTAtYmE3OC0zZDgyMTA3MjI1NWYiLCJjb2duaXRvOmdyb3VwcyI6WyJ1cy1lYXN0LTJfSm5jQUVjeUM4X0dpZ3lhIl0sImRldmljZV9pZCI6ImFmYzRlMGUyLTFiMTMtNDY0Mi1iODUxLTdhYWY0ZDkzMTY1YiIsImN1c3RvbTpsYXN0TG9naW4iOiIxNzUxNDM3MTk1MDAwIiwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMi5hbWF6b25hd3MuY29tXC91cy1lYXN0LTJfSm5jQUVjeUM4IiwiY3VzdG9tOmZmcCI6IjE0MTM4MTY0MCIsImNvZ25pdG86dXNlcm5hbWUiOiJHaWd5YV8xYTI4MzZhZC01YmJiLTQ1OTMtYTFlYS02NTAzZTUzNzM4NjEiLCJsb2NhbGUiOiJlbiIsIm5vbmNlIjoiT3VaLXQ4ZlFyLVhqaEVHcjZnRlZqTjM4V1dja3p5WVZXNW9pandtYjhXcmZBT1RmaEktVWNFcTFleEdmU0JWZVVSYkQ0a19wTnZqRndxWWdkSW9xOWU3NG5TMzV2M3hFLVRXNnNkcDdDbGlHaTJuZmYwVGF1X1NzbnYxT2I0RkQxT1Rrb2Q1Vlptb3J0YS1wcFRnOXVYbWFKeEZfM1NNeUV1TzVxcVNMdVlJIiwiYXVkIjoiNXB1dDBwbzFqcXRyZmk0azlmbTQzcm9mbGciLCJpZGVudGl0aWVzIjpbeyJ1c2VySWQiOiIxYTI4MzZhZC01YmJiLTQ1OTMtYTFlYS02NTAzZTUzNzM4NjEiLCJwcm92aWRlck5hbWUiOiJHaWd5YSIsInByb3ZpZGVyVHlwZSI6Ik9JREMiLCJpc3N1ZXIiOm51bGwsInByaW1hcnkiOiJ0cnVlIiwiZGF0ZUNyZWF0ZWQiOiIxNzQ5NDAwOTQ1MjI4In1dLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTc1MTQzNzIxMiwiZXhwIjoxNzUxNDM4MTEyLCJpYXQiOjE3NTE0MzcyMTJ9.IlhCrWtNNvIC2WXFDsd2gDRZFK9VGZsc6NKcGYnLJiTw_NByE6uN1wamIGrc1mlnc5Km9Glh5TIIvRUZjrMVblKSIoLtFjkzf0OXVc23GLaHOBUDd3wsnK3U4e3s37oj3kxVK9MJIf-1Gv-lcSXNmD81zPTLXKarfu50Xu-PPgHs3gU3PZIiv0D7ltGMRhDr-JaUVPLc2i4OeYN03lyN0aCrwPhpe89TgKt-9Kv_9PxNnodwDxgtqI2C-rE9O6AHPoCw513f2ph9C7Ddc0YRybUoEUIR28chKyn8Iat7ORJnOnFHsH1Mvr0ywXhUZcls3aljv83KCpE566d-V9qAjQ',
    'x-kpsdk-cd': cd,
    'x-kpsdk-ct': ct,
    'x-kpsdk-v': v,
}

json_data = {
    'searchPreferences': {
        'showSoldOut': False,
        'showMilesPrice': True,
    },
    'corporateCodes': [
        'REWARD',
    ],
    'travelers': [
        {
            'passengerTypeCode': 'ADT',
        },
    ],
    'currencyCode': 'CAD',
    'itineraries': [
        {
            'originLocationCode': 'JFK',
            'destinationLocationCode': 'LHR',
            'departureDateTime': '2025-08-08T00:00:00.000',
            'isRequestedBound': True,
            'commercialFareFamilies': [
                'REWARD',
            ],
        },
    ],
    'frequentFlyer': {
        'cardNumber': '141381640',
        'companyCode': 'AC',
        'priorityCode': '9',
    },
}

response = requests.post(
    'https://akamai-gw.dbaas.aircanada.com/loyalty/dapidynamicplus/1ASIUDALAC/v2/search/air-bounds',
    cookies=cookies,
    headers=headers,
    json=json_data,
    proxies={
        'http': 'http://127.0.0.1:8989',
        'https': 'http://127.0.0.1:8989',
    },
    impersonate='chrome136'
)

print(response.text)
print(response.status_code)

url = "https://akamai-gw.dbaas.aircanada.com/loyalty/polldapi"
data = {
    "pollId": response.json()['pollId']
}
data = json.dumps(data, separators=(',', ':'))
time.sleep(5)
response = requests.post(url, headers=headers, data=data, impersonate='chrome136')
print(response.text)