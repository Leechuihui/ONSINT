#!/usr/bin/env python3

import sys
import re
import urllib.request
import urllib.parse

def strip_tags(text):
    """移除 HTML 标签"""
    return re.sub('<[^<]+>', '', text)

if len(sys.argv) != 2:
    print("\nExtracts emails from DuckDuckGo results.")
    print("Usage: python3 ddg-mail.py <domain>\n")
    sys.exit(1)

domain_name = sys.argv[1]
# 使用 set 自动去重，替代原来的字典
unique_emails = set()

# DuckDuckGo 的纯 HTML 节点，不需要执行 JavaScript
query = f'"{domain_name}" email OR @{domain_name}'
encoded_query = urllib.parse.quote(query)
url = f"https://html.duckduckgo.com/html/?q={encoded_query}"

# 伪造一个现代的浏览器 User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

print(f"[*] Searching DuckDuckGo for {domain_name} ...\n")

try:
    # 发起请求
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    html_content = response.read().decode('utf-8', errors='ignore')
    
    # 清理 HTML 标签
    clean_text = strip_tags(html_content)
    
    # 正则匹配邮箱
    # 使用 re.escape 确保域名中的特殊字符（如.）被正确转义
    pattern = r'([a-zA-Z0-9.\-_]+@' + re.escape(domain_name) + r')'
    emails_found = re.findall(pattern, clean_text)
    
    for email in emails_found:
        unique_emails.add(email.lower())

except urllib.error.HTTPError as e:
    print(f"[!] HTTP Error: {e.code} - DuckDuckGo might be blocking the request.")
except Exception as e:
    print(f"[!] Cannot connect to DuckDuckGo: {e}")

# 输出结果
if unique_emails:
    print("[+] Emails found:")
    for email in unique_emails:
        print(email)
else:
    print("[-] No emails found.")