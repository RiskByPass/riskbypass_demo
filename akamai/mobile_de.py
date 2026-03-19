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
PROXY = f"http://xxxxxxxxxxxxx__cr.de:xxxxxxxxxxxxxxxx@gw.dataimpulse.com:{random.randint(10000, 20000)}"

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

params = {
    'cf_template': 'OTP',
    'source_uri': 'https://www.mobile.de/',
}

session = Session()
session.tls_config = TLS_CHROME_LATEST

response = session.get('https://id.mobile.de/oidc/authorize', headers=headers, proxies={'https': PROXY})
init_cookies = session.cookies.get_dict()

akamai_payload = {
  "task_type": "akamai",
  "proxy": "http://username:password@ip:port",
  "target_url": "https://id.mobile.de/login?service=https%3A%2F%2Fid.mobile.de%2Foauth2.0%2FcallbackAuthorize%3Fclient_id%3Dmobile_web_DL1WJUPw%26redirect_uri%3Dhttps%253A%252F%252Fwww.mobile.de%252Fapi%252Fauth%252FloginCallback%253F%26response_type%3Dcode%26response_mode%3Dquery%26client_name%3DCasOAuthClient&lang=de&cf_template=OTP&state=eyJybmQiOiJqTEExUjZ4WUJlWWZvcEVhUXB1V1JqdmxZaXkzay1GN2RzNnpFS0p0c2dNIiwic3JjIjoiaHR0cHM6Ly93d3cubW9iaWxlLmRlLyIsInZlcmlmaWNhdGlvblN0ZXBzIjpbIk9UUCIsIldFTENPTUUiXSwiY2YiOiJPVFAifQ%3D%3D&nonce=ft3dmIBls0tvjCFgTUDn3X3IDw3-EWhqbbMsnp3bWzA&scope=openid",
  "akamai_js_url": "https://id.mobile.de/_bqyfuQdffXjx/Jz/GO9kf5hhPMF8/ikuYhXS5Ei7Xwk/SWMRIi4B/DT5EXwNA/bjkB",
  "page_fp": "424541475255404d4247465f5f53544d5c5148425e5b5f5b4e495c50474547454b535155405a435f404543475255425342455e51455f4e494b505f415e595f5b4e4b4252465f4a5140475242"
}
akamai_payload['proxy'] = PROXY
akamai_payload['init_cookies'] = init_cookies
akamai_payload['akamai_js_url'] = 'https://id.mobile.de' + re.findall(r'<script type="text/javascript" nonce=".*?" src="(.*?)">', response.text)[-1]
result = client.run_task(akamai_payload, timeout=TIMEOUT)

cookies = result.get('cookies_dict')
ua = result.get('ua')

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://id.mobile.de',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://id.mobile.de/login?service=https%3A%2F%2Fid.mobile.de%2Foauth2.0%2FcallbackAuthorize%3Fclient_id%3Dmobile_web_DL1WJUPw%26redirect_uri%3Dhttps%253A%252F%252Fwww.mobile.de%252Fapi%252Fauth%252FloginCallback%253F%26response_type%3Dcode%26response_mode%3Dquery%26client_name%3DCasOAuthClient&lang=de&cf_template=OTP&state=eyJybmQiOiJqTEExUjZ4WUJlWWZvcEVhUXB1V1JqdmxZaXkzay1GN2RzNnpFS0p0c2dNIiwic3JjIjoiaHR0cHM6Ly93d3cubW9iaWxlLmRlLyIsInZlcmlmaWNhdGlvblN0ZXBzIjpbIk9UUCIsIldFTENPTUUiXSwiY2YiOiJPVFAifQ%3D%3D&nonce=ft3dmIBls0tvjCFgTUDn3X3IDw3-EWhqbbMsnp3bWzA&scope=openid',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
}

