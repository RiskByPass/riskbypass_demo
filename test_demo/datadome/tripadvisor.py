import requests
from curl_cffi import request
import json

# Your api key, get it from https://riskbypass.com
api_key = 'Your API Key'
headers = {
    'Content-Type': 'application/json',
    'X-API-Key': api_key,
}

# The website which your need bypass
# 需要过datadome的网站
target_url = 'https://www.tripadvisor.com/'
# The datadome custom js url
# datadome主要的js url
datadome_js_url = 'https://js.datadome.co/tags.js'
# datadome js key, you can get it by entering window.ddjskey in F12 console, or by searching for ddjskey in the HTML source code
# datadome js key, 你可以使用F12控制台输入window.ddjskey获得, 或者在html源码中搜索ddjskey获得
ddjskey = '2F05D671381DB06BEE4CC52C7A6FD3'
# datadome options, you can get it by entering window.ddoptions in F12 console, or by searching for ddoptions in the HTML source code
# datadome options, 你可以使用F12控制台输入window.ddoptions获得, 或者在html源码中搜索ddoptions获得
ddoptions = json.dumps({
    "ajaxListenerPath": True,
    "allowHtmlContentTypeOnCaptcha": True
})
# proxy, format: https://username:password@ip:port
# 代理, 格式: https://username:password@ip:port
proxy = 'http://127.0.0.1:8989'

json_data = {
  "task_type": "datadome-hard",
  "params": {
    "target_url": target_url,
    "datadome_js_url": datadome_js_url,
    "ddjskey": ddjskey,
    "ddoptions": ddoptions,
    "proxy": proxy
  }
}

response = requests.post('https://riskbypass.com/api/task/sync', headers=headers, json=json_data)
print(response.json())
datadome_cookie = response.json().get('result', {}).get('result')
if not datadome_cookie:
    raise Exception('Unknown error')
else:
    for i in range(10):
        print(f'Request {i+1} times')
        headers = {
            'Accept': '*/*', 
            'Content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', 
            'referer': target_url,
            'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"', 
            'sec-ch-ua-mobile': '?0', 
            'sec-ch-ua-platform': '"Windows"'
        }
        try:
            params = {
                'searchRequest': '{"searchStartTime":"2025-07-03T16:16:00Z","numResults":11,"resultOffset":0,"clientId":"89.36.163.109","segments":[{"departureDate":"2025-08-19","departureAirportCode":"SAN","arrivalAirportCode":"SDQ","includeNearbyOrigins":true,"includeNearbyDestinations":true}],"classOfService":"ECONOMY","travelers":{"numAdults":1,"numSeniors":0,"childAges":[]},"itineraryType":"ONE_WAY","inventoryCountry":"US","pointOfSale":"en-US","displayCurrency":"USD","platforms":["DESKTOP","WEB"],"filter":{"segments":[],"numberOfStops":[],"marketingCarriers":[],"operatingCarriers":[],"amenities":[],"departureAirportCodes":["SAN","CLD"],"arrivalAirportCodes":[],"connectingAirportCodes":[],"purchaseLinkProviders":[],"alliances":[],"travelTypes":[],"classesOfService":["ECONOMY"],"flightQualities":[]},"isp":"Melbikomas UAB","searchCompletionCount":0,"ipCountry":"US","sortOrder":"ML_BEST_VALUE","searchId":"6dc78aef-0661-44ee-8dfa-6947e5108d52.480","extendedInfo":{"pageViewId":"75559f84-07b0-44a0-a0e1-7af578e393b0","pinnedItineraryKeys":[]}}',
                'searchRequestAdditions': '{"awConf":false,"aw":true,"awSub":false,"scc":0,"vpsid":"","ss":false,"ssUrl":"","pf":[],"srv":"CheapFlightsSearchResults","p":"NONE","df":{"segments":[],"numberOfStops":[],"marketingCarriers":[],"operatingCarriers":[],"amenities":[],"departureAirportCodes":[],"arrivalAirportCodes":[],"connectingAirportCodes":[],"purchaseLinkProviders":[],"alliances":[],"travelTypes":[],"classesOfService":[],"flightQualities":[]},"trt":1}',
                'pollingData': '{"finalAttempt":false,"ccids":[1727,1728],"op":false,"VP":false,"si":false,"prefilterStage":"NONE","requestNumber":14}',
                'filterSettings': '{"aa":"","tt":"","a":"","d":"","ns":"","cos":"0","fq":"","al":"","ft":"","sid":"","oc":"","plp":"","mc":"","da":"SAN,CLD","pRange":"-1,-1","ca":""}',
                'puid': '75559f84-07b0-44a0-a0e1-7af578e393b0',
                'addDynamicDeal': 'true',
                'searchKey': '7de16e0fdf4bdeee9869fcf0b8f39388',
            }

            response = requests.get('https://www.tripadvisor.com/data/1.0/flightsearch/poll', params=params, cookies=json.loads(datadome_cookie), headers=headers, proxies={'https':proxy})
            print(response.text)
        except Exception as e:
            print(e)