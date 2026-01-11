# -*- coding: utf-8 -*-
# RiskByPass 面板 + TruePeopleSearch 完整爬取流程 (修复版)
# 修复: 使用Session保持Cookie和IP一致性
# 依赖: pip install requests curl_cffi

import requests
import time
import json
import random
import string
from urllib.parse import urljoin, quote
from curl_cffi import requests as c_requests

BASE_URL = "https://riskbypass.com"
TOKEN = "Your Token"
TIMEOUT = 60
PROXY = "http://username:password@host:port"

def get_random_session_id():
    """生成随机session ID用于代理轮换"""
    return ''.join(random.sample(string.ascii_letters + string.digits, 8))

def get_proxy():
    """获取代理地址"""
    session_id = get_random_session_id()
    return PROXY

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


def bypass_datadome(target_url, proxy):
    """
    通过RiskByPass绕过DataDome检测
    
    Args:
        target_url: 目标URL
        proxy: 代理地址
        
    Returns:
        dict: 包含datadome cookie的结果
    """
    payload = {
        "task_type": "datadome-device-check",
        "proxy": proxy,
        "target_url": target_url,
        "target_method": "GET"
    }
    return run_task(payload)


def bypass_turnstile(target_url, site_key, proxy):
    """
    通过RiskByPass绕过Cloudflare Turnstile
    
    Args:
        target_url: 验证码页面URL
        site_key: Turnstile sitekey
        proxy: 代理地址
        
    Returns:
        dict: 包含token的结果
    """
    payload = {
        "task_type": "turnstile",
        "proxy": proxy,
        "target_url": target_url,
        "site_key": site_key
    }
    return run_task(payload)


def extract_return_url(html_content, default_url):
    """
    从HTML中提取returnUrl
    
    Args:
        html_content: HTML内容
        default_url: 默认URL
        
    Returns:
        str: 提取或默认的returnUrl
    """
    import re
    from urllib.parse import unquote
    
    # 尝试从表单action中提取
    match = re.search(r'action="([^"]*\?returnUrl=([^"&]*))', html_content)
    if match and match.group(2):
        try:
            return_url = unquote(match.group(2))
            print(f"[*] 从HTML中提取到 returnUrl: {return_url}")
            return return_url
        except:
            pass
    
    # 默认返回提供的URL
    return default_url

def main():
    """主流程"""
    
    # ============================================================================
    # 配置
    # ============================================================================
    
    PHONE_NO = "(213)937-9027"
    TARGET_URL = "https://www.truepeoplesearch.com/find/person/p4ul60n4nur98r62u48n"
    PROXY = get_proxy()
    
    print(f"\n{'='*70}")
    print(f"[*] TruePeopleSearch 爬取流程 (修复版)")
    print(f"[*] 目标: {TARGET_URL}")
    print(f"[*] 代理: {PROXY.split('@')[1]}")
    print(f"{'='*70}\n")
    
    # ============================================================================
    # 关键: 创建持久Session，保持Cookie和代理一致
    # ============================================================================
    
    crawler_session = c_requests.Session(impersonate='chrome136')
    crawler_session.proxies = {
        'http': PROXY,
        'https': PROXY
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Upgrade-Insecure-Requests': '1',
        'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    
    # ============================================================================
    # 步骤1: DataDome 绕过
    # ============================================================================
    
    print("[STEP 1] 绕过 DataDome 检测")
    print("-" * 70)
    
    datadome_results = bypass_datadome(TARGET_URL, PROXY)
    if not datadome_results:
        print("[!] DataDome绕过失败")
        return False
    
    datadome_cookie = datadome_results.get('datadome')
    print(f"[+] DataDome Cookie 获取成功 (长度: {len(datadome_cookie)})\n")
    crawler_session.cookies.update({'datadome': datadome_cookie})
    
    # ============================================================================
    # 步骤2: 初始请求（使用Session保持Cookie）
    # ============================================================================
    
    print("[STEP 2] 发送初始请求")
    print("-" * 70)
    
    try:
        response = crawler_session.get(
            TARGET_URL,
            headers=headers,
            allow_redirects=True,
            timeout=30
        )
        
        print(f"[+] 状态码: {response.status_code}")
        print(f"[+] 最终URL: {response.url}")
                
        with open('step2_response.html', 'w', encoding='utf8') as f:
            f.write(response.text)
        print(f"[+] 响应已保存到 step2_response.html\n")
        
    except Exception as e:
        print(f"[!] 初始请求异常: {repr(e)}")
        return False
    
    # ============================================================================
    # 步骤3: 检查是否触发验证码
    # ============================================================================
    
    if 'Captcha' in response.url or 'captcha' in response.text.lower():
        print("[STEP 3] 检测到验证码，启动 Turnstile 绕过")
        print("-" * 70)
        
        # 绕过Turnstile
        cf_results = bypass_turnstile(
            response.url,
            site_key="0x4AAAAAAAmywfqBst8n7ro5",
            proxy=PROXY
        )
        
        if not cf_results:
            print("[!] Turnstile绕过失败")
            return False
        
        token = cf_results.get('token')
        print(f"[+] Turnstile Token 获取成功 (长度: {len(token)})\n")
        
        # ====================================================================
        # 步骤4: 提交验证码token (关键: 使用同一Session)
        # ====================================================================
        
        print("[STEP 4] 提交验证码token")
        print("-" * 70)
        
        return_url = extract_return_url(response.text, TARGET_URL)
        print(f"[*] Return URL: {return_url}\n")
        
        try:
            submit_result = crawler_session.post(
                'https://www.truepeoplesearch.com/internalcaptcha/captchasubmit',
                params={
                    'returnUrl': return_url,
                    'rrstamp': '900'
                },
                data={'captchaToken': token},
                headers={
                    **headers,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                timeout=30
            )
            
            print(f"[+] 提交状态码: {submit_result.status_code}")
            print(f"[+] 提交验证码响应内容: {submit_result.text}")
            
            submit_json = submit_result.json()
            print(f"[+] 响应: {json.dumps(submit_json, ensure_ascii=False, indent=2)}\n")
            
            if not submit_json.get('success'):
                print("[!] 验证码验证失败")
                return False
            
        except Exception as e:
            print(f"[!] 提交验证码异常: {repr(e)}")
            return False
        
        # ====================================================================
        # 步骤5: 跟随重定向获取最终结果 (关键: 继续使用同一Session)
        # ====================================================================
        
        print("[STEP 5] 获取最终结果")
        print("-" * 70)
        
        redirect_url = submit_json.get('redirectUrl')
        print(f"[*] 重定向URL: {redirect_url}\n")
        
        try:
            final_response = crawler_session.get(
                redirect_url,
                headers=headers,
                allow_redirects=True,
                timeout=30
            )
            
            print(f"[+] 最终状态码: {final_response.status_code}")
            print(f"[+] 最终URL: {final_response.url}")
                        
            # 检查是否真正获得了内容（而不是又回到验证码）
            if 'Captcha' in final_response.url or 'InternalCaptcha' in final_response.url:
                print("\n[!] ⚠️  警告: 最终URL仍然指向验证码!")
                print("[!] 这通常表示:")
                print("    1. IP不匹配 (验证码IP ≠ 当前IP)")
                print("    2. Cookie丢失或被重置")
                print("    3. Token已过期")
                print("    4. 验证码验证实际失败")
                return False
            
            with open('final_result.html', 'w', encoding='utf8') as f:
                f.write(final_response.text)
            
            print(f"\n[+] 最终结果已保存到 final_result.html")
            
            # 验证页面内容是否有效
            if len(final_response.text) < 1000:
                print("[!] ⚠️  警告: 返回的HTML过短，可能不是有效的结果页面")
                with open('final_result.html', 'r') as f:
                    content = f.read()
                    if 'person' not in content.lower() or 'result' not in content.lower():
                        print("[!] 页面内容不包含预期的关键词")
            
            return True
        
        except Exception as e:
            print(f"[!] 获取最终页面异常: {repr(e)}")
            return False
    
    else:
        # 直接获取成功，没有验证码
        print("[+] 无需验证码，直接获取成功！\n")
        
        with open('final_result.html', 'w', encoding='utf8') as f:
            f.write(response.text)
        
        print(f"[+] 结果已保存到 final_result.html\n")
        
        return True


if __name__ == "__main__":
    try:
        success = main()
        if success:
            print(f"\n{'='*70}")
            print("[✓] 爬取完成！")
            print(f"{'='*70}")
        else:
            print(f"\n{'='*70}")
            print("[✗] 爬取失败")
            print(f"{'='*70}")
    except Exception as e:
        print(f"\n[!] 程序异常: {repr(e)}")
        import traceback
        traceback.print_exc()