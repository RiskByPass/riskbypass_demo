# -*- coding: utf-8 -*-
# 由 RiskByPass 面板自动生成
# 依赖: pip install riskbypass
import json
from curl_cffi import requests
from riskbypass import RiskByPassClient

BASE_URL = "https://riskbypass.com"  # api端口地址
TOKEN    = "your token"    # 访问令牌（作为 x-api-key 发送）
TIMEOUT  = 120                         # 任务最大执行时间（秒）, 超出此时间将抛出异常
PROXY   = "http://username:password@ip:port"

# 任务 JSON
payload = json.loads(r"""
{
  "task_type": "akamai",
  "proxy": "http://username:password@ip:port",
  "target_url": "https://event.thaiticketmajor.com/user/signin.php?redir=/index.html",
  "akamai_js_url": "https://event.thaiticketmajor.com/TsNvq6/NVC/kQP/5Jl8Ng/miu7cDSVwNfQ6w/Vk9uag/CCsxGAUr/FxYB",
  "page_fp": "424543475255404d4243475d5f5a534a5c5148435e4442475355404d5e425e51455f4e494b505f5e4345434752555d505f4b4a5a5f5b59495c4c425f424543474f485c5945475e59485a4e54414d435f42455e5a4e4148525f4349595f5b4e495c515f44455e5f5e50495c5148435e595f5b4e495c5945475e5e42594e494b505f435e595f5b4e4148525f4b415a5f5b59485c515f435e595f5a554b484d4a434245435052555d505f435e595f46535549574a5f425243474f485c515f435e4442475a4c434d434842455e5a4e495c515f5e4345425857405c5148435e4442475255404d5e425e5845585455405a435f4245434752555d505f5e4345435052555d505f435e595f5e51415c54404b5e59485b4e54414d435f4245445e52554754435f4252"
}
""")

payload['proxy'] = PROXY
# 初始化客户端
client = RiskByPassClient(token=TOKEN, base_url=BASE_URL)
# 运行任务
result = client.run_task(payload, timeout=TIMEOUT)
print(json.dumps(result, indent=2))
cookies = {
    'HWWAFSESID': 'a94d18b7eb600309e8',
    'HWWAFSESTIME': '1773297851491',
    'PHPSESSID': '48f44d7a7407ad66bb73afa019b81982',
    'ak_bmsc': '967B7673E7C8891502C81CEDB81633BE~000000000000000000000000000000~YAAQlmrRF4h7eNCcAQAABuPJ4B8CrKBQ7h4Vp1CRHAn5D36H345fd7vmZPW+j9wtFugtSZbozJYn8OdqVnhdXxLqOSLcAbhN5in0Hap5Lt2dtAZBihx9Vb4MvtOBejmmm0zrX8z8YtlzmHd5hRzNqJhYbvXpMsTyhLYiBi+4x6TCPmVNT6DY8I6KRS32opSNbAlc5nsNSOwrPGKFXhljFDNgxnTFxOlgM+tt2dX59fns1wUPmEcV6Vq88hvfpChmzf2Rt8PEkmPj2C8x3fLOOT48dvJ+mNd61pm/Qsd1623MSk082fWkJibfxMXP42o9X+Gnem+AYleH8Prnuga89NvRjllsX4EdMJsTZQ/Zy6N4VMnZWEmorVb90uRV4KT4k13Z2rcQPUDZDSIozDQ/2xNiVs/l',
    '_twpid': 'tw.1773297857211.920352543105906264',
    '_gcl_au': '1.1.1652339420.1773297858',
    '_ga': 'GA1.1.1091785676.1773297859',
    '__lt__cid': 'a4029546-0df1-4a21-aaf0-14cbd629c991',
    '__lt__sid': '7258c9d6-a5fdc69a',
    '__gads': 'ID=dce2c4f2faf8e899:T=1773297861:RT=1773297861:S=ALNI_MbKDlPj6kuVr_gAtJ3RTgP991NFsA',
    '__gpi': 'UID=0000134c7a942853:T=1773297861:RT=1773297861:S=ALNI_MYa4N555aQdsKPd8QtBgl1VjLAAOw',
    '__eoi': 'ID=bf7128491e5e00df:T=1773297861:RT=1773297861:S=AA-AfjbilL9xPmmL_IcoGEaeHo9I',
    '_fbp': 'fb.1.1773297861343.606163792126931193',
    '_clck': 'hjf3b%5E2%5Eg4a%5E0%5E2262',
    '_clsk': '460up%5E1773297862898%5E1%5E1%5Es.clarity.ms%2Fcollect',
    '_ga_VQH8622D4L': 'GS2.1.s1773297859$o1$g1$t1773297873$j46$l0$h0',
}

cookies.update(result["cookies_dict"])

headers = {
    'accept': '*/*',
    'accept-language': 'en',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://event.thaiticketmajor.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://event.thaiticketmajor.com/user/signin.php?redir=/index.html',
    'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

data = {
    'email': 'sadsadas@sdmk.com',
}

response = requests.post('https://event.thaiticketmajor.com/register/checkemail.php', cookies=cookies, headers=headers, data=data, proxy=PROXY, impersonate='chrome136')
print(response.text)
print(response.status_code)