from riskbypass import RiskByPassClient

# -*- coding: utf-8 -*-
# 由 RiskByPass 面板自动生成
# 依赖: pip install riskbypass
import random
from riskbypass import RiskByPassClient

BASE_URL = "https://riskbypass.com"  # api端口地址
TOKEN    = "your token"    # 访问令牌（作为 x-api-key 发送）
TIMEOUT  = 120                         # 任务最大执行时间（秒）, 超出此时间将抛出异常
PROXY = f"http://xxxxxx__cr.us:xxxxxx@gw.dataimpulse.com:{random.randint(10000, 20000)}"

client = RiskByPassClient(token=TOKEN)

headers = {
    ":method": "GET",
    ":authority": "www.arrow.com",
    ":path": "/en/products/verdin-i-mx95-evaluation-kit/toradex-ag.html",
    ":scheme": "https",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Google Chrome\";v=\"146\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "sec-fetch-site": "none",
    "sec-fetch-mode": "navigate",
    "sec-fetch-user": "?1",
    "sec-fetch-dest": "document",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en",
    "priority": "u=0, i"
}

response = client.tls_get('https://www.arrow.com/en/products/verdin-i-mx95-evaluation-kit/toradex-ag.html', headers=headers, proxies={'https':PROXY})
print(response.text)
print(response.status_code)


