import requests
import json
import random
from riskbypass import RiskByPassClient # pip install riskbypass

BASE_URL = "https://riskbypass.com"  # API base URL
TOKEN    = "your token"    # Access token (sent as x-api-key)
TIMEOUT  = 120                         # Max task execution time (seconds), exceeding this will throw an exception
random_port = random.randint(10000, 20000)
PROXY    = f"http://username:password@host:port"

# Task JSON payload
payload = {
  "task_type": "aws",
  "proxy": PROXY,
  "target_url": "https://superbet.bet.br/",
  "aws_js_url": "https://ab5d8485472a.5cd02325.sa-east-1.token.awswaf.com/ab5d8485472a/cf10ee63cfb6/challenge.compact.js"
}
# Initialize client
client = RiskByPassClient(token=TOKEN, base_url=BASE_URL)
# Run task
result = client.run_task(payload, timeout=TIMEOUT)

cookies = {
    'OptanonAlertBoxClosed': '2026-03-10T02:20:39.977Z',
    '_ga': 'GA1.1.782724869.1773109198',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Mon+Mar+09+2026+22%3A20%3A40+GMT-0400+(Eastern+Daylight+Time)&version=202501.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=fe738fa1-d4d1-49b8-8833-ff54c1599d91&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&intType=1',
    '_twpid': 'tw.1773109257264.366997718689792394',
    '_tguatd': 'eyJzYyI6IihkaXJlY3QpIiwiZnRzIjoiKGRpcmVjdCkifQ==',
    '_tgpc': '897089c7-b3c4-4387-b199-63c582e76cf0',
    '_tgidts': 'eyJzaCI6ImQ0MWQ4Y2Q5OGYwMGIyMDRlOTgwMDk5OGVjZjg0MjdlIiwiY2kiOiJlYjA2YjM4Ny00MjViLTQzMGItOWRiOC01MjI4YTY1MzQ1NzYiLCJzaSI6IjAzMmQwM2M2LTVlMmYtNGVhZi1iOWI5LWVhODIyMGEwODJlNyJ9',
    '_tglksd': 'eyJzIjoiMDMyZDAzYzYtNWUyZi00ZWFmLWI5YjktZWE4MjIwYTA4MmU3Iiwic3QiOjE3NzMxMDkyNTczMzAsInNvZCI6IihkaXJlY3QpIiwic29kdCI6MTc3MzEwOTI1NzMzMCwic29kcyI6Im8iLCJzb2RzdCI6MTc3MzEwOTI1NzMzMH0=',
    '_uetsid': 'c5ff7c401c2711f1ac4697dffbbb8b46',
    '_uetvid': 'c5ff7e601c2711f1b0774142b65da160',
    '_fbp': 'fb.2.1773109273437.872866456720901370',
    '_tt_enable_cookie': '1',
    '_ttp': '01KKARRRW4NF31JX8R754332E3_.tt.2',
    '_k_gid_collect': '1',
    'kwai_uuid': '78f06b3f8312b5eaed162d3b9d6a2aa5',
    '_k_cp': '1',
    '_tgsid': 'eyJscGQiOiJ7XCJscHVcIjpcImh0dHBzOi8vc3VwZXJiZXQuYmV0LmJyJTJGXCIsXCJscHRcIjpcIlN1cGVyYmV0JTIwQnJhc2lsJTIwJTdDJTIwQXBvc3RhcyUyMEVzcG9ydGl2YXMlMjAlN0MlMjBBcG9zdGFzJTIwT25saW5lXCIsXCJscHJcIjpcIlwifSIsInBzIjoiNGUxZmZjZDMtMGZlZi00MWQ5LWE1YjItN2I0MjkwZDZkYjAzIiwicHZjIjoiMSIsInNjIjoiMDMyZDAzYzYtNWUyZi00ZWFmLWI5YjktZWE4MjIwYTA4MmU3Oi0xIiwiZWMiOiI1IiwicHYiOiIxIiwidGltIjoiMDMyZDAzYzYtNWUyZi00ZWFmLWI5YjktZWE4MjIwYTA4MmU3OjE3NzMxMDkyNjAzNTI6LTEifQ==',
    'aws-waf-token': result.get('token'),
    'ttcsid_CU7NRURC77U5PP3DAJT0': '1773109273478::RjJ2LKNLTTbLvURLobnQ.1.1773110988370.1',
    'ttcsid': '1773109273478::fL4Di0LmAAjRsK0MQ8re.1.1773110988370.0',
    '_gcl_au': '1.1.2121430457.1773109240.795308922.1773110977.1773110988',
    '_ga_5WNY7XV0QK': 'GS2.1.s1773109197$o1$g1$t1773110988$j60$l0$h0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://superbet.bet.br',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://superbet.bet.br/',
    'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': result.get('ua'),
    'x-analytics-correlation-id': '067f0132-f31d-4862-8629-fab3ea623426',
    'x-aws-waf-token': result.get('token'),
}

params = {
    'type': 'multi',
    'destination': 'https://superbet.bet.br/',
    'clientSourceType': 'Desktop_new',
}

json_data = {
    'type': 'Credentials',
    'username': 'asdmksam@sds.com',
    'password': 'asdmkn3242.',
    'includeAccessToken': True,
    'session': 'W;6.10.5;MpC/zElmZZmNh+E7GVxKmg==;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',
    'sessionId': '2594269568942592722062838332790549198691773109334456',
    'deviceFingerprint': '38a39189-c6ae-4f8b-98ed-7621af74d64b',
    'externalDeviceId': '38a39189-c6ae-4f8b-98ed-7621af74d64b',
    'clientSourceType': 'Desktop_new',
}
from curl_cffi import requests
response = requests.post(
    'https://api.web.production.betler.superbet.bet.br/api/v1/login',
    params=params,
    cookies=cookies,
    headers=headers,
    json=json_data,
    proxy=PROXY
)

print(response.text)