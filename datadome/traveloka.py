# -*- coding: utf-8 -*-
import json, uuid, re
from urllib.parse import urlencode
import cycronet as requests
from riskbypass import RiskByPassClient

BASE_URL = "https://riskbypass.com"
TOKEN = "your token"
PROXY = "http://username:password@ip:port"

client = RiskByPassClient(token=TOKEN, base_url=BASE_URL)


def get_headers(ua, search_id):
    return {
        "x-route-prefix": "en-en",
        "sec-ch-ua-platform": '"macOS"',
        "t-a-v": "262328",
        "tv-clientsessionid": "T1-web.01KT3468CN7DYCTCSQYYX97Z89",
        "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "tv-country": "EN",
        "content-type": "application/json",
        "x-client-interface": "desktop",
        "www-app-version": "release_webfpr_20260522-ede75aebbe",
        "fpr-search-id": search_id,
        "tv-currency": "CAD",
        "Referer": "https://www.traveloka.com/en-en/flight/fullsearch?ap=DEL.DPS&dt=21-06-2026.NA&ps=1.0.0&sc=ECONOMY",
        "tv-mcc-id": "01KT366EDCA7R91W7TZE6Q6SXN",
        "x-domain": "flight",
        "tv-language": "en_EN",
        "User-Agent": ua,
        "x-did": "MDFLVDM0NjhXUEJRSFlDNU1TWVRSVE01NFI=",
    }


