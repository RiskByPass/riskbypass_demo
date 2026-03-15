# -*- coding: utf-8 -*-
# 由 RiskByPass 面板自动生成
# 依赖: pip install riskbypass
import requests
import json, random
from riskbypass import RiskByPassClient
import cycronet
import json, random

BASE_URL = "https://riskbypass.com"  # api端口地址
TOKEN    = "your token"    # 访问令牌（作为 x-api-key 发送）
TIMEOUT  = 120                         # 任务最大执行时间（秒）, 超出此时间将抛出异常
# 初始化客户端
client = RiskByPassClient(token=TOKEN, base_url=BASE_URL)

def main():
    random_port = random.randint(10000, 20000)
    PROXY = f"http://xxxxxxxxxxxx__cr.us:xxxxxxxxxxxx@gw.dataimpulse.com:{random_port}"  # 代理
    print(PROXY)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'nonce': 'yMVq5FfJRmhwZIgHtPIb',
        'scope': 'openid profile email',
        'client_id': 'portaluser',
        'redirect_uri': 'https://www.maersk.com/portaluser/oidc/callback',
        'response_type': 'code',
        'code_challenge': 'LmwHWYLIcF4aH85_AOKinN5nX90D4zLVoCF4K9NkS_8',
    }

    # 任务 JSON
    payload = {
        "task_type": "custom_task",
        "proxy": "http://username:password@ip:port",
        "target_url": "maersk.com",
    }
    payload['proxy'] = PROXY
    # 运行任务
    result = client.run_task(payload, timeout=TIMEOUT)
    print(json.dumps(result, indent=4))
    
    headers = {
        "Host": "accounts.maersk.com",
        "Connection": "keep-alive",
        "Content-Length": "0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Google Chrome\";v=\"145\", \"Chromium\";v=\"145\"",
        "accept-api-version": "protocol=1.0,resource=2.1",
        "x-auth-method": "frPrimaryAuth_UsernamePassword",
        "sec-ch-ua-mobile": "?0",
        "traceparent": "00-a40d93ecab65c63ce85088ee33fa653d-44ecb6980b2eabf7-01",
        "x-login-source": "https://www.maersk.com/portaluser/oidc/callback",
        "x-requested-with": "forgerock-sdk",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        "accept": "application/json",
        "x-acm-username": "a1796932792sd",
        "content-type": "application/json",
        "x-acm-password": "asdasdas12.",
        "Origin": "https://accounts.maersk.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://accounts.maersk.com/ocean-maeu/auth/login?nonce=yMVq5FfJRmhwZIgHtPIb&scope=openid%20profile%20email&client_id=portaluser&redirect_uri=https%3A%2F%2Fwww.maersk.com%2Fportaluser%2Foidc%2Fcallback&response_type=code&code_challenge=LmwHWYLIcF4aH85_AOKinN5nX90D4zLVoCF4K9NkS_8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en",
    }

    params = {
        'authIndexType': 'service',
        'authIndexValue': 'frPrimaryAuth',
    }
    response = cycronet.post(
        'https://accounts.maersk.com/root/acm/json/realms/mau/authenticate',
        params=params,
        cookies=result,
        headers=headers,
        chrometls="chrome_144",
        proxies={
            'https':PROXY
        }
    )
    print(response.text)
    print(response.status_code)

if __name__ == '__main__':
    main()