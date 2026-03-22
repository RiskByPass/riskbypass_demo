# -*- coding: utf-8 -*-
# 由 RiskByPass 面板自动生成
# 依赖: pip install riskbypass
import random, re
from riskbypass import RiskByPassClient
from requests_go import Session
from requests_go.tls_config import TLS_CHROME_LATEST

BASE_URL = "https://riskbypass.com"  # api端口地址
TOKEN    = "your token"    # 访问令牌（作为 x-api-key 发送）
TIMEOUT  = 120                         # 任务最大执行时间（秒）, 超出此时间将抛出异常
PROXY = f"http://xxxxxxxxxx__cr.us:xxxxxxxxxx@gw.dataimpulse.com:{random.randint(10000, 20000)}"

client = RiskByPassClient(token=TOKEN, base_url=BASE_URL)

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
}

session = Session()
session.tls_config = TLS_CHROME_LATEST

response = session.get('https://www.kohls.com/giftcard/gift_card_check_balance.jsp', headers=headers, proxies={'https': PROXY})
init_cookies = session.cookies.get_dict()

akamai_payload = {
  "task_type": "akamai",
  "proxy": "http://username:password@ip:port",
  "target_url": "https://www.kohls.com/giftcard/gift_card_check_balance.jsp",
  "akamai_js_url": "https://www.kohls.com/5mnx6xKr3U/FSgldaIP/Q-/Si7rrX5fYbOSNc/ZklJUVMpdA0/T0VoNg/U_PBAB",
  "page_fp": "424543475255404d4540424545585255405a435f5f585f5b4e495c5046444745425f50485c5048435e4442475255404d4241475a5f5a5240494d424842455e5a4e495c515f4244504a47534b47565f4249595f465355404d435f4059445a4e484556415f4352"
}
akamai_payload['proxy'] = PROXY
akamai_payload['init_cookies'] = init_cookies
akamai_payload['akamai_js_url'] = 'https://www.kohls.com' + re.findall(r'<script type="text/javascript"  src="(.*?)">', response.text)[-1]
result = client.run_task(akamai_payload, timeout=TIMEOUT)

cookies = result.get('cookies_dict')
ua = result.get('ua')
print(cookies)
headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en,en-US;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.kohls.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.kohls.com/giftcard/gift_card_check_balance.jsp',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

