
def get_sys_proxies_settings():
  import urllib.request
  proxy_handler = urllib.request.ProxyHandler()
  proxy_settings = proxy_handler.proxies
  return proxy_settings