cookies = {
    'arrow-country': 'US',
    'platform': 'nextgen',
    'affinity': '"0b474d85b36c9ad7"',
    'AKA_A2': 'A',
    'bm_ss': 'ab8e18ef4e',
    'bm_so': 'A29C6BF27CAB1FC43F2DFB6EFDC41D7835B950244418FABCD96E95A6BA4445E3~YAAQSw7SF3UkPPucAQAATgxcEweOjGHA8PgjInCA54zBPeLYcIv9LvWaw5vw5YzgMNDMb2Rge4YEIKECIUDRsiQNcW9QRn48P3kZhAIB/XkG3q+pUor81eDAVW1RwVePVSPrb9Hd3DznOtCuaY4sP6hXj74venongExpqmuohVgCyTxumKZM1Jlq26kiP+g5wfd8jls782nQRB7G/Jp6qgJ8EhKucuttApPpCrWbCs4otRNK9NdYaFVHLC0xJxQn2k34Sw9xe6Ej8ps0p6j2dIGs8LVroDN5k+C/z411rEvRjNynOfQuhnBkUufKrpjxtg/yEDo6eDwmYJZdQ8WtvsYLy8QZZY1Z8w+L2BbabYuhuzCeHNWWWI5OM3eHB8ETTxUdyRX6tR2bkMhgo8+iyhSUF5XRE1Ws/U6c3pAMERzVBbnD3hD2lMMLCubK/VhoJg6kjdeSVUkiL1Yy',
    'bm_sz': 'CE407B7D0DC0B18962BC77C9587EA438~YAAQSw7SF3YkPPucAQAATgxcEx/yynS3wBxFFyjof4Ex5x0kc2B0bg4/NUdH3Uqqf/mpF4wpimK+Y78fypxUHTsMzXDn/riFavUdf++zcasLhN2cKlTVvHhD2A1gOqQtiUwmsVy8mKSJtugBBHdlmPtB3Jm3gjlfxT0SUArx2x0HqcDiy0hGJ7juXIk2zJ212jHF/JrPpIFBXCXhiw2DHbRIC3/Oey90Gof9dRgVRlqEVC/v8q/ItNp8e2/MdnaS9JrpNAcTLgnsHg2KRh0Q6LP2xJFSqzEaIBsE96PvZujhOXS9TZLF8tzvHR7lFhAQymnzyMGJ/YH5q39582iFg9KCORT6F4kiuz4kwVggqsSIbva5M1wTgARAoUN2fygr2WRrIvm8QqkH+kA=~3551542~3425337',
    'bm_lso': 'A29C6BF27CAB1FC43F2DFB6EFDC41D7835B950244418FABCD96E95A6BA4445E3~YAAQSw7SF3UkPPucAQAATgxcEweOjGHA8PgjInCA54zBPeLYcIv9LvWaw5vw5YzgMNDMb2Rge4YEIKECIUDRsiQNcW9QRn48P3kZhAIB/XkG3q+pUor81eDAVW1RwVePVSPrb9Hd3DznOtCuaY4sP6hXj74venongExpqmuohVgCyTxumKZM1Jlq26kiP+g5wfd8jls782nQRB7G/Jp6qgJ8EhKucuttApPpCrWbCs4otRNK9NdYaFVHLC0xJxQn2k34Sw9xe6Ej8ps0p6j2dIGs8LVroDN5k+C/z411rEvRjNynOfQuhnBkUufKrpjxtg/yEDo6eDwmYJZdQ8WtvsYLy8QZZY1Z8w+L2BbabYuhuzCeHNWWWI5OM3eHB8ETTxUdyRX6tR2bkMhgo8+iyhSUF5XRE1Ws/U6c3pAMERzVBbnD3hD2lMMLCubK/VhoJg6kjdeSVUkiL1Yy~1774146293577',
    '_abck': '14343FEA3A2984D98D6FF42AD1B9779A~-1~YAAQSw7SFw8lPPucAQAAHxNcEw/vE+WfnyQYSOjiIMKBscm3AxvzQJk6mVF8r/AGska459o+iE6ZxwYS0VIA8vF7Tx+9YXETDRjvGp066OVLU9cgDeodthZzy77FH6vWIC60QghwTFymk+2RNAW6ExshU6miedodaYL6XwEh/il9O6diHsgUzXHyRe98rizByxqfAoL1elANDrnLQTU+15bRet9GlssexKXHzKDf/CYYL57y//5PwcB3B/B05MEYskkAjGSY63P9yFR9eoyLS9n6oXDw4fbegMnaVwJMSwxttQ8SsUaAR7APTCnLqn27rXBgfRGr0ZjbSTNHY1bL1TM2ZcqM5yduyuzggsvn1ZAIsiezCHdnAsG4BgI5ql46rza9zMuTKa2Qyjr+JSIWaksZroXOn+p1oaj77I91tE351eZ+fovCPgF/Oj2QLhIpovH3BUdB44+5TrlWoaCZVX3nMujLhjaZkmJLDvjsM+JKHIK6NKckYfhzXGW5RmEElmhrn03JF9aEj1kllFAEWvs8jJY4FhmExi8TUH5NrMCx6y++QJGVbpaixf58C23U0UV34xBx5OqWiUYqEj6Zr5BII3I=~-1~-1~-1~AAQAAAAF%2f%2f%2f%2f%2f72MfVGiSr%2f8285M+INnn77x1hXYDMY3VKcfQ9iU1R%2fSsX0wy5e0r%2fMLnxkSdEeTUU1yf4h91yVhDpfdT7JER%2fPYtvKXmNpeJztA~-1',
    'ak_bmsc': 'DBB84969CA206A08D4120E77A925AE50~000000000000000000000000000000~YAAQSw7SFxElPPucAQAAKxNcEx8PNWnOi+FudoHYo3OYfI7JHma4Zjq2chYY4/BZptqc8KRnYKqn4F8B2UMZcZEqOu3/wqRkzEWW0IENdlSSgGr3HuHZVGWnciQmmtq22dpv10q5Z2odA6deEQZbkeBnbzHJf3GjFsOcJKQ5PvJnVFxJ2Pst49FmmY6hUOZ4MC4ty+Oaw77GaL1kLVtPoGfJzaomoTWCmD1UawU0Gd8Ag0UENgpVlGecpIVEqwfsr5f+vmPcLJ0YaboGw0/E21JaC80ScKYg3GVKEkgpbg1jGJJQ99WMCY/6WXy/E/gk9gRw5SCkMYdFup0OzTY0EmzRjhBlarJZv6pRxl956et3SS3STDZ6K/xhi4R73AGDZFuB4UyQAjgf3rj8GJ4nmMfjNOLIVAH52XbaB2v6obsBAE+eFG/xDs/a5vY692TKxnjgqg==',
    'arrow-currency': 'USD',
    'arrow-lang': 'en',
    'bm_s': 'YAAQSw7SF3UlPPucAQAAUBZcEwWkE1t4i3SdkVJMAxk8zMegknmMcMQ/SmnIKZd3SsJDlH8Kut2H/HOdKEIhI5KvWLO95zznUiy9uI65vf29Tr++ILQndScwKGhTLmDkocX5qUUjVaeseIux3WjwQZ4IdJxbeF5xCLENiBJWa1mimyhQn81KLDd5djvT7wU6E2gf3h3k4wBAvIlN807ZEZ8ncIO5GF1Ucf1M76DfRm2bmn0V4vDZALHoH2pExjKpfENMUfNSHgPohPvycb3T7WNC3fch//gIs/jCbRgOjerqgXGT45BoC0J3Ez5TwVmAspnpe1s10uNETEiweNQ5gS7SgANZEguHaAeJ0kwXWvJsocA/UszrkbpVzqrC5jsKZb67/WWgk8CEpEaYk3E2n9N2uoRF1kjgxBwihe/2+PbvIJQrgliop2vWs0uC5xl/GNMXTsp2qu0sLCRAnRyA2mRcF5VW6VFsKngMro2yg7Ab9jYAygRsD9Jqb60BYI6WYC6qkWGrAGaeyPO4yowAho5KW+F+eK42FtDzKrx8G5udDk3EEYvVVBqmjkYXetKrte9jWSM8P7/+eYefjL3S3eZxdi57ZqRgKmGhO5DOstT3iNliIPAmU2JC/lXpyUX+dWvRZl681y8C7QN4nlkUwk6/tYZ8uMDVVba7GJ2/EKKDF+rM9ftm5pZgkhGKc63MJzpB28XjgWn/V/8RMfrrkCBi+23rC59xRjdbjvPlh4SqwlTq0Uz2RUcYCe9vzmYyZQO5NzpcLdxxvA3s0iAqEx+Or0Axgsw=',
    'bm_sv': 'D528E9EABCDE262B3C3041344AFCFD84~YAAQSw7SF3YlPPucAQAAUBZcEx+mh3YIfNGKYQL8GHrNDUWyiKJVYJxGsDj/eF/27IRxeJ2DSj8CUe17copLhU0UUF1zZ+I++Xi4sxslcmUNnanairUbmRqwWagqSZUlLDyHNXoo3Tc18n/6pqDPsvqvZUkwsmwLquVSa9QnR55RlKNNqWwZzjiTIY9ldwgt6Lmh7NTV45VGqzN8hX7aVVz57QP12UFWtNQWlcJ2Bpa2is9KXAopto//QsOJGmw=~1',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://www.arrow.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.arrow.com/en/search-result.html?keyword=ad&currPage=1',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
}

params = {
    'countryCode': 'US',
    'currency': 'USD',
    'lang': 'en',
}

json_data = {
    'pageSize': '',
    'currentPage': '1',
    'category': '',
    'manufacturer': [],
    'searchTerm': 'ad',
    'sort': '',
    'sortDirection': '',
    'filters': [],
}

response = client.tls_post(
    'https://www.arrow.com/experienceservices/search/',
    params=params,
    cookies=cookies,
    headers=headers,
    json=json_data,
    proxies={'https':PROXY}
)
print(response.text)
print(response.status_code)