#!/usr/bin/env python3
import sys, re, requests, urllib.parse, time, random
from concurrent.futures import ThreadPoolExecutor, as_completed

def strip_tags(text): return re.sub('<[^<]+>', '', text)

if len(sys.argv) != 2:
    print("\n[🎯] Ultra Fast Email Scraper via Tor (20 seconds)")
    print("Usage: python3 goog-mail-20s.py <domain>\n")
    sys.exit(1)

start_time = time.time()
domain_name = sys.argv[1]
unique_emails = set()

# 30 个深度查询
search_queries = []
# 基础查询
for q in [f'"{domain_name}"', f'@{domain_name}', f'site:{domain_name}']:
    for ext in ['email', 'mail', 'contact', 'admin', 'support', 'info', 'help', 'service']:
        search_queries.append(f'{q} {ext}')
        search_queries.append(f'"{q}" "{ext}"')

# 域名扩展查询
for suffix in ['com', 'cn', 'org', 'net', 'cn', 'edu', 'gov', 'io', 'biz']:
    search_queries.append(f'@{domain_name} site:{suffix}')
    search_queries.append(f'site:{domain_name}.{suffix}')

# 特殊查询
for q in ['filetype:pdf', 'filetype:xls', 'filetype:csv', 'inurl:contact', 'intitle:contact', 'inurl:email', 'intext:email']:
    search_queries.append(f'{domain_name} {q}')

# 平台查询
for platform in ['linkedin', 'facebook', 'twitter', 'github', 'medium']:
    search_queries.append(f'site:{platform}.com {domain_name}')

# 去重
search_queries = list(set(search_queries))[:30]

# 25 个引擎
engines = [
    ('DuckDuckGo', 'https://html.duckduckgo.com/html/?q={query}', 0.3, 2),
    ('Google', 'https://www.google.com/search?q={query}', 0.4, 3),
    ('Google UK', 'https://www.google.co.uk/search?q={query}', 0.4, 3),
    ('Google HK', 'https://www.google.hk/search?q={query}', 0.4, 3),
    ('Bing', 'https://www.bing.com/search?q={query}', 0.3, 2),
    ('Bing CN', 'https://cn.bing.com/search?q={query}', 0.3, 2),
    ('Baidu', 'https://www.baidu.com/s?wd={query}', 0.3, 2),
    ('Sogou', 'https://www.sogou.com/web?query={query}', 0.3, 2),
    ('360', 'https://www.so.com/s?q={query}', 0.3, 2),
    ('Yahoo', 'https://search.yahoo.com/search?p={query}', 0.3, 2),
    ('Yahoo CN', 'https://cn.yahoo.com/search?p={query}', 0.3, 2),
    ('Qwant', 'https://www.qwant.com/?q={query}', 0.3, 2),
    ('Startpage', 'https://www.startpage.com/sp/search?q={query}', 0.4, 3),
    ('Ecosia', 'https://www.ecosia.com/search?q={query}', 0.3, 2),
    ('QQ 搜索', 'https://search.qq.com/?s={query}', 0.3, 2),
    ('Shodan', 'https://api.shodan.io/search?query={query}&key=', 0.5, 3),
    ('Fofa', 'https://fofa.so/result?q={query}', 0.5, 3),
    ('ZoomEye', 'https://www.zoomeye.org/searchResult?q={query}', 0.5, 3),
    ('Pastebin', 'https://pastebin.com/search?q={query}', 0.3, 2),
    ('Wayback', 'https://web.archive.org/search?q={query}', 0.3, 2),
    ('Github', 'https://github.com/search?q={query}&type=repositories', 0.4, 3),
    ('GitLab', 'https://gitlab.com/search?q={query}', 0.4, 3),
    ('StackOverflow', 'https://stackoverflow.com/search?q={query}', 0.3, 2),
    ('Medium', 'https://medium.com/search?q={query}', 0.3, 2),
    ('CrunchBase', 'https://www.crunchbase.com/search?search={query}', 0.4, 3),
]

proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
}

print(f"[*] Tor: 127.0.0.1:9050 | Domain: {domain_name}")
print(f"[*] Queries: {len(search_queries)} | Engines: {len(engines)} | {len(search_queries)*len(engines)} searches\n")

ip = requests.get('https://api.ipify.org', proxies=proxies, timeout=5, verify=False)
print(f"[+] Current IP: {ip.text.strip()}")

def search(engine_name, url, q_idx, min_delay, retries):
    ua = random.choice([
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/122.0.0.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/122.0.0.0',
        'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/122.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/17.2',
    ])
    hdrs = headers.copy()
    hdrs['User-Agent'] = ua
    
    time.sleep(min_delay * random.uniform(0.5, 1.2))
    
    for attempt in range(retries + 1):
        try:
            resp = requests.get(url, headers=hdrs, proxies=proxies, timeout=25, verify=False, allow_redirects=True)
            if resp.status_code == 200:
                return engine_name, resp.text, True, q_idx, attempt
            elif resp.status_code == 429 and attempt < retries:
                time.sleep(1)
            elif resp.status_code in [403, 503] and attempt < retries:
                time.sleep(0.5)
        except Exception as e:
            if attempt < retries: time.sleep(0.5)
            continue
    return engine_name, "", False, q_idx, 503

with ThreadPoolExecutor(max_workers=50) as executor:
    futures = []
    for q_idx, query in enumerate(search_queries):
        for (eng_name, eng_url, min_delay, retries) in engines:
            url = eng_url.format(query=urllib.parse.quote(query))
            futures.append(executor.submit(search, eng_name, url, q_idx, min_delay, retries))
    
    total = len(futures)
    seen = set()
    
    for future in as_completed(futures):
        eng_name, text, success, q_idx, status = future.result(timeout=30)
        if success:
            clean = strip_tags(text)
            emails = re.findall(r'[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', clean)
            for e in emails:
                e_lower = e.lower()
                if domain_name.lower() in e_lower and e_lower not in seen:
                    seen.add(e_lower)
                    unique_emails.add(e_lower)
    
    # 打印结果
    for eng_name, text, success, q_idx, status in [f.result(timeout=30) for f in futures]:
        if success:
            clean = strip_tags(text)
            emails = re.findall(r'[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', clean)
            valid = [e for e in emails if domain_name.lower() in e.lower()]
            if valid and (eng_name, q_idx) not in seen:
                seen.add((eng_name, q_idx))
                print(f"[+] [{q_idx+1}/{total}] {eng_name}: {len(valid)} emails")

elapsed = time.time() - start_time
print(f"\n[*] Totoal Time：{elapsed:.2f}秒")
print(f"[+] Finds email ({len(unique_emails)} 个):")
for email in sorted(unique_emails): print(f"    {email}")
