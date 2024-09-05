import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

def get_tariff(code):
    # https://www.trade-tariff.service.gov.uk/commodities/3926300040
    url = f"https://www.trade-tariff.service.gov.uk/commodities/{code}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)
    open('soup.html', 'w', encoding='utf-8').write(soup.prettify())
    # 这里需要根据实际网页结构调整选择器
    if len(str(code)) == 10:
        tariff_element = soup.select_one('.duty-expression')
    else:
        tariff_element = soup.select_one('.commodities')

    print(tariff_element)
    if tariff_element:
        return tariff_element.text.strip()
    else:
        return "未找到关税信息"

def process_excel(file_path):
    # 读取Excel文件
    df = pd.read_excel(file_path)

    # 假设海关编码列名为 'HS Code'
    df['Tariff'] = df['HS Code'].apply(get_tariff)

    # 保存结果到新的Excel文件
    output_file = 'output_tariffs.xlsx'
    df.to_excel(output_file, index=False)
    print(f"结果已保存到 {output_file}")

# 使用示例
file_path = '1.xlsx'  # 替换为您的Excel文件路径
process_excel(file_path)