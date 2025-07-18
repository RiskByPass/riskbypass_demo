import random
import time
from concurrent.futures import ThreadPoolExecutor
import os
from curl_cffi import requests
import json
import threading
from datetime import datetime
import random

a = [
    'TPP 40-148A-J',
    'TPP 40-105A-J',
    'TPP 40-105E-D',
    'TPP 40-105E-J',
]
def get_px3():
    headers = {
        'content-type': 'application/json',
        'x-api-key': 'Your API Key',
    }

    random_str = ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyz', k=10))
    json_data = {
        'task_type': 'perimeterx-hard',
        'params': {
            'target_url': f'https://www.digikey.cn/zh/products/result?keywords={random_str}', # The page url which your target api is in
            'perimeterx_js_url': 'https://www.digikey.com/lO2Z493J/init.js', # The perimeterx js url, get it by F12
            'pxAppId': 'PXlO2Z493J', # The perimeterx app id, get it by F12
            'proxy': 'http://127.0.0.1:8989', # Your proxy
        },
    }

    response = requests.post('https://riskbypass.com/api/task/sync',  headers=headers, json=json_data)
    print(response.json())
    px_cookie = json.loads(response.json().get('result', {}).get('result', '{}'))
    return px_cookie

print_lock = threading.Lock()
headers = [
    {
        "Host": "www.digikey.cn",
        "Cache-Control": "max-age=0",
        "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Language": "zh-CN,zh;q=0.9"
    },

{
    "Host": "www.digikey.cn",
    "sec-ch-ua": "\"Chromium\";v=\"136\", \"Microsoft Edge\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
},

]
# cookies = get_px3()
def load_cookies():
    try:
        if os.path.exists('cookies.json'):
            with open('cookies.json', 'r',encoding='utf8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading cookies: {str(e)}")
    return None


def save_cookies(cookies):
    try:
        with open('cookies.json', 'w') as f:
            json.dump(cookies, f)
    except Exception as e:
        print(f"Error saving cookies: {str(e)}")


implements = [
    'chrome136',
    'chrome133a',
]

# Load cookies at startup
cookies = load_cookies()
if not cookies:
    cookies = get_px3()
    save_cookies(cookies)

proxy = "http://127.0.0.1:8989" # Your proxy
proxies = {
    "http": proxy,
    "https": proxy
}

def process_sku(sku):
    global cookies  # Use the global cookies variable

    try:
        with print_lock:
            # print(sku)
            pass

        # time.sleep(random.uniform(1,15))
        start_time = datetime.now()
        url = f"https://www.digikey.cn/zh/products/result?keywords={sku}"

        # First try with current cookies
        c = requests.get(url,proxies=proxies, headers=random.choice(headers), cookies=cookies, impersonate=random.choice(implements))
        print(c)
        if c.status_code != 200:
            cookies = get_px3()
            save_cookies(cookies)
            c = requests.get(url,proxies=proxies, headers=random.choice(headers), cookies=cookies, impersonate=random.choice(implements))

        end_time = datetime.now()
        print(end_time - start_time)
        print(sku)
        print(c)
        print('-------------')

    except Exception as e:
        with print_lock:
            print(f"Error processing {sku}: {str(e)}")


with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(process_sku, a[::-1])