from riskbypass import RiskByPassClient
import re
import random

TOKEN = "your_token_here"
random_port = random.randint(10000, 20000)
proxy = f"http://user:password@host:{random_port}"

url = "https://booking.norwegian.com/booking/"

# 来自 Chromium user_agent_utils.cc 的 GREASE 常量
_GREASEY_CHARS = [" ", "(", ":", "-", ".", "/", ")", ";", "=", "?", "_"]
_GREASED_VERSIONS = ["8", "99", "24"]
_BRAND_ORDERS = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]


def _grease_brand(seed):
    return f"Not{_GREASEY_CHARS[seed % 11]}A{_GREASEY_CHARS[(seed + 1) % 11]}Brand"


def _grease_version(seed):
    return _GREASED_VERSIONS[seed % 3]


def build_sec_ch_ua_headers(user_agent, *, full_version=None, platform=None,
                            platform_version=None, arch="x86", bitness="64",
                            model="", mobile=None):
    """从 UA 字符串生成 sec-ch-ua 系列请求头。

    自动从 UA 解析：Chrome 主版本、平台（macOS/Windows/Linux）、mobile。
    以下无法从 UA 反推（UA reduction 已冻结），需按需覆盖：
      full_version      完整版本号，如 "149.0.7827.197"；不传则退化为 major.0.0.0
      platform_version  平台版本，如 macOS "15.5.0" / Win11 "15.0.0"
      arch              "x86" 或 "arm"
      bitness           "64" / "32"
    """
    ua = user_agent
    m = re.search(r"Chrome/(\d+)(?:\.(\d+)\.(\d+)\.(\d+))?", ua)
    if not m:
        raise ValueError("UA 里找不到 Chrome 版本")
    major = int(m.group(1))

    # 完整版本：UA 里若带且非 reduced 则用之，否则用参数，再否则 major.0.0.0
    ua_full = f"{m.group(1)}.{m.group(2)}.{m.group(3)}.{m.group(4)}" if m.group(2) else None
    if full_version is None:
        full_version = ua_full if (ua_full and ua_full.split(".")[1:] != ["0", "0", "0"]) \
            else f"{major}.0.0.0"

    # 平台
    if platform is None:
        if "Windows" in ua:
            platform = "Windows"
        elif "Mac OS X" in ua or "Macintosh" in ua:
            platform = "macOS"
        elif "Linux" in ua or "X11" in ua or "Ubuntu" in ua:
            platform = "Linux"
        else:
            platform = "Unknown"

    # 平台版本默认值（强烈建议真机传入，尤其 macOS/Win11）
    if platform_version is None:
        if platform == "Windows":
            platform_version = "10.0.0"          # Win10；Win11 一般是 "13.0.0"+/"15.0.0"
        elif platform == "macOS":
            mm = re.search(r"Mac OS X (\d+)[_.](\d+)[_.]?(\d+)?", ua)
            platform_version = f"{mm.group(1)}.{mm.group(2)}.{mm.group(3) or '0'}" if mm else "10.15.7"
        else:  # Linux / Ubuntu
            platform_version = ""                 # Chrome on Linux 通常回传空

    # mobile
    if mobile is None:
        mobile = "?1" if ("Mobile" in ua or "Android" in ua) else "?0"

    seed = major
    gb, gv = _grease_brand(seed), _grease_version(seed)
    # 索引固定为 0=GREASE, 1=Chromium, 2=Google Chrome；顺序由 seed 决定
    brands = [
        (gb, gv, f"{gv}.0.0.0"),
        ("Chromium", str(major), full_version),
        ("Google Chrome", str(major), full_version),
    ]
    ordered = [brands[i] for i in _BRAND_ORDERS[seed % 6]]
    sec_ch_ua = ", ".join(f'"{b}";v="{v}"' for b, v, _ in ordered)
    full_list = ", ".join(f'"{b}";v="{fv}"' for b, _, fv in ordered)

    return {
        "user-agent": user_agent,
        "sec-ch-ua": sec_ch_ua,
        "sec-ch-ua-arch": f'"{arch}"',
        "sec-ch-ua-bitness": f'"{bitness}"',
        "sec-ch-ua-full-version": f'"{full_version}"',
        "sec-ch-ua-full-version-list": full_list,
        "sec-ch-ua-mobile": mobile,
        "sec-ch-ua-model": f'"{model}"',
        "sec-ch-ua-platform": f'"{platform}"',
        "sec-ch-ua-platform-version": f'"{platform_version}"',
    }

client = RiskByPassClient(token=TOKEN)

task = {
  "task_type": "cloudflare_waf",
  "proxy": proxy,
  "target_url": url,
  "target_method": "GET"
}
response = client.run_task(task)

print(response)

cookies = response.get("cookies")
user_agent = response.get("ua")
sec_headers = build_sec_ch_ua_headers(user_agent)

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://booking.norwegian.com',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://booking.norwegian.com/booking/',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-arch': '"arm"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"149.0.7827.197"',
    'sec-ch-ua-full-version-list': '"Google Chrome";v="149.0.7827.197", "Chromium";v="149.0.7827.197", "Not)A;Brand";v="24.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-ua-platform-version': '"15.5.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
}

print(sec_headers)
headers.update(sec_headers)

response = client.tls_get('https://booking.norwegian.com/booking/recovery', headers=headers, cookies=cookies, proxies={"http": proxy, "https": proxy})

print(response.text)
print(response.status_code)