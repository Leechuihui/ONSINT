**English** | [简体中文](README.zh-CN.md)

# ONSINT

**O**pen-**S**ource **INT**elligence toolkit — email harvesting via Tor with a single command.

[![Python](https://img.shields.io/badge/Python-3.8%2B-3fb950?logo=python&logoColor=white)](https://python.org)
[![Tor](https://img.shields.io/badge/Network-Tor-8b5cf6?logo=tor-project&logoColor=white)](https://torproject.org)
[![License](https://img.shields.io/badge/Use_for_recon_only-blue)](#disclaimer)

## What it does

Harvests publicly exposed email addresses for a target domain by querying search engines **through the Tor network** — no API keys, no accounts, no rate-limit fingerprints on your real IP.

```
$ python3 goog-mail-20s.py example.com
[🎯] Ultra Fast Email Scraper via Tor (20 seconds)
...
contact@example.com
hr@example.com
support@example.com
[✓] 14 unique addresses in 19.8s
```

## Two variants

| Script | Best for |
|---|---|
| `goog-mail.py` | quick single-source pull |
| `goog-mail-20s.py` | concurrent workers, dedupe, ~20s per domain |

## Setup

```bash
# 1. install Tor and start the service
sudo apt update && sudo apt install -y tor
sudo systemctl start tor

# 2. deps
pip install requests

# 3. run (SOCKS5 proxy on 127.0.0.1:9050 is auto-detected)
python3 goog-mail-20s.py target-domain.com
```

## How it works

1. Rotates requests through Tor's SOCKS5 proxy (`127.0.0.1:9050`)
2. Queries search engines for `"<domain>" email OR @<domain>` patterns
3. Strips HTML, regex-extracts addresses, dedupes across workers
4. Prints unique results with timing stats

## Disclaimer

For **authorised reconnaissance** only — your own domains, engagements with written permission, or CTF environments. Harvesting emails for spam or phishing is illegal in most jurisdictions. The authors accept no liability for misuse.

## License

MIT