def get_body(search_id):
    return {
        "fields": [],
        "data": {
            "tripType": "ONE_WAY",
            "seatPublishedClass": "ECONOMY",
            "journeys": [{"originCode": "DEL", "destinationCode": "DPS", "departureDate": "2026-06-18"}],
            "journeyIndex": 0,
            "selectedFlights": [],
            "numSeats": {"numAdults": 1, "numChildren": 0, "numInfants": 0},
            "searchId": search_id,
            "currency": "CAD",
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


def search_flight(cookies, ua, search_id):
    proxies = {"http": PROXY, "https": PROXY} if PROXY else None
    r = requests.post(
        "https://www.traveloka.com/api/v2/flight/search/initial",
        headers=get_headers(ua, search_id),
        cookies=cookies,
        json=get_body(search_id),
        proxies=proxies,
        timeout=30,
    )
    return r


def extract_interstitial_url(html):
    m = re.search(r"var dd=(\{.*?\})</script>", html)
    if not m:
        return None
    dd = json.loads(m.group(1).replace("'", '"'))
    return (
        f"https://{dd['host']}/interstitial/?"
        + urlencode({
            "initialCid": dd["cid"],
            "hash": dd["hsh"],
            "cid": dd["cookie"],
            "referer": "https://www.traveloka.com/en-en",
            "s": dd["s"],
            "e": dd["e"],
            "b": dd["b"],
            "dm": "cd",
        })
    )


def solve_slider(interstitial_url, cookies):
    result = client.run_task({
        "task_type": "datadome-slider",
        "proxy": PROXY,
        "target_url": interstitial_url,
        "target_method": "GET",
        "init_cookies": cookies,
    }, timeout=120)
    print(f"slider result: {result}")
    if result and result.get("datadome"):
        return result["datadome"]
    return None


def main():
    # Step 1: solve aws waf
    aws_result = client.run_task({
        "task_type": "aws",
        "proxy": PROXY,
        "target_url": "https://www.traveloka.com/en-en",
        "aws_js_url": "https://d9253bf4bdfd.edge.sdk.awswaf.com/d9253bf4bdfd/1fcfec27aa97/challenge.compact.js",
    }, timeout=120)
    print(f"aws result: {aws_result}")
    aws_token = aws_result["token"]
    ua = aws_result["ua"]

    base_cookies = {
        "currentCountry": "CA",
        "selectedCurrency": "CAD",
        "tv-repeat-visit": "true",
        "clientSessionId": "T1-web.01KT3468CN7DYCTCSQYYX97Z89",
        "tv_cs": "1",
        "countryCode": "CA",
        "_gcl_au": "1.1.761323979.1780369008",
        "tv_user": '{"authorizationLevel":100,"id":null}',
        "_tt_enable_cookie": "1",
        "_ttp": "01KT346BM9C6H8F63KR1NAM1XN_.tt.1",
        "_fwb": "109PE4WvamT4uJMLyaJoAAP.1780369011286",
        "_yjsu_yjad": "1780369011.6816f5d4-7b05-4dda-84be-52c9913253a9",
        "_cs_ex": "1760605804",
        "_cs_c": "1",
        "__lt__cid": "266869d7-cd0a-4bd7-b1e2-b1ca5150ae65",
        "__lt__sid": "ab9f6033-ea9f8727",
        "_gid": "GA1.2.2105760811.1780369013",
        "_fbp": "fb.1.1780369013138.826550336747576666",
        "_ly_su": "1780369011.6816f5d4-7b05-4dda-84be-52c9913253a9",
        "_pin_unauth": "dWlkPU5USTNPVEZtWWpNdFlUZzVNQzAwTjJVeExXSmpOemt0TW1FMk9ETTBNR1JpTlRGag",
        "g_state": '{"i_l":0,"i_ll":1780369247837,"i_b":"UIo8IAS4bHMCESYZJbKQGGnAcS5fZi2O94s5m8zRD0s","i_e":{"enable_itp_optimization":0},"i_et":1780369014431}',
        "amp_f4354c": "lVGBjK72J1cjppIbp5hGJL...1jq3469jn.1jq34dnf9.0.0.0",
        "__rtbh.lid": '%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22ViTVufMbcXJNOHlnBGey%22%2C%22expiryDate%22%3A%222027-06-02T03%3A00%3A51.955Z%22%7D',
        "wcs_bt": "s_2cb982ada97c:1780369252",
        "_ga": "GA1.2.1744586869.1780369011",
        "ttcsid_CUM82PBC77U4QKJNCRL0": "1780369010315::a1Z_4fO3hi6luKKPRRj9.1.1780369252933.1",
        "_rdt_uuid": "1780369012909.f6eb9919-4a9f-43d0-9749-0506b7239a14",
        "tv_mcc_id": "01KT34DRPG9R98TAHH4GXFYANF",
        "cto_bundle": "07zG2V9kTG1XUCUyQlN0MiUyQmY4eFpHc1VkJTJCU08wcnpqb09nJTJGQTZ3RFJmMHNxaDhmOE1LaXBSeGFRVTRwWDRETk1YdXp0dHdsTW9RY0R1NDg0Tkljek03RThzMkJnVDdvdVYlMkY1S0R6WnBZWENuelNOeUhwbjh3OXNnb012TDF4WDJlU082a3FWUFlJb3FwaDN3a2dab2YlMkIlMkJzOHE3USUzRCUzRA",
        "_ga_RSRSMMBH0X": "GS2.1.s1780369010$o1$g1$t1780369253$j58$l0$h1286926689",
        "tv_lt": "1780369406056",
        "sen_t": "Adt8GUIP08HOIyh9XsCCsjum5aG05zT4VAHdduNss7E0htGgwlKXAkpa78vcPdUhznc2J8SwPQ/MJKyWUdy+55CZ+4ezzZQEQ8JJVx04ah2ckykl+i4HcKVq+SM=",
        "ttcsid": "1780369010316::Ibge9K1md2ftbFJqMdMV.1.1780369252933.0::1.242499.241846::431830.11.1649.758::0.0.0",
        "exp_variant_flight_frontend_exp_web": "CONTROL",
        "amp_1a5adb": "PlkY1vonkyVsOw67E00u2U...1jq3469jk.1jq34jjst.u.0.u",
        "exp_variant_flight_search_api_revamp_experiment_web": "CONTROL",
        "exp_variant_fl_autocomplete_revamp_web": "X_N_A",
        "exp_variant_flight_fe_prefetch_experiment_web": "X_N_A",
        "exp_variant_flight_search_exp_web": "VAR_CARRY_OVER",
        "exp_variant_fl_search_autocomplete_srs_web": "X_N_A",
        "exp_variant_flight_fe_exp_web": "CONTROL",
        "exp_variant_fl_bundle_web": "CONTROL",
        "_dd_s": "rum=0&expire=1780370342145&logs=1&id=bb575e8c-18ae-4621-976a-6ec23ce8f54c&created=1780369007008",
        "exp_variant_fl_price_graph_web": "CONTROL",
        "tvs": "qgdHX7GvehrD9XH5a3S4PXWKx93/3Xi103f/kPpnhg1IQez7AjqOPow88qqCMiL7CqvJjpn5Z2svD8QZzAmUN07gmFQkK2qgsdbWEYgFfB5uk0fUx7sD+NMcK9CmgVocVXCUQH7jQYSGVHd/Q00sukDA955iBvi1BiD11jxKqfL5u09yAru40JsnILlCW/Ax9J5S785Db9rSSMgL+VLDbY9uReQC3XjTJmpg5aN14DhxulayFMoO/TzKJgiFT0leg43qby0ICwtMQsEEYY/mJ063CCJo+Z+R9n/X0FgUdFdWi6NKpEDgL3xVNnQjLp40FhrkmWFU4Pn0+ElScsbvvTiMfdMUTSusT7vsPBJgiZPlPIHG/10iGeoZDK7x7sfH3g39s8rYSA7HjK/8G//IPFrVT48LTcC7PrGLCYcS3IXVQBEu5WaSvTPNcBYiPha4BZndNlY7RHVR9o8C7zQGZ2rR0pGDiAsnOWt7ipbHyNR8KTGPdQGBcyeofM2v70q5WFyB96qYZpNobYu/0utkvw==",
        "tvo": "L2FwaS92Mi9mbGlnaHQvc2VhcmNoL2luaXRpYWw=",
        "tvl": "qgdHX7GvehrD9XH5a3S4PUiOJGezXQ9yizVaSxTklwrLYY64AE4apiD1qmHRGaV8gGAQoV6xR5wi1hxtboYegx0JoHbuxL9J5IDMykh7yrn/kmgjvZe3CXlrOt5A94G1h8SGYm0D03zEW7S7g02l9zkAPbkMGQ6AJj+0Bs51j2e9SZmGg6OFSbJOpR7JfCIqCI1se4xoGkOFZX0fVahZ62hHfL1P0bR1Il8gNsTJrDqf8Y9VO62NtJ1LVcPuU1R/BMZxXyEsFbLwH0fYW6iCB91EbvH0iKih21G9OYSMy+jM0WMA1zSky7I1/5su3gOqscruCdxDE+8ozZakmxoZBO7zmstCX4iU7dBBDkx6AHXQxIN2Eyn0u8317CGGUnLgxbVWc9mUJC6U6r8wkx04c+4CDTx/jJt5ZXoEQTwGFtkDiUcpAerSj1wc+39pi+hfuWC/awjANJRjKz0Vnk7xltA3KaEdrj/1NKCprWcOyTb4khOlZXUnpQ0OOWYlTOEOtO87/nxmILGXfMVUWbBgQ2U1fEbW5//zNUdkH7roM9U=",
    }
    cookies = {**base_cookies, "aws-waf-token": aws_token}

    # Step 2: search flight
    search_id = str(uuid.uuid4())
    r = search_flight(cookies, ua, search_id)
    print(f"HTTP {r.status_code}")
    print(r.text[:500])

    # Step 3: if datadome interstitial triggered, solve slider and retry
    if "captcha-delivery.com" in r.text:
        interstitial_url = extract_interstitial_url(r.text)
        if interstitial_url:
            print(f"\ninterstitial URL:\n{interstitial_url}")
            dd_cookie = solve_slider(interstitial_url, cookies)
            if dd_cookie:
                cookies["datadome"] = dd_cookie
                r = search_flight(cookies, ua, search_id)
                print(f"\nretry: HTTP {r.status_code}")
                print(r.text[:2000])

    print(f"\nfinal: HTTP {r.status_code}")


if __name__ == "__main__":
    main()
