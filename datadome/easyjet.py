import requests
import time
import json
import random

BASE_URL = "https://riskbypass.com"
TOKEN = "your token"
TIMEOUT = 60
PROXY = "http://username:password@host:port"


def run_task(payload):
    """
    向RiskByPass提交任务并轮询结果
    
    Args:
        payload: 任务配置字典
        
    Returns:
        dict: 任务结果，失败返回None
    """
    session = requests.Session()
    headers = {
        "Content-Type": "application/json",
        "x-api-key": TOKEN
    }

    print("[*] 提交任务:", payload.get('task_type'))

    try:
        resp = session.post(
            f"{BASE_URL}/task/submit",
            headers=headers,
            json=payload,
            timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print("[!] 提交请求异常:", repr(e))
        return None

    if not data.get("ok"):
        print("[!] 提交失败:", data)
        return None

    task_id = data.get("task_id")
    if not task_id:
        print("[!] 响应中没有 task_id:", data)
        return None

    print(f"[+] 已提交，task_id = {task_id}")

    start_time = time.time()

    while True:
        # 超时检查
        if time.time() - start_time > TIMEOUT:
            print("[!] 任务超时")
            return None

        try:
            r = session.get(
                f"{BASE_URL}/task/result/{task_id}",
                headers={"Cache-Control": "no-cache", "x-api-key": TOKEN},
                timeout=30
            )
            r.raise_for_status()
            j = r.json()
        except Exception as e:
            print("[!] 轮询异常:", repr(e))
            time.sleep(1)
            continue

        st = j.get("status", "UNKNOWN")
        print(f"[*] 状态: {st}")

        if st in ("RUNNING", "QUEUED"):
            time.sleep(1)
            continue

        if st == "SUCCESS":
            result = j.get("result")
            print("[+] 成功:", json.dumps(result, ensure_ascii=False, indent=2))
            return result

        elif st == "FAILED":
            print("[!] 任务失败:", j.get("error", j))
            return None

        elif st == "NOT_FOUND":
            print("[!] 未找到任务")
            return None

        else:
            print("[!] 未知响应:", j)
            return None

search_url = 'https://flightconnections.easyjet.com/api/graphql?query=%20%20%20%20query%20searchOutbound($partner:%20Partner!,%20$origin:%20String!,%20$destination:%20String!,%20$passengerAges:%20[PositiveInt!]!,%20$metadata:%20Metadata!,%20$departureDateString:%20String!,%20$returnDateString:%20String,%20$sort:%20Sort,%20$limit:%20PositiveInt,%20$filters:%20OfferFiltersInput,%20$utmSource:%20String)%20{%20%20boundSearch:%20searchOutbound(%20%20%20%20partner:%20$partner%20%20%20%20origin:%20$origin%20%20%20%20destination:%20$destination%20%20%20%20passengerAges:%20$passengerAges%20%20%20%20metadata:%20$metadata%20%20%20%20departureDateString:%20$departureDateString%20%20%20%20returnDateString:%20$returnDateString%20%20%20%20sort:%20$sort%20%20%20%20limit:%20$limit%20%20%20%20filters:%20$filters%20%20%20%20utmSource:%20$utmSource%20%20)%20{%20%20%20%20offers%20{%20%20%20%20%20%20...Offer%20%20%20%20}%20%20%20%20offersFilters%20{%20%20%20%20%20%20...OffersFilters%20%20%20%20}%20%20}}%20%20%20%20%20%20%20%20fragment%20Offer%20on%20Offer%20{%20%20id%20%20journeyId%20%20price%20%20pricePerPerson%20%20outboundPricePerPerson%20%20homeboundPricePerPerson%20%20fareType%20%20currency%20%20transferURL%20%20duration%20%20itinerary%20{%20%20%20%20...Itinerary%20%20}%20%20passengerAges%20%20isOneWay}%20%20%20%20%20%20%20%20fragment%20Itinerary%20on%20Itinerary%20{%20%20outbound%20{%20%20%20%20...Route%20%20}%20%20homebound%20{%20%20%20%20...Route%20%20}}%20%20%20%20%20%20%20%20fragment%20Route%20on%20Route%20{%20%20id%20%20origin%20{%20%20%20%20code%20%20%20%20name%20%20%20%20city%20%20%20%20country%20%20}%20%20destination%20{%20%20%20%20code%20%20%20%20name%20%20%20%20city%20%20%20%20country%20%20}%20%20departure%20%20arrival%20%20duration%20%20operatingCarrier%20{%20%20%20%20name%20%20%20%20code%20%20%20%20flightNumber%20%20}%20%20marketingCarrier%20{%20%20%20%20name%20%20%20%20code%20%20%20%20flightNumber%20%20}%20%20legs%20{%20%20%20%20...Leg%20%20}}%20%20%20%20%20%20%20%20fragment%20Leg%20on%20Leg%20{%20%20id%20%20duration%20%20origin%20{%20%20%20%20code%20%20%20%20name%20%20%20%20city%20%20%20%20country%20%20}%20%20destination%20{%20%20%20%20code%20%20%20%20name%20%20%20%20city%20%20%20%20country%20%20}%20%20departure%20%20arrival%20%20carrierType%20%20operatingCarrier%20{%20%20%20%20name%20%20%20%20code%20%20%20%20flightNumber%20%20}%20%20marketingCarrier%20{%20%20%20%20name%20%20%20%20code%20%20%20%20flightNumber%20%20}}%20%20%20%20%20%20%20%20fragment%20OffersFilters%20on%20OfferFilters%20{%20%20carrierCodes%20%20cabinClass%20%20connectionTime%20{%20%20%20%20min%20%20%20%20max%20%20}%20%20landing%20{%20%20%20%20outbound%20{%20%20%20%20%20%20min%20%20%20%20%20%20max%20%20%20%20}%20%20%20%20homebound%20{%20%20%20%20%20%20min%20%20%20%20%20%20max%20%20%20%20}%20%20}%20%20takeoff%20{%20%20%20%20outbound%20{%20%20%20%20%20%20min%20%20%20%20%20%20max%20%20%20%20}%20%20%20%20homebound%20{%20%20%20%20%20%20min%20%20%20%20%20%20max%20%20%20%20}%20%20}}%20%20%20%20&variables={%22departureDateString%22:%222026-02-07%22,%22destination%22:%22ABJ%22,%22filters%22:{%22carrierCodes%22:null,%22connectionTime%22:{%22max%22:0,%22min%22:0},%22landing%22:{%22homebound%22:{%22max%22:0,%22min%22:0},%22outbound%22:{%22max%22:0,%22min%22:0}},%22maxNumberOfStops%22:null,%22overnightFlight%22:true,%22overnightStay%22:true,%22takeoff%22:{%22homebound%22:{%22max%22:0,%22min%22:0},%22outbound%22:{%22max%22:0,%22min%22:0}},%22cabinClass%22:null},%22limit%22:25,%22metadata%22:{%22country%22:%22US%22,%22currency%22:%22USD%22,%22isExperimentEnabled%22:false,%22language%22:%22en%22},%22origin%22:%22KEF%22,%22partner%22:%22easyjet%22,%22passengerAges%22:[25],%22returnDateString%22:null,%22sort%22:%22RECOMMENDED%22,%22utmSource%22:%22easyjet_search_pod%22}'

from primp import Client

client = Client(impersonate='chrome_133', proxy=PROXY)

cookies = {}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-device-memory': '8',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-full-version-list': '"Google Chrome";v="143.0.7499.170", "Chromium";v="143.0.7499.170", "Not A(Brand";v="24.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
}

response = client.get(
    'https://flightconnections.easyjet.com/api/graphql?query=%20%20%20%20query%20searchOutbound($partner:%20Partner!,%20$origin:%20String!,%20$destination:%20String!,%20$passengerAges:%20[PositiveInt!]!,%20$metadata:%20Metadata!,%20$departureDateString:%20String!,%20$returnDateString:%20String,%20$sort:%20Sort,%20$limit:%20PositiveInt,%20$filters:%20OfferFiltersInput,%20$utmSource:%20String)%20{%20%20boundSearch:%20searchOutbound(%20%20%20%20partner:%20$partner%20%20%20%20origin:%20$origin%20%20%20%20destination:%20$destination%20%20%20%20passengerAges:%20$passengerAges%20%20%20%20metadata:%20$metadata%20%20%20%20departureDateString:%20$departureDateString%20%20%20%20returnDateString:%20$returnDateString%20%20%20%20sort:%20$sort%20%20%20%20limit:%20$limit%20%20%20%20filters:%20$filters%20%20%20%20utmSource:%20$utmSource%20%20)%20{%20%20%20%20offers%20{%20%20%20%20%20%20...Offer%20%20%20%20}%20%20%20%20offersFilters%20{%20%20%20%20%20%20...OffersFilters%20%20%20%20}%20%20}}%20%20%20%20%20%20%20%20fragment%20Offer%20on%20Offer%20{%20%20id%20%20journeyId%20%20price%20%20pricePerPerson%20%20outboundPricePerPerson%20%20homeboundPricePerPerson%20%20fareType%20%20currency%20%20transferURL%20%20duration%20%20itinerary%20{%20%20%20%20...Itinerary%20%20}%20%20passengerAges%20%20isOneWay}%20%20%20%20%20%20%20%20fragment%20Itinerary%20on%20Itinerary%20{%20%20outbound%20{%20%20%20%20...Route%20%20}%20%20homebound%20{%20%20%20%20...Route%20%20}}%20%20%20%20%20%20%20%20fragment%20Route%20on%20Route%20{%20%20id%20%20origin%20{%20%20%20%20code%20%20%20%20name%20%20%20%20city%20%20%20%20country%20%20}%20%20destination%20{%20%20%20%20code%20%20%20%20name%20%20%20%20city%20%20%20%20country%20%20}%20%20departure%20%20arrival%20%20duration%20%20operatingCarrier%20{%20%20%20%20name%20%20%20%20code%20%20%20%20flightNumber%20%20}%20%20marketingCarrier%20{%20%20%20%20name%20%20%20%20code%20%20%20%20flightNumber%20%20}%20%20legs%20{%20%20%20%20...Leg%20%20}}%20%20%20%20%20%20%20%20fragment%20Leg%20on%20Leg%20{%20%20id%20%20duration%20%20origin%20{%20%20%20%20code%20%20%20%20name%20%20%20%20city%20%20%20%20country%20%20}%20%20destination%20{%20%20%20%20code%20%20%20%20name%20%20%20%20city%20%20%20%20country%20%20}%20%20departure%20%20arrival%20%20carrierType%20%20operatingCarrier%20{%20%20%20%20name%20%20%20%20code%20%20%20%20flightNumber%20%20}%20%20marketingCarrier%20{%20%20%20%20name%20%20%20%20code%20%20%20%20flightNumber%20%20}}%20%20%20%20%20%20%20%20fragment%20OffersFilters%20on%20OfferFilters%20{%20%20carrierCodes%20%20cabinClass%20%20connectionTime%20{%20%20%20%20min%20%20%20%20max%20%20}%20%20landing%20{%20%20%20%20outbound%20{%20%20%20%20%20%20min%20%20%20%20%20%20max%20%20%20%20}%20%20%20%20homebound%20{%20%20%20%20%20%20min%20%20%20%20%20%20max%20%20%20%20}%20%20}%20%20takeoff%20{%20%20%20%20outbound%20{%20%20%20%20%20%20min%20%20%20%20%20%20max%20%20%20%20}%20%20%20%20homebound%20{%20%20%20%20%20%20min%20%20%20%20%20%20max%20%20%20%20}%20%20}}%20%20%20%20&variables={%22departureDateString%22:%222026-02-07%22,%22destination%22:%22ABJ%22,%22filters%22:{%22carrierCodes%22:null,%22connectionTime%22:{%22max%22:0,%22min%22:0},%22landing%22:{%22homebound%22:{%22max%22:0,%22min%22:0},%22outbound%22:{%22max%22:0,%22min%22:0}},%22maxNumberOfStops%22:null,%22overnightFlight%22:true,%22overnightStay%22:true,%22takeoff%22:{%22homebound%22:{%22max%22:0,%22min%22:0},%22outbound%22:{%22max%22:0,%22min%22:0}},%22cabinClass%22:null},%22limit%22:25,%22metadata%22:{%22country%22:%22US%22,%22currency%22:%22USD%22,%22isExperimentEnabled%22:false,%22language%22:%22en%22},%22origin%22:%22KEF%22,%22partner%22:%22easyjet%22,%22passengerAges%22:[25],%22returnDateString%22:null,%22sort%22:%22RECOMMENDED%22,%22utmSource%22:%22easyjet_search_pod%22}',
    cookies=cookies,
    headers=headers,
)

if response.status_code == 403:
    dd_url = response.json().get('url')
    print(dd_url)
    if 'captcha' in dd_url:
        task_type = 'datadome-slider'
    else:
        task_type = 'datadome-device-check'
    payload = {
        "task_type": task_type,
        "proxy": PROXY,
        "target_url": dd_url,
        "target_method": "GET"
    }
    # if 
    result = run_task(payload)
    if not result:
        raise Exception('Failed to submit task')
    cookies['datadome'] = result.get('datadome')
    headers['user-agent'] = result.get('ua')
    client = Client(impersonate='chrome_133', proxy=PROXY)
    response = client.get(
        'https://flightconnections.easyjet.com/api/graphql?query=%20%20%20%20query%20searchOutbound($partner:%20Partner!,%20$origin:%20String!,%20$destination:%20String!,%20$passengerAges:%20[PositiveInt!]!,%20$metadata:%20Metadata!,%20$departureDateString:%20String!,%20$returnDateString:%20String,%20$sort:%20Sort,%20$limit:%20PositiveInt,%20$filters:%20OfferFiltersInput,%20$utmSource:%20String)%20{%20%20boundSearch:%20searchOutbound(%20%20%20%20partner:%20$partner%20%20%20%20origin:%20$origin%20%20%20%20destination:%20$destination%20%20%20%20passengerAges:%20$passengerAges%20%20%20%20metadata:%20$metadata%20%20%20%20departureDateString:%20$departureDateString%20%20%20%20returnDateString:%20$returnDateString%20%20%20%20sort:%20$sort%20%20%20%20limit:%20$limit%20%20%20%20filters:%20$filters%20%20%20%20utmSource:%20$utmSource%20%20)%20{%20%20%20%20offers%20{%20%20%20%20%20%20...Offer%20%20%20%20}%20%20%20%20offersFilters%20{%20%20%20%20%20%20...OffersFilters%20%20%20%20}%20%20}}%20%20%20%20%20%20%20%20fragment%20Offer%20on%20Offer%20{%20%20id%20%20journeyId%20%20price%20%20pricePerPerson%20%20outboundPricePerPerson%20%20homeboundPricePerPerson%20%20fareType%20%20currency%20%20transferURL%20%20duration%20%20itinerary%20{%20%20%20%20...Itinerary%20%20}%20%20passengerAges%20%20isOneWay}%20%20%20%20%20%20%20%20fragment%20Itinerary%20on%20Itinerary%20{%20%20outbound%20{%20%20%20%20...Route%20%20}%20%20homebound%20{%20%20%20%20...Route%20%20}}%20%20%20%20%20%20%20%20fragment%20Route%20on%20Route%20{%20%20id%20%20origin%20{%20%20%20%20code%20%20%20%20name%20%20%20%20city%20%20%20%20country%20%20}%20%20destination%20{%20%20%20%20code%20%20%20%20name%20%20%20%20city%20%20%20%20country%20%20}%20%20departure%20%20arrival%20%20duration%20%20operatingCarrier%20{%20%20%20%20name%20%20%20%20code%20%20%20%20flightNumber%20%20}%20%20marketingCarrier%20{%20%20%20%20name%20%20%20%20code%20%20%20%20flightNumber%20%20}%20%20legs%20{%20%20%20%20...Leg%20%20}}%20%20%20%20%20%20%20%20fragment%20Leg%20on%20Leg%20{%20%20id%20%20duration%20%20origin%20{%20%20%20%20code%20%20%20%20name%20%20%20%20city%20%20%20%20country%20%20}%20%20destination%20{%20%20%20%20code%20%20%20%20name%20%20%20%20city%20%20%20%20country%20%20}%20%20departure%20%20arrival%20%20carrierType%20%20operatingCarrier%20{%20%20%20%20name%20%20%20%20code%20%20%20%20flightNumber%20%20}%20%20marketingCarrier%20{%20%20%20%20name%20%20%20%20code%20%20%20%20flightNumber%20%20}}%20%20%20%20%20%20%20%20fragment%20OffersFilters%20on%20OfferFilters%20{%20%20carrierCodes%20%20cabinClass%20%20connectionTime%20{%20%20%20%20min%20%20%20%20max%20%20}%20%20landing%20{%20%20%20%20outbound%20{%20%20%20%20%20%20min%20%20%20%20%20%20max%20%20%20%20}%20%20%20%20homebound%20{%20%20%20%20%20%20min%20%20%20%20%20%20max%20%20%20%20}%20%20}%20%20takeoff%20{%20%20%20%20outbound%20{%20%20%20%20%20%20min%20%20%20%20%20%20max%20%20%20%20}%20%20%20%20homebound%20{%20%20%20%20%20%20min%20%20%20%20%20%20max%20%20%20%20}%20%20}}%20%20%20%20&variables={%22departureDateString%22:%222026-02-07%22,%22destination%22:%22ABJ%22,%22filters%22:{%22carrierCodes%22:null,%22connectionTime%22:{%22max%22:0,%22min%22:0},%22landing%22:{%22homebound%22:{%22max%22:0,%22min%22:0},%22outbound%22:{%22max%22:0,%22min%22:0}},%22maxNumberOfStops%22:null,%22overnightFlight%22:true,%22overnightStay%22:true,%22takeoff%22:{%22homebound%22:{%22max%22:0,%22min%22:0},%22outbound%22:{%22max%22:0,%22min%22:0}},%22cabinClass%22:null},%22limit%22:25,%22metadata%22:{%22country%22:%22US%22,%22currency%22:%22USD%22,%22isExperimentEnabled%22:false,%22language%22:%22en%22},%22origin%22:%22KEF%22,%22partner%22:%22easyjet%22,%22passengerAges%22:[25],%22returnDateString%22:null,%22sort%22:%22RECOMMENDED%22,%22utmSource%22:%22easyjet_search_pod%22}',
        cookies=cookies,
        headers=headers,
    )

print(response.text)