params = {
    'service': 'https://id.mobile.de/oauth2.0/callbackAuthorize?client_id=mobile_web_DL1WJUPw&redirect_uri=https%3A%2F%2Fwww.mobile.de%2Fapi%2Fauth%2FloginCallback%3F&response_type=code&response_mode=query&client_name=CasOAuthClient',
    'lang': 'de',
    'cf_template': 'OTP',
    'state': 'eyJybmQiOiJqTEExUjZ4WUJlWWZvcEVhUXB1V1JqdmxZaXkzay1GN2RzNnpFS0p0c2dNIiwic3JjIjoiaHR0cHM6Ly93d3cubW9iaWxlLmRlLyIsInZlcmlmaWNhdGlvblN0ZXBzIjpbIk9UUCIsIldFTENPTUUiXSwiY2YiOiJPVFAifQ==',
    'nonce': 'ft3dmIBls0tvjCFgTUDn3X3IDw3-EWhqbbMsnp3bWzA',
    'scope': 'openid',
}

data = {
    'execution': '4920f141-bbc0-4c71-9d83-6f2b31d6a35e_ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LjVoeUwtMUdLVE9MdEllNmQ5Y0NZOG5uU1VIWFVVc2VkUmExeU5fNWVRM1IzcjhZNXFMdkQtVG4xRzhvLWdHYVI0UnE3Q2g3bE1oZEZLZTV1VzJkSUdkZVY3YnBMZm53QlU2WndlenJBaUtYZUU2bHdXZnpuaUd5RlhQdVJiQWJLcFVFSnFDOS03Q0tnLWp5VExwR25OMFluWlZ5eTE5dTRCanFxRVZPS1NTWWVmWjUtVFVwTFJ5Z1M1SWR4QktIYnZKQ3RoQ2NidjZHX2s5cmtpZHM1aTd6bG0zVEE5YTExVVBIUGQybm1SMFdpVHdQbkVBaW82c2ZSTlhkczNkNTJFMnZiYTBJOFZFMFg2U1dvX3duR1RxNV9JUWs1eVVQQXB3M2FPbzgwT21DZzN6YnFocHE1TF83cXN6dHN6azZ6QUhlS19jOEQzWTFsQTd3NmNDUGt5RXRleDItXzhTM3Z4UHg2cnhPUExTWl90aUY2N0NEcFJ2WHY2bFRrY2I3a3ZadlFGTFA2Sm5hY3JnRG1hUml1MlV2U290WWNhREdUOFdGZDZfSTI0TFBFa1FYTHVZUjJiZGI1ckZQNHFzZjBqYkM1cVlOMDlDWVRLWE4yQmdmQTFvVWk1eXllUzVDOGVHd09lcGU3cWRaTVpaa1J5enplT2RkZXhWd1JpTERZcXN1VkpNaV9WNnhXVmhaM0VyTUtRYjVvalFhRmJoRGxoYmw0ZEQwZlRXcDRlOWtYVkd2TjJ0Y1RZVUFiUVJ1ZHpLN2YwSmN0ejFMMEZkWWp3V0NjRXVCS3NlUEVlYXZSQW93QWtrRS1BOEtMOEs1WXVSQlJCY0VxZk5sZzZvU1pyNFNWbWFUYVVTcUEtbUp4OERSVGk3NDQwUXliRDdzbk9SS1FidzB6SnltQlROcTRYZGsteF9ZUEJIOU43cVdVTDNGTEZrdjVGMEpZYWtWdS0tVXM3cGpfTlpnQm5jVzU3aVhSbHVaWEJpQjhvVzlTNVcwRlE3NzdqZFZKSmJjR1cxUWJ0MGRkVG50akRCLUVMUnhaNGMyZEVMeG1ya1dKa252UnItRFEtMHhVaXYzSlZBNjNVN2tDZEpOeGJFeU5DODQ0b1FpMkpGbmVqYTJUUHVtcXNMaGFFaHpIUW5nWWZ3YkFfUjBISTBOQ0hmbnVwOF83R3p5bXdZWTM1Qnhld29yNkUtdEFWbU44VzdlZVgxRTJlTDZTUXZJdVZGYzZnUW1RNFQwRzNzWVlWcjRXQmpmc3N1a05sOHBFc1ZVU2V0VjA0a0FvWVRYdDJmd0E1WUZKU2QwNlM3bkZDYjlNUGhLaEtsYTdON2ZDZ3ZwOGl5Y0M1OTRPWF9LVUJMaXk1SWxQbVEwUGZOdlkyYlZsVndkem1zZG9LUm5vLVZIU3RqcDA4ZFczR2x0VGxRRXprUEk4WE1pcWdyME9sMlkwYnd1TzVvWkQxRGc1WFdIbndJa01kSmN1R0hmYUpHalJVZjhaZ0d3U2RHMWI1dW00M1doXzdXb3NCTlh4Q0pjVlVGZzNRd0t6LUl5VWVvUUpVb0RCS0tiSG1lQnBRUHRjbkdNUU9haG9wS2RMT1pGcVBqZHI0MWdLMlVVMVloOXlSWldWOV84TWEzNU9YMi10ckJzQ3lPNkliT0RoQlNwZ1VIeGRWRFRRVVVfZ0FJZGl4RTBNbkV4YUtSc25VVEoteTJNcGRPbjg0cEVVUTIzYmpPS1pfbzdEYk0tOHdTVERGMnpkVDc4bnMxX3ppVWVwZXRzdU5YTmNZeF8zaWRBUVhBblc3QXVLTHhFMzZrVnBNczUyUXU4ckRBMzB2RFJiTWxRLXhXYjd2NGM3S1lQaEZpaWJwdUF1eGczZG9pZGM5UkFYblYzV2dtemxhTU1jdDhyeDRqMndlOE4wNmxHV2NMbU9iYUlBQ1NhbjN5bHlNQXFwdlBWOFdOOXpYQmJvNUxLRmJoRlJlZlJIUU9ZSTF0Y252b21uTmpycUo0V0diczBzYzdRSU1MOFRHdXRJUk84TVBUeWpJR3BNNnNyMG5EWURCZ3dfRXE3NmptTFFvUFFnMUQzb2tGbDZMWFQ0cWtlTGlEQUozWDVJcWVvY21xTGF5RWtWV2pOaDhJX1RVUFN5TWx4d1FXU2IzYjgyVDRNZ1hmWFFrbmxNa3ktaUdYVVlUZzE3YjNhcXpna0FqNXVKdUV6SWlRb2FpdWI4SHJYeDFEcUtuN3AyQ3hMZjJxMGdnTk96MDJsTzBwa2hzM3dVanhEYW1rUWJPTTJWb1ViU0FTRHZxUGlEM1BMM2pGOXdJVTdDRlJPWkdxUVVSUVBUWldnYkVWQXdHc0tJcWNOUGZ6Sk5Qa3FNZUx3aWJmeVpuQ1dFV09TbFpJdnJmLVZySkpMVnNJT08zV2JrQ3EySkdXNk4ya0hvMFFoUE5HNEN1SjBTbmxxd0pQRlVIb0JfTUxCTmMwNVFPaHNmRXVuUjR0ZkU4bG1CaHlOWkFSOXVENmFWd2hsOGFRWmJiN1h0QmNoYVhseklfYXhuc294MTI3Q2wtR245X1ZHSjJBZnBLYXo4OGc1S01Ga0hXbEc5NjNPemdmUFFmRGdwbGYxdlhQUUNnaHF2Vmx2YkNBVk5ubG1sQXBhbVpMWkszaVVkeXJBbk9ySjNLUmNuWFZOdDV6WUJqak9rYWZNX2NxSnhZcmRsdko4bWlDQlR1cmhDb0R1WjVfNVRoWlRTN0diU185QWRoNkZ0WTNrQnRwNVdzeW1kZFhzRGNGWThHeW5FbnpvZkdiTjExRlUzWTRfTDFCOUwtVTJaOVNRX3ZEWk5mXzgtVFctd3NKXzMyT2FxbWRORTZIRVk0QkZYUE9oZXl0NE1nSS1kdk92NjBZRENoTEJTTHZSbXFyMklFMW1YYjZjVE1wUDJnenJTcHh2bFBTNFJuaS1GT3lLX3QwektjM1VtSTdQUG14Q0xNWHlUbmRhNkVIcEZ1Z3pvbTlaZDdsb2wtWjZvRVJpWTBmR2lCYm5PZHF1VUVZTjFuSThQb2JDLTRyZXBoNzlaWE8yTDZoTFhFWHNNRWlIcnZYVTVCUUlRV1JXZ3J4SUNFZ3lTVEVhSlJJVU5ieW1DWDg0bXpHSGVYUnBZMFFYNGFGVWlkeDJsZzA5RGdWdGllQTJmWlgtclIzUTQzN2UtVlNFb2NWTjhjSFFib3ZWb2p0N3BMUm96Y0REanVWZm0tR2JyYnk0ZGtnR3RSaU4yRFhHbElmTEpyRXkxTXJDSlZ3YUF5aGFkLVBuejM4SE40LU5keEVVOEI4TkZYSUJ5eENWem1yU2VOOHZvZ2ZJUFAxZEduLWotZkwyYjdSbm95TUxEclhOS2RrT3hRbkJHTzJPd0tNX3RJeGtJdjJXZEctNWpPYXJFRGs1Z29WUUVNVHRLRjQ0RkVJNHBhTkJIV2s2c1pWZC1YaGhyTnZBLUVNb2RXVXU5UVhJWDZyQ0N5dnNfZVR6RWVLU29iT3RXbnpiU1hYRkJ3bnNGMWIzLXZmUTVvZ1Q3MVlfWTFoUEwxRnVhb2poVi1xNmtvU1hMZDB3VVN4bkVMa3A4UWpsTGpBNFFmalp6anBBZzdIZGhQNEhxZUVabzgwSjctZGJ2ZHdNd1I1TS1QcHFDVHJBWFZEYmhnbGRIcjVwRjhwYWFXZkJZdjdXVWN3QU1INW5XckFsQ2dzMkl1RmdHOEsxMC1Mb3ZPRnQ5ZVNkMEtaQ1gtUlY2NDNMQ0NGTkljazc0MVhPT2dSOGhsZG1ySUtIZEJoUEhYWHRnaGNsdG4tWjh2X1hPYW5WS1NGVF9sOVZFczR3Qm9pQVJzR3MtSC1GSmd2RHpLazEyZG1xTWZ3emRYc1ZySkpLZHRYQzhwT2VjYUs0eFJTa0VNc1lJZnJsaDdMMV9fZmh2c0trZ19lZXZnMUVoQ2NYdkpVM1BsUVJnTHdCSkdtR3RoN0MyejM1eTRYZUp6NU0yS1JuX2wxS3BpUHdSTTVxbU9jS2hYazBDSDNRc3JOc2ZOU2wySE1VQ2tJV0JFZ2duaThwM2pYaC1ZOXBKUExwQVB5ZFBCWWx2TVJFSDdrSWx0REFpdzdxQUpwN0tIaWVqZGxkU2NxeUhQSGFFa1FWOU5PLTJwb2lKMFdGNC1LTWZrM3RfOGM5b094bGg1UGtXdGJOWE5IRnNRQ0o3d3dvcEVPMVZzT1FJRWVuMU9sc2VTNzB0Mk1LeF9MVG1oRi1vWFNRcTM2MVpUSlVQM2RKaG4xYm9nbFg1dmJkTGJmcTc5aGlwMlJrV3RPZnFfcHc0VGZ6ZmN1NlU0WnJucUtOU3ZySFdVb3AyUDVYU25iNVVyZXhmSjhraHdubTM1eWwtWl9ENjJtNzZRSmJORUZNaVYxcVh5VTRKLWVwUXoyWm51NDVjSzZlQVBUc1VnWkJZYU8ycXJXMGx2OWcyV2Z2dUliUzJGSG1yOUhlb0FYTnVrMTRLaHlLSkN5RG9Db1Zha1ZwcjRscEFHWHB6d3FMZzR2d1hHVWlnVjc5NHV5R24ycUJpa1locE9JcUNtYVJTZDhRRnVCUnhLeEotdVRNelMwaHgzNXBxV01fbjNnWVRHRWFNOGZ0SXBjMTJkVkRIMm5FTURQVTY2MGVxR2h2WHl3OTl0YUdHQTZFSHhlVDlkXzkxUFZiSG9NUktHbDl6c1BZUGNTNWcyMDhKaHpwSFN1cW12TWpXSWVlcmJPZG9hZF95ZjFDcFVwOURDRmhuX05aVmd1WU5HVGpEazI3aGpGMjNoYVhEY08yMWZGNlNzX0pYdndiTmF0d3pVTU1yVjlvdnUtNkRIVE1sM1FKUEV1NXRTNWxRV2JoV0tQTHpLM1VXNXRDNU5wTHgzVTZxZ1ZOeHYzZlo0UjBweFNCMXVIdG14X1VHeXQ5QllLV2JXVnItYlJyQ2lZVDAxdTNlSmppOThTVVl4Z3lvQTBVUEJPY1NJZ18xX3ZBODNJRzd6WC0yeU4xV3ItTGM3dUxLUVJ5NUViaVhUcldjMmJHMHFjenZDSXQ2cG54RHViS3lDSlFLV0x3eHlMWUo4cmVjck1OV1JMRVFoeWZ4Nlg1MjRRN1hYalFuanhBLVNVWWtOT0Z1VWpIVFNldXgtUGtyQlZocG9YZTBhMGZmNk05LWhONldlV1o2OFk3QWhlb215MTk4SHcyeTJDU0ZjZ0dwMkEya3pldFlmS2VXb256OXNtMkpfMGR5SjJTamFCMGpWRlpHRXh2RHlZOENfZmhfbGRkdm9GajJLTlhZWVRqVDE3ajZfbjBzalFkRVd4R0s3WFFoMy1nSFBFcE84ZHNpVkxJd2tPaWxBUUhBZ3lHQU5VcnJvRWZteEh3U1B1WVM4VWR5TTFELTdlOFFCWHRpb3lQa0RwRms5ekRTdlZ3RjZYc2xJSHl1eW1vcGZJMTY2MTFqb2FVYTBmdTFiMmM2TUNOdDh2azJocnlTTDlFUU1NQ2pkenhURGlyakpqV0pYTlRaZ0I2eVJ4MFZjanVQVTZyWlJSNngyMElSMENsRVFJbTRzbWFURlZjaW14SlNTRUVTNHF3YWh2U2hVaWVlVGxicWRNdmRmNEctMjVJcTZRV0lldjJ3bTJ4eGpaaHpsMldYRVJBVUJORjFYbGItMlJkZXdEY1hZUm1tRnNxUFB5UGNpbVBIVGJSMV9wZkpycmZlMjVpckRUeUxlNV9XMFZ2Qk80bEpldHBjdUtLUlRqdjUxVEVCekpkZnBwaWFmT040d3VBU1F5bWwwT3huY0JnZXh2dWtVT1Q1NDdXa2tvc05ZUjRZOF9USkJBc01sX2JsSE1KNVVRQXpEVE05TWNlQkJCVHVzaGVnTlZNZkFMb3d6c0dTc3dMVmRNNUxrc0hBOXlMQVBXU29Kd1E3NGIzVEJUajhwSm5jU3RsYUlYN3pHbHBoc3NjWnd0dzBuQUNfQ09kR2VkdTBRWXdsUmZGYnNvQXRYblpmWWpQRHNzb0hFeHhqdXNXTnRIek9QN0hrS1owWGVLRFN1d3hEVGcwZlNSYmtOSXRWaHBfNzRqdWU0WDBUZHQzY1Q3c0wtQjFod3FVTTlOQUVjVEtWcU5ndWs0dXF1SzNuejI4TlZkb2FYaEE1S0t3cFUtZVlhVDVqWmZvQTQzcWZlTVotSjdfU2dhTDdpblVhZzM3RWw1blMwNWJONm4yT3dub2s4NXdKZEZiNzRDWnQ0ZjVkU1lPZUJicXlpdmwtSFVWWHlEcWJ0WU8xaWhvc2ZqX0Rhc0xDSTBtN0FSN0xweENIc1BVZURXRWx1aWtDUl8yeC1ZcTI5UkRIazRCVnNrdzduaWkwRTFXNmpIQWpMQWk4blZxUDRzM0dCdEFYY24tSGJhcDZIbG9vTkZVYkQ1dWhUeEtvdGFqaFVCQjFOWTVJU0N2XzlHemtTOXNFMWczWUsxUHBKMDgtc1JNWHBINktPbk9ia25Ec3RZRVFVTl9XS05DelJKSFhIbkVfbEtrRkNJbEhIOVlkNkZBclZPbnhpUGVfVUV1M2hhOGZEVU5kTXVBZ2pFUENDZkIxN3Z5SWE5eGo0ekNNVUdDVnlaajBGcW1JSE5BeDNWQWR0MG5uM25QMFhlNURHUGhRb1FKT1RMVkxQaFZMWk1JMXVraDFndDBHbXVuMFJVdGVNRmVRTFlfdVJyX3dYdVFQdURnekFjMnFwbHBYRGt1ckh1YmlqRnE1c3Y3TXF3b3ZEQ3ZrSkNZM255WU9VaTlOczgtX0FTamRvUVNFajdSMmhKR3MyYnNCa0RVRlJHSG1yd05iSEdLYTNrN2piVTZZeURJenJCTmN6N05hamFMYjd1ZmpUNE02WEdpbVZQdUxLdFJfUUppdmZuN1lvR1FzbUdna3ViN1FGd0lFbjJTZ0NGSjh2emszWnVqUjR5QnVIdGRXRE1qTk5hR2trQUhKUzg4ZHB5ZUFCQ3lGVF8xbkpCdjBfV2dwME9VRkhFTlhGdEVPNjZrM2NPaW45cDd2Ylk5Si1sa0t3djNIcmRrUTRUUUhQc1JhSGNlSlFZdkFIZFhmMVFzT19mcUJ3TlpXVkxqZy1mZWd6Z0lWdkYyaFBwcDJYWGUwQUNHNkpsN1FSQUhTS0RUMkVLYTVaS0tfQV9wSjJySEgxVnE5OXhjc29FSHU5TndNaVVENUNrSTUzZG52eDZpLVRKdGRKMmtPdkEuYjhUbFRqbkVwdUtnT1I1NFBwUV9KU3R3eGJfWm5DUnlKdmd3TlpGdEZLQXM2Q2Y1LXcxWVNfYW4yQkxKRUNqMFBnd3VXU01nbHpWUjE4VGpvX0p0NHc=',
    'service': 'https://id.mobile.de/oauth2.0/callbackAuthorize?client_id=mobile_web_DL1WJUPw&redirect_uri=https%3A%2F%2Fwww.mobile.de%2Fapi%2Fauth%2FloginCallback%3F&response_type=code&response_mode=query&client_name=CasOAuthClient',
    'state': 'eyJybmQiOiJqTEExUjZ4WUJlWWZvcEVhUXB1V1JqdmxZaXkzay1GN2RzNnpFS0p0c2dNIiwic3JjIjoiaHR0cHM6Ly93d3cubW9iaWxlLmRlLyIsInZlcmlmaWNhdGlvblN0ZXBzIjpbIk9UUCIsIldFTENPTUUiXSwiY2YiOiJPVFAifQ==',
    'nonce': 'ft3dmIBls0tvjCFgTUDn3X3IDw3-EWhqbbMsnp3bWzA',
    'locale': '',
    'kc_locale': '',
    'scope': 'openid',
    'tmSessionId': '39a3a392-1ced-4695-8133-e801f6af2071',
    '_eventId': 'submit',
    'geolocation': '',
    'username': 'asdsadafd@gmail.com',
    'password': 'asdasd12.',
}

response = client.tls_post('https://id.mobile.de/login', params=params, cookies=cookies, headers=headers, data=data, proxies={'https': PROXY})
print(response.status_code)