data = {
    'giftCardNumber': '34534534353445',
    'giftCardPin': '2345',
    'couponNumber': '',
    'couponNumberPin': '',
    'g-recaptcha-response': '0cAFcWeA4I27SVojD75os631ZsI-amEh4BCtfey9iIm607W9HmneLX-Hf-XNYT4XntSU7ZNaV5EddefMQRNxpz9aDd_AXJbC3dMOKXCDwR_tVKIUlAqKBjtDg2JwdAGi5u4Bemwad6z4zVhSMvPUppe8mtfCGobCB-C9wPpro-qqmCagliFkI6nrmK74bpGtlwjd00iFwVbGoKR1M8T7PPG9OfL3zk9d-frehuRtVExHHQXQ6twxafOYqLpTDet2mTfKFmhxlEkLmB2QKA4d9mDMzGVWvToWOXW0W8k3G0FDkCDys0vxxqdh2ppiP_ZU0mSQrm8Ci6_WqvJ05D1muFAYbnYANeWlLnbtXqfWTbi8OwlkTjycNV_nrB-24e4Jq0E0YbfyTuusNFYNSpAgW9iFJg4qEpzlgihwhc1FDoMOkL2qzSwgYE3LBqnduQm1DVEO8RYYGtO8hi7Nt4B8jMjfxcDEO-N6hSRwhOSLz4UQ-zh1GZvw1hYK0m0yXsZlr7T7gza-X3bfj7E2vTOotUj54RTlZ2yvlxHZIVH0ybrnrLaCFpprT9Z1uJglZRb4846GPUWTDnuGtqK6nBIzZDvta9Mov2zpx-Y3GaolFXqVKYOGfrtBfKiIgRQObxZAyb4TZ4rOFCSlTEAXOD3601UFOnX2faastf4P2RgA0PCMgfblkWq6mzzxK0JzHFwFIeBnWIj5NyX2WYUxhATYxLIxnZuGJaMhfz1Uj92b8lIDnb0Y77ywWJrM_WEzQkjPyqt-tKVr-ZEHGGcQEAb4wRKfZRm2wxjOERrSI5C01PRzrfLhAsIodvpLgxQt2NvMq27_sKO5ZcLtxL78vL8DEf-7oVDg5_0OzmxQASI_uRVkpGrqKNnplid_XNVopAfvkMMK_W4tGwBz9mM4RXPnCtrBCjn5iUgU3UqBvupgpD-5WHk7gqT-neR4yGuQuNpaAT6Ni5mn3-h7SlpsIwVxBySlMfQVA1CmtEfOLWl6fT8zsP9k2mYiYGasq3gnLbNhp6GDnsIWxtrb2rItaEDusa0RMONtjF2rxPAA3szQzQXnvL3xEEjB2Zu7SZ0tdAvTG_SkdMTVuAMK5hl8aD2jWEPHO34ADzdN0pgBz9fwM3sQ_7NITxWUd_t4ubQOAovRT72AVfvJo9TeTWk0NhM9bV_GOPZXJJO9wlAqfWZhFpuVxlKsX_jlZznhAOyJGus90-h4YDcxUTnpKIcUy_CJGzUnvZhslIJ-E9x8w70akwqG-6c9obbkXygx5G8tBvy8UuhpK1HATEZIRhoAA1TZnmXVObtbcNSKDkExtwsCw9VSrq8yFnd7AdTpZ0F5GOQsrj6wyrnS070iySQBkRH5n9lSSwvari7qmPGXCV07wdIAhU_2fZkZbAecexmT3w1Zv0coyRx7jZ6ZzK41gXu0ERDPkcb_GpKu1x1YtfvlDrXHN4ogPT47bnuE6IoDO3TT9BtvPI27QJEsa4-sShUmzTkEsHCg6UYnFYKrglAtzPwJk7bekcAAkx51htjoHaAf46bqr-SF3yYYRW73_f4x2uyLWsGatvCmuuNuf7N_TLHIm72cIgKsCpBtQTVeD6uPTcEbMb7y_2chOch6Vc79flL6KFkCT1Kwva04xCmNlm-iM_5RthFLAuVEzo3en_x_dm59P0UuouTdgw2igGo6ynOOngCzo94-gqijXtKR0rLntCnU57WONc2V0zhAwULpSP--7k_e-I2dl_ZJIMacJvcgPs8Br_aPxUjq7i-1ZkO6Lek5f6K9NhGnWE8ssPIHu5RL58CuhyLuvY4sOALUYao6DdaOIhC9Aorr9SXqbIl1Li7NEn_wUgnqONhX5m_d972TEZorpNIs4n8dTpI26oh3EXJiQQNk3Bvg81iiiwucBvx8Zeh8azP52oAs8H2ULgvSLAPpn1hu_ZMLe6BNyc2O3DANdUNWUYx5UkIOrJfcxHkh-UnTIE3Ju2CKuzc0Rv-8Ajo1AHteBdO5oHHBVb4qtHEZ2BruFmuHNAh_R2l6oi-6SOC4sxVGFZwXBQMiy30C_MVJ5e2vOYV1Q9-fPi5mA2O5wCNhIyQbBouuQDUbhg00srsrVKZY7WSmkHw74nfxVZBMoEaL547APolySV9tz_zoB4n84HATcOsK0O9k791snKr9zE1wkOB6LPPApvXmWAiMJ0IncqVI2LH7s6TDDsXGZGiu_YrHO_Ky5w_CB53sucWADcBlUt7Lf-Qis-DqwRHjFcYYvjj29ncoUSIO9XdE-AL-As5aEznA1MZ7QRUECYzoM92sFnPNtNGTyc1kxWEWX-VGOU5M2BbCJGBdYoUdMyCKxX5R120FcNJdCIb69RDZMmsbP5MIPOLiCWrNqVUzxGRP4xrk_-P_zLcDGzWgxUQJAfNDyKBSYMJ8HjVG0MFwgHSiJvdjRHCSEfSYMuyaW12HmWhxD-u0AivVcQnur_ItKJoF7ehIkWWUUBxOw2jZTUUyq6ZN-2eiML6pE05v75urYrmDEFS3Uh4NqVjB5TiCCNJrEqAdHDqF4UvT70I6FSB1FEwra_xLuaq5HgUGExK3iJBC5xNwqB3DSe0fJYo7Wpvp6h3UK7u3qeAEwe6pdoZyxzAgyhtzRarZP8EYvPC53k75wT7xoF99ShPsPE2sgSK6E52Tc7i_Nk6YiRcCBuoYARrX3b75eCISMHt5CI1TDa6u5TIMn4LROUkgNPeJi7YQXl4kPnFbVwMU2L9uwD-j1Tn41v2ZJ7pKlsqDmWUQ7wVYE9Jpa1mDW2r5oOUJT13RcbbuVlW990NJdtPnh-S3pqPszxrcVjkQ4MaV_BLi7__hMpu6YvebFKQ-AeenZAqn_qh-LQofKLB0kJAUCLGmd1gckXhYdkEI7J0b8mbmai',
}

response = client.tls_post('https://www.kohls.com/cnc/giftcard/getbalancejson', cookies=cookies, headers=headers, data=data, proxies={'https': PROXY})

print(response.status_code)
print(response.text)