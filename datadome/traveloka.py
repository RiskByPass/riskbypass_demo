# -*- coding: utf-8 -*-
import uuid, re
import tls_client
from riskbypass import RiskByPassClient

BASE_URL = "https://riskbypass.com"
TOKEN = "your_token"
PROXY = "http://xxxxxx:xxxxxxx@45.111.11.11:1223"
TARGET_URL = "https://www.traveloka.com/en-en/flight/fullsearch?ap=DEL.DPS&dt=25-06-2026.NA&ps=1.0.0&sc=ECONOMY"

client = RiskByPassClient(token=TOKEN, base_url=BASE_URL)

HEADER_ORDER = [
    "content-length",
    "x-route-prefix",
    "sec-ch-ua-full-version-list",
    "sec-ch-ua-platform",
    "t-a-v",
    "tv-clientsessionid",
    "sec-ch-ua",
    "sec-ch-ua-model",
    "sec-ch-ua-mobile",
    "tv-country",
    "sec-ch-ua-arch",
    "content-type",
    "x-client-interface",
    "www-app-version",
    "fpr-search-id",
    "tv-currency",
    "sec-ch-device-memory",
    "tv-mcc-id",
    "x-domain",
    "tv-language",
    "user-agent",
    "x-did",
    "accept",
    "origin",
    "sec-fetch-site",
    "sec-fetch-mode",
    "sec-fetch-dest",
    "referer",
    "accept-encoding",
    "accept-language",
    "cookie",
    "priority",
]


def parse_chrome_version(ua):
    m = re.search(r'Chrome/(\d+)\.(\S+)', ua)
    if m:
        return m.group(1), f"{m.group(1)}.{m.group(2)}"
    return "148", "148.0.7778.216"


def get_headers(ua, search_id):
    major, full_ver = parse_chrome_version(ua)
    is_mac = "Macintosh" in ua
    platform = '"macOS"' if is_mac else '"Windows"'
    arch = '"arm"' if is_mac else '"x86_64"'

    return {
        "x-route-prefix": "en-en",
        "sec-ch-ua-full-version-list": f'"Chromium";v="{full_ver}", "Google Chrome";v="{full_ver}", "Not/A)Brand";v="99.0.0.0"',
        "sec-ch-ua-platform": platform,
        "t-a-v": "262381",
        "tv-clientsessionid": "T1-web.01KTBF7D7FPBE8Z0SNR6CAJX8Q",
        "sec-ch-ua": f'"Chromium";v="{major}", "Google Chrome";v="{major}", "Not/A)Brand";v="99"',
        "sec-ch-ua-model": '""',
        "sec-ch-ua-mobile": "?0",
        "tv-country": "EN",
        "sec-ch-ua-arch": arch,
        "content-type": "application/json",
        "x-client-interface": "desktop",
        "www-app-version": "release_webfpr_20260602-a250d4859f",
        "fpr-search-id": search_id,
        "tv-currency": "USD",
        "sec-ch-device-memory": "16",
        "tv-mcc-id": "01KTBFAARQ1GV14710E749QTEE",
        "x-domain": "flight",
        "tv-language": "en_EN",
        "user-agent": ua,
        "x-did": "MDFLVDM0NjhXUEJRSFlDNU1TWVRSVE01NFI=",
        "accept": "*/*",
        "origin": "https://www.traveloka.com",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": TARGET_URL,
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en,en-US;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "priority": "u=1, i",
    }


def get_body(search_id):
    return {
        "fields": [],
        "data": {
            "tripType": "ONE_WAY",
            "seatPublishedClass": "ECONOMY",
            "journeys": [{"originCode": "DEL", "destinationCode": "DPS", "departureDate": "2026-06-29"}],
            "journeyIndex": 0,
            "selectedFlights": [],
            "numSeats": {"numAdults": 1, "numChildren": 0, "numInfants": 0},
            "searchId": search_id,
            "currency": "USD",
            "additionalData": {
                "utmId": None, "utmSource": None, "utmIdMarketing": None,
                "pageName": "SEARCH_RESULT", "searchSource": "ONE_WAY",
                "visitId": str(uuid.uuid4()),
                "usePromoFinder": True, "useDateFlow": False,
                "isBreakSmartCombo": False, "prefetchFlag": True,
                "isBaggageFilterEnabled": False,
            },
            "filter": {"standAlone": True},
            "inventoryPricingDisplayType": "INDEPENDENT",
            "sharedFlights": [],
            "trackingMap": {},
        },
        "clientInterface": "desktop",
    }

def main():
    # Step 1: solve aws waf via riskbypass
    print("=== Step 1: solve AWS WAF ===")
    aws_result = client.run_task({
        "task_type": "aws",
        "target_url": "https://www.traveloka.com/en-en",
        "aws_js_url": "https://d9253bf4bdfd.edge.sdk.awswaf.com/d9253bf4bdfd/1fcfec27aa97/challenge.compact.js",
    }, timeout=120)
    print(f"aws result: {aws_result}")
    aws_token = aws_result["token"]
    ua = aws_result["ua"]

    # Step 2: solve datadome via riskbypass custom_task (traveloka_event)
    print("\n=== Step 2: solve datadome (riskbypass custom_task) ===")
    dd_result = client.run_task({
        "task_type": "custom_task",
        "proxy": PROXY,
        "target_url": TARGET_URL,
        "init_cookies": {"aws-waf-token": aws_token},
        "custom_event": "traveloka",
    }, timeout=120)
    print(f"datadome result: {dd_result}")
    datadome = dd_result.get("datadome")
    dd_ua = dd_result.get("ua")
    # datadome cookie 绑定浏览器 UA
    ua = dd_ua or ua

    # Step 3: search flight with tls_client
    print("\n=== Step 3: search flight ===")
    cookies = {
        "countryCode": "CA",
        "_gcl_au": "1.1.761323979.1780369008",
        "_tt_enable_cookie": "1",
        "_ttp": "01KT346BM9C6H8F63KR1NAM1XN_.tt.1",
        "_fwb": "109PE4WvamT4uJMLyaJoAAP.1780369011286",
        "_yjsu_yjad": "1780369011.6816f5d4-7b05-4dda-84be-52c9913253a9",
        "_kmpid": "km|www.traveloka.com|1780369011502|38397e32-9de3-4caf-9058-a095dc0faea9",
        "_cs_ex": "1760605804",
        "_cs_c": "1",
        "__lt__cid": "266869d7-cd0a-4bd7-b1e2-b1ca5150ae65",
        "_fbp": "fb.1.1780369013138.826550336747576666",
        "_ly_su": "1780369011.6816f5d4-7b05-4dda-84be-52c9913253a9",
        "_pin_unauth": "dWlkPU5USTNPVEZtWWpNdFlUZzVNQzAwTjJVeExXSmpOemt0TW1FMk9ETTBNR1JpTlRGag",
        "tv_cs": "1",
        "tv-repeat-visit": "true",
        "_gid": "GA1.2.1951459652.1780565821",
        "tv_user": '{"authorizationLevel":100,"id":null}',
        "clientSessionId": "T1-web.01KTBF7D7FPBE8Z0SNR6CAJX8Q",
        "__lt__sid": "ab9f6033-e8985a27",
        "tv_mcc_id": "01KTBFAARQ1GV14710E749QTEE",
        "tv_lt": "1780649298150",
        "aws-waf-token": aws_token,
        "exp_variant_flight_search_exp_web": "VAR_CARRY_OVER",
        "exp_variant_fl_search_autocomplete_srs_web": "X_N_A",
        "exp_variant_flight_fe_prefetch_experiment_web": "X_N_A",
        "exp_variant_fl_autocomplete_revamp_web": "X_N_A",
        "exp_variant_flight_frontend_exp_web": "VAR_INCREMENTAL_LOADING",
        "exp_variant_fl_bundle_web": "CONTROL",
        "exp_variant_flight_fe_exp_web": "CONTROL",
        "exp_variant_flight_search_api_revamp_experiment_web": "CONTROL",
        "exp_variant_fl_price_graph_web": "CONTROL",
        "sen_t": "Adt8GULxQ4mpmGt0XOhcGzBMOxEx7HQp9eG6eDA4WLSdqdR4/ASdOKdswxcdToS1um+t7kWmxI5QY/xNKVt0z18mG4n+PD2+kWL4NM9wmJzxNdvCt+uPfWisn/pL",
        "amp_f4354c": "lVGBjK72J1cjppIbp5hGJL...1jqbf7eo5.1jqbg5qf9.0.1.1",
        "ttcsid_CUM82PBC77U4QKJNCRL0": "1780649017746::tXcHba6kApIchbQeaBHX.5.1780650011734.1",
        "__rtbh.lid": '{"eventType":"lid","id":"ViTVufMbcXJNOHlnBGey","expiryDate":"2027-06-05T09:00:11.774Z"}',
        "_ga_RSRSMMBH0X": "GS2.1.s1780649018$o6$g1$t1780650011$j60$l0$h1593071270",
        "_ga": "GA1.2.1744586869.1780369011",
        "_gat_UA-29776811-12": "1",
        "_rdt_uuid": "1780369012909.f6eb9919-4a9f-43d0-9749-0506b7239a14",
        "wcs_bt": "s_2cb982ada97c:1780650011",
        "g_state": '{"i_l":0,"i_ll":1780650011947,"i_b":"C0ZzTVTzfTC7fqGmeNCQmVkX1ekOq821xTDvUkjv+TA","i_e":{"enable_itp_optimization":0},"i_et":1780369014431}',
        "exp_variant_fl_fe_summary_tray_web": "CONTROL",
        "cto_bundle": "cumT1V9kTG1XUCUyQlN0MiUyQmY4eFpHc1VkJTJCU083aXIyYUYlMkY4czFqZk5OdG56bFU4OWdCckQzZGIlMkIlMkYwRUdRdVFjYkVTS2FQaSUyQjhhSGxjZiUyQllGWWY1WUFJblEzWGkxaVFRQnN6Wlo4MGVSVDNhcjJXeUMwS1JnSDRMVjRxWmdmWXdJV3QlMkJZalU2NiUyQmh3UU4zQVhHcCUyRkdHd3dMVURnJTNEJTNE",
        "tvs": "qgdHX7GvehrD9XH5a3S4PXWKx93/3Xi103f/kPpnhg1IQez7AjqOPow88qqCMiL7CqvJjpn5Z2svD8QZzAmUN07gmFQkK2qgsdbWEYgFfB5uk0fUx7sD+NMcK9CmgVocrii3pNJ2kgG/MGUmzAKhwmCIB1NXpx+g05VnrVlNT1r5u09yAru40JsnILlCW/AxwrbRHflY9M7JmqJpVY+CNeh8IwirbSyrPwuwCXJPBaEOPWf1H1TwWIrzQ38h3S6Ng43qby0ICwtMQsEEYY/mJ063CCJo+Z+R9n/X0FgUdFdWi6NKpEDgL3xVNnQjLp40FhrkmWFU4Pn0+ElScsbvvTdAlhWnvtaY2TT/eB3a75rebnifJg2HT8UU61dJRfWwNCiosKIt/rK+fJMXZ/CxGIvdXGsqLCea6vaYcvwZOTI4pkItQi5qQo00jp4Rum9gQQ7Rb2JpXZSOvkfVcbeBF2T/sG995qR5yssY233eWZWRWQQlti40Vt30KSn2IQEa",
        "ttcsid": "1780649017746::Be_KC3CnX5b85R7gwaJb.5.1780650011734.0::1.986713.993691::999770.9.133.68::93902.10.0",
        "amp_1a5adb": "PlkY1vonkyVsOw67E00u2U...1jqbf7eo1.1jqbg60re.8v.1.90",
        "tvl": "qgdHX7GvehrD9XH5a3S4PUiOJGezXQ9yizVaSxTklwrLYY64AE4apiD1qmHRGaV8gGAQoV6xR5wi1hxtboYegx0JoHbuxL9J5IDMykh7yrn/kmgjvZe3CXlrOt5A94G1h8SGYm0D03zEW7S7g02l9zkAPbkMGQ6AJj+0Bs51j2d7dB7d2GOPZefxwlUgv88KTVIUSALzrwnYbDhX+O9UyoLkeHDnQ25bUlnoVrisvfaBYmCzHr4AeeDHaLlpr3YFBMZxXyEsFbLwH0fYW6iCB91EbvH0iKih21G9OYSMy+jM0WMA1zSky7I1/5su3gOqscruCdxDE+8ozZakmxoZBO7zmstCX4iU7dBBDkx6AHXQxIN2Eyn0u8317CGGUnLgxbVWc9mUJC6U6r8wkx04c+4CDTx/jJt5ZXoEQTwGFtmsBqzEGLwe3QJEWK6atmQKtUI0OnbOC/FwlVW2PoN09+U8gcb/XSIZ6hkMrvHux8fyr2npoMcG3LoGCiP3w7uAFIINF1Mq0BLxeBc71R+3la5ReueIqbN1HRKmP2mCv2g=",
        "tvo": "L2FwaS92MS90dmxrL2V2ZW50cw==",
        "_dd_s": "rum=0&expire=1780650919029&logs=1&id=e2893d0d-d749-4c5d-ab0e-c59cf0042f74&created=1780649014796",
    }
    if datadome:
        cookies["datadome"] = datadome

    session = tls_client.Session(
        client_identifier="chrome_120",
        random_tls_extension_order=True,
        header_order=HEADER_ORDER,
    )
    search_id = str(uuid.uuid4())
    r = session.post(
        "https://www.traveloka.com/api/v2/flight/search/initial",
        headers=get_headers(ua, search_id),
        cookies=cookies,
        json=get_body(search_id),
        proxy=PROXY,
    )
    print(f"HTTP {r.status_code}")
    print(f"Body: {r.text[:2000]}")

    if "captcha-delivery.com" not in r.text and r.status_code == 200:
        print(f"\n✅ OK — HTTP {r.status_code}")
    else:
        print(f"\n❌ Failed — HTTP {r.status_code}")


if __name__ == "__main__":
    main()
