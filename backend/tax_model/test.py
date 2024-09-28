import logging
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_sys_proxies_settings():
  # import urllib.request
  # proxy_handler = urllib.request.ProxyHandler()
  # proxy_settings = proxy_handler.proxies
  # return proxy_settings
  return {
    "http": '',
    "https": "",
  }

logger = logging.getLogger('log')
logger.setLevel(logging.DEBUG)

proxies = get_sys_proxies_settings()

def get_full_code(code):
  url = f"https://www.trade-tariff.service.gov.uk/commodities/{code}"
  logger.info(f"请求地址：{url}")
  response = requests.get(url, proxies=proxies)
  soup = BeautifulSoup(response.text, 'html.parser')
  tariff_element = soup.select_one('.duty-expression')
  if tariff_element:
    return tariff_element.text.strip()
  return None

def get_search_code(code):
  # https://www.trade-tariff.service.gov.uk/search_suggestions.json?term=392630
  logger.info(f"不是完整编码：{code}, 开始搜索")
  url = f"https://www.trade-tariff.service.gov.uk/search_suggestions.json?term={code}"
  logger.info(f"请求地址：{url}")
  response = requests.get(url, proxies=proxies)
  result = response.json()
  logger.info(f"搜索结果：{result}")
  if result:
    # 获取第一个结果
    first_result = result['results'][0]
    logger.info(f"第一个结果：{first_result}")
    if first_result:
      source_id = first_result['resource_id']
    else:
      source_id = 'undefined'
    logger.info(f"获得source_id：{source_id}")
    # https://www.trade-tariff.service.gov.uk/search?q=392630&resource_id=39520
    search_url = f"https://www.trade-tariff.service.gov.uk/search?q={code}&resource_id={source_id}"
    logger.info(f"搜索地址：{search_url}")
    # 获得重定向
    response = requests.get(search_url, proxies=proxies)
    # 获得重定向后的url
    redirect_url = response.url
    logger.info(f"重定向地址：{redirect_url}")
    # 获得重定向后的网页内容
    response = requests.get(redirect_url, proxies=proxies)
    soup = BeautifulSoup(response.text, 'html.parser')
    # 获得重定向后的网页内容
    tariff_element = soup.select_one('.commodities .last-child .vat')

    tariff_element2 = soup.select_one('.duty-expression')

    # 第三种情况
    tariff_element3 = soup.select_one(".commodities .last-child .govuk-table .govuk-table__body .govuk-table__row:last-child .govuk-table__cell:last-child")
    if tariff_element3:
      tax = tariff_element3.text.strip()
      print(tax)
      logger.info(f"获得关税信息3：{tax}")
      return tax
    if tariff_element:
      tax = tariff_element.text.strip()
      logger.info(f"获得关税信息1：{tax}")
      return tax
    elif tariff_element2:
      tax = tariff_element2.text.strip()
      logger.info(f"获得关税信息2：{tax}")
      return tax
    else:
      logger.info(f"未找到关税信息")
      return None
  return None


def get_tariff(code):
    try:
      logger.info(f"开始处理：{code}")
      # 这里需要根据实际网页结构调整选择器
      if len(str(code)) == 10:
        res = get_full_code(code)
      else:
        res = get_search_code(code)

      if res:
        # 去掉所有的空格
        res = res.replace(' ', '')
        return res
      else:
        return None
    except Exception as e:
      pass
      logger.info(f"{code}处理失败")
      return None

def process_excel(file_path):

  try:
    logger.info("开始处理Excel文件：%s", file_path)
    # 读取Excel文件
    df = pd.read_excel(file_path)

    logger.info("读取文件成功")

    logger.info(f"当前系统代理：{proxies}")

    # 假设海关编码列名为 'HS Code'
    df['Tariff'] = df['HS Code'].apply(get_tariff)

    # 保存结果到新的Excel文件
    file_name, file_extension = os.path.splitext(os.path.basename(file_path))
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    new_file_name = f"{file_name}_关税导出{file_extension}"
    output_file = os.path.join(desktop_path, new_file_name)
    df.to_excel(output_file, index=False)
    logger.info(f"结果已保存到 {output_file}")
  except Exception as e:
    logger.error(f"处理出错：{e}")

# 使用示例
# file_path = '1.xlsx'  # 替换为您的Excel文件路径
# process_excel(file_path)

if __name__ == '__main__':
  try:
    print('===开始')
    res = get_tariff('392630')
    print(res)
  except Exception as e:
    print(e)