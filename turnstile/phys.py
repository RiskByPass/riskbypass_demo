# -*- coding: utf-8 -*-
"""
Turnstile HTML Unlocker
-----------------------
输入 URL + 代理，自动判断是否 403 Turnstile 拦截页。
如果是 → 解析 sitekey / submit-url / server-ts → RiskByPass 过验证 → 带 cookie 重新访问
如果不是 → 直接返回 response
"""

import re
import json
import logging
from urllib.parse import urljoin

import requests
from riskbypass import RiskByPassClient

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


# ─── 配置 ────────────────────────────────────────────────────────────
RISKBYPASS_BASE_URL = "https://riskbypass.com"
RISKBYPASS_TOKEN = "your token"
TASK_TIMEOUT = 120

# 默认请求头，模拟正常浏览器
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


# ─── HTML 解析工具 ───────────────────────────────────────────────────
def _extract_sitekey(html: str):
    """从 turnstile.render 调用或 data-sitekey 属性中提取 sitekey"""
    # 方式1: JS 中的 sitekey: '...'
    m = re.search(r"""sitekey\s*:\s*['"]([0-9a-zA-Zx_-]+)['"]""", html)
    if m:
        return m.group(1)
    # 方式2: data-sitekey="..."
    m = re.search(r'data-sitekey\s*=\s*["\']([0-9a-zA-Zx_-]+)["\']', html)
    if m:
        return m.group(1)
    return None


def _extract_submit_url(html: str):
    """从 <html data-submit-url="..."> 提取提交路径"""
    m = re.search(r'data-submit-url\s*=\s*["\']([^"\']+)["\']', html)
    return m.group(1) if m else None


def _extract_server_ts(html: str):
    """从 <html data-server-ts="..."> 提取时间戳"""
    m = re.search(r'data-server-ts\s*=\s*["\']([^"\']+)["\']', html)
    return m.group(1) if m else None


def _is_turnstile_challenge(status_code: int, html: str) -> bool:
    """判断是否为 Turnstile 拦截页"""
    if status_code != 403:
        return False
    # 特征: 页面包含 turnstile 相关内容
    indicators = [
        "challenges.cloudflare.com/turnstile",
        "turnstile.render",
        "data-sitekey",
        "cf-turnstile",
    ]
    html_lower = html.lower()
    return any(ind.lower() in html_lower for ind in indicators)


# ─── 核心逻辑 ────────────────────────────────────────────────────────
def unlock(
    url: str,
    proxy = None,
    *,
    riskbypass_base_url: str = RISKBYPASS_BASE_URL,
    riskbypass_token: str = RISKBYPASS_TOKEN,
    timeout: int = TASK_TIMEOUT,
    extra_headers = None,
) -> requests.Response:
    """
    访问目标 URL，若遇到 Turnstile 403 则自动解锁并返回解锁后的 response。

    Parameters
    ----------
    url : str
        目标页面 URL
    proxy : str | None
        代理地址，格式: http://user:pass@ip:port
    riskbypass_base_url : str
        RiskByPass API 地址
    riskbypass_token : str
        RiskByPass API Token
    timeout : int
        任务超时时间（秒）
    extra_headers : dict | None
        额外请求头

    Returns
    -------
    requests.Response
        最终拿到的 response（已解锁或无需解锁）
    """

    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    if extra_headers:
        session.headers.update(extra_headers)

    proxies = {"http": proxy, "https": proxy} if proxy else None

    # ── 第一次请求 ──
    log.info(f"GET {url}")
    resp = session.get(url, proxies=proxies, timeout=30, allow_redirects=True)
    log.info(f"Status: {resp.status_code}  Length: {len(resp.text)}")

    if not _is_turnstile_challenge(resp.status_code, resp.text):
        log.info("无 Turnstile 拦截，直接返回")
        return resp

    # ── 解析挑战页 ──
    html = resp.text
    sitekey = _extract_sitekey(html)
    submit_path = _extract_submit_url(html)
    server_ts = _extract_server_ts(html)

    if not sitekey:
        raise RuntimeError("未能从拦截页提取 sitekey")
    if not submit_path:
        raise RuntimeError("未能从拦截页提取 submit-url")

    submit_url = urljoin(url, submit_path)
    log.info(f"Turnstile 拦截 → sitekey={sitekey}  submit={submit_url}  ts={server_ts}")

    # ── 调用 RiskByPass 解 Turnstile ──
    client = RiskByPassClient(token=riskbypass_token, base_url=riskbypass_base_url)

    payload = {
        "task_type": "turnstile",
        "target_url": url,
        "site_key": sitekey,
    }
    if proxy:
        payload["proxy"] = proxy

    log.info("提交 Turnstile 任务到 RiskByPass …")
    result = client.run_task(payload, timeout=timeout)
    log.info(f"RiskByPass 结果: {json.dumps(result, ensure_ascii=False)[:200]}")

    # 提取 turnstile token (兼容不同返回结构)
    turnstile_token = None
    if isinstance(result, dict):
        turnstile_token = (
            result.get("token")
            or result.get("turnstile_token")
            or (result.get("solution", {}) or {}).get("token")
        )
    if not turnstile_token:
        raise RuntimeError(f"RiskByPass 未返回有效 token: {result}")

    log.info(f"Turnstile token: {turnstile_token[:40]}…")

    # ── 提交验证 ──
    verify_headers = {
        "x-turnstile-token": turnstile_token,
        "Content-Type": "application/json",
    }
    if server_ts:
        verify_headers["x-request-ts"] = server_ts

    log.info(f"GET {submit_url}  (带 turnstile token)")
    verify_resp = session.get(
        submit_url,
        headers=verify_headers,
        proxies=proxies,
        timeout=30,
        allow_redirects=True,
    )
    log.info(f"验证响应: {verify_resp.status_code}")

    if not verify_resp.ok:
        raise RuntimeError(
            f"Turnstile 验证提交失败: HTTP {verify_resp.status_code}\n{verify_resp.text[:500]}"
        )

    # ── 验证通过后，重新访问原始 URL（此时 session 已携带解锁 cookie）──
    log.info(f"重新访问 {url} …")
    final_resp = session.get(url, proxies=proxies, timeout=30, allow_redirects=True)
    log.info(f"最终状态: {final_resp.status_code}  Length: {len(final_resp.text)}")

    return final_resp


# ─── CLI 入口 ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    url = "https://phys.org/news/2026-02-ai-roman-era-board-game.html"
    proxy = "http://username:password@host:port"
    resp = unlock(url, proxy)
    print(resp.status_code)
    print(resp.text[:100])