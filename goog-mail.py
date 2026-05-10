#!/usr/bin/env python3

import sys
import re
import requests
import urllib.parse

def strip_tags(text):
    return re.sub('<[^<]+>', '', text)

if len(sys.argv) != 2:
    print("\nExtracts emails from DuckDuckGo via Tor Network.")
    print("Usage: python3 ddg-tor-mail.py <domain>\n")
    sys.exit(1)

domain_name = sys.argv[1]
unique_emails = set()

query = f'"{domain_name}" email OR @{domain_name}'
encoded_query = urllib.parse.quote(query)
url = f"https://html.duckduckgo.com/html/?q={encoded_query}"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0', # 伪装成 Tor Browser 的 UA
    'Accept-Language': 'en-US,en;q=0.5'
}

# 配置 Tor SOCKS5 代理 (使用 socks5h 让 DNS 解析也走 Tor 网络)
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

print(f"[*] Routing traffic through Tor network (127.0.0.1:9050) ...")
print(f"[*] Searching DuckDuckGo for {domain_name} ...\n")

try:
    # 测试一下当前的 Tor IP
    ip_check = requests.get('https://api.ipify.org', proxies=proxies, timeout=10)
    print(f"[+] Current Tor Exit Node IP: {ip_check.text}")

    # 请求 DuckDuckGo
    response = requests.get(url, headers=headers, proxies=proxies, timeout=15)
    response.raise_for_status()
    
    clean_text = strip_tags(response.text)
    
    # 正则匹配邮箱
    pattern = r'([a-zA-Z0-9.\-_]+@' + re.escape(domain_name) + r')'
    emails_found = re.findall(pattern, clean_text)
    
    for email in emails_found:
        unique_emails.add(email.lower())

except requests.exceptions.RequestException as e:
    print(f"[!] Network Error via Tor: {e}")
except Exception as e:
    print(f"[!] An error occurred: {e}")

if unique_emails:
    print("\n[+] Emails found:")
    for email in unique_emails:
        print(email)
else:
    print("\n[-] No emails found.")
