
import os


http_proxy = os.environ.get("http_proxy")
https_proxy = os.environ.get("https_proxy")
print("HTTP代理地址：", http_proxy)
print("HTTPS代理地址：", https_proxy)

import urllib.request

proxy_handler = urllib.request.ProxyHandler()
proxy_settings = proxy_handler.proxies

print(f"Proxy settings: {proxy_settings}")