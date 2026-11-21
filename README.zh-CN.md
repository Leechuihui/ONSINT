[English](README.md) | **简体中文**

# ONSINT

**O**pen-**S**ource **INT**elligence（开源情报）工具集 — 一条命令，经由 Tor 收集邮箱地址。

[![Python](https://img.shields.io/badge/Python-3.8%2B-3fb950?logo=python&logoColor=white)](https://python.org)
[![Tor](https://img.shields.io/badge/Network-Tor-8b5cf6?logo=tor-project&logoColor=white)](https://torproject.org)
[![License](https://img.shields.io/badge/Use_for_recon_only-blue)](#disclaimer)

## 它做什么

通过 **Tor 网络**查询搜索引擎，收集目标域名上公开暴露的邮箱地址——无需 API 密钥，无需账号，不会在你的真实 IP 上留下限流指纹。

```
$ python3 goog-mail-20s.py example.com
[🎯] Ultra Fast Email Scraper via Tor (20 seconds)
...
contact@example.com
hr@example.com
support@example.com
[✓] 14 unique addresses in 19.8s
```

## 两种变体

| 脚本 | 适用场景 |
|---|---|
| `goog-mail.py` | 快速的单源抓取 |
| `goog-mail-20s.py` | 并发 worker、去重，每个域名约 20 秒 |

## 环境搭建

```bash
# 1. 安装 Tor 并启动服务
sudo apt update && sudo apt install -y tor
sudo systemctl start tor

# 2. 依赖
pip install requests

# 3. 运行（自动检测 127.0.0.1:9050 上的 SOCKS5 代理）
python3 goog-mail-20s.py target-domain.com
```

## 工作原理

1. 通过 Tor 的 SOCKS5 代理（`127.0.0.1:9050`）轮转请求
2. 以 `"<domain>" email OR @<domain>` 模式查询搜索引擎
3. 剥离 HTML，正则提取地址，跨 worker 去重
4. 输出去重后的结果及耗时统计

## 免责声明

仅用于**获授权的侦察**——你自己的域名、持有书面许可的委托项目，或 CTF 环境。在大多数司法辖区，为垃圾邮件或钓鱼收集邮箱均属违法行为。作者对滥用行为不承担任何责任。

## 许可证

MIT
