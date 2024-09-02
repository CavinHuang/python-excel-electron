import asyncio
import sys
from pyppeteer import launch
from lxml import etree
import requests
import ddddocr
from anti_useragent import UserAgent
import os
import time

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
local_image_tmp = os.path.join(desktop_path, '_tmp-images')

VALID_DOMAIN_NAMES = [
    "amazon.com",
    "amazon.ca",
    "amazon.co.uk",
    "amazon.de",
    "amazon.fr",
    "amazon.in",
    "amazon.it",
    "amazon.co.jp",
    "amazon.cn",
    "amazon.com.mx",
    "amazon.com.au",
    "amazon.nl",
    "amazon.pl",
    "amazon.sg",
    "amazon.sa",
    "amazon.es",
    "amazon.se",
    "amazon.ae",
    "amazon.br",
    "amazon.com.tr",
    "amzn.to",
]

# 识别验证码
def find_image(code_path):
    ocr = ddddocr.DdddOcr()
    with open(code_path, 'rb') as f:
        img_bytes = f.read()
    result = ocr.classification(img_bytes)
    return result

ua = UserAgent()

cache_product_price = {}
cache_product_image = {}

browser = None
async def start_browser():
  global browser
  if browser is None:
    browser = await launch({
      "headless": True,
      "defaultViewport": None,
      "args": ['--lang=en-US', '--no-sandbox', '--disable-setuid-sandbox'],
      "handleSIGINT": False,
      "handleSIGTERM": False,
      "handleSIGHUP": False,
    })
  return browser

async def main(url, file_full_name, logger, image_in_cell, isPrice, isFetchImg):
    '''
    :param ASIN: 商品的对应asin
    :return:
    '''

    fetch_image_success = False
    if isFetchImg is True:
      if image_in_cell is not False:
        fetch_image_success = True
        print("========存在图片")

      if url in cache_product_image and fetch_image_success is not True:
        fetch_image_success = True
        logger.info('从缓存中获取图片')
        print('从缓存中获取图片')


    fetch_price = None
    if isPrice is True:
      if url in cache_product_price:
        fetch_price = cache_product_price[url]
        logger.info('从缓存中获取价格')
        print('从缓存中获取价格', fetch_price)

    if fetch_image_success and fetch_price:
      logger.info('从缓存中获取图片和价格')
      print('从缓存中获取图片和价格')
      return fetch_image_success, fetch_price

    if isPrice is not True and isFetchImg is not True:
      logger.info('没有开启价格获取和图片获取')
      return fetch_image_success, fetch_price

    url = f'{url}'
    logger.info(f"开始获取图片和价格{url}")
    logger.info(f"{getattr(sys, 'frozen', False)}")
    print(f"{getattr(sys, 'frozen', False)}")
    if getattr(sys, 'frozen', False):
      chromium_path = os.path.join(sys._MEIPASS, 'pyppeteer', 'local-chromium')
      # 在 Windows 上，可能需要进一步指定可执行文件路径
      if sys.platform == 'win32':
        chromium_path = os.path.join(chromium_path, 'chrome.exe')
      logger.info(f"chromium_path: {chromium_path}")
      print(f"chromium_path: {chromium_path}")
      browser = await launch({
        "headless": True,
        "defaultViewport": {
          "width": 1920,
          "height": 1080
        },
        "args": ['--lang=en-US', '--no-sandbox', '--disable-setuid-sandbox'],
        "handleSIGINT": False,
        "handleSIGTERM": False,
        "handleSIGHUP": False,
        "executablePath": chromium_path,
      })
    else:
      logger.info('==============else==============')
      browser = await launch({
        "headless": False,
        "defaultViewport": {
          "width": 1920,
          "height": 1080
        },
        "args": ['--lang=en-US', '--no-sandbox', '--disable-setuid-sandbox'],
        "handleSIGINT": False,
        "handleSIGTERM": False,
        "handleSIGHUP": False,
      })
    page = await browser.newPage()

    desktop_ua = ua.random

    # 确保我们获得的是桌面版 User-Agent
    while 'Mobile' in desktop_ua or 'Android' in desktop_ua or 'iPhone' in desktop_ua:
        desktop_ua = ua.random

    await page.setUserAgent(desktop_ua)
    await page.setViewport({'width': 1920, 'height': 1080})

    try:
        # 保证页面加载完成
        await page.goto(url, waitUntil='domcontentloaded')
        # await page.waitForNavigation(waitUntil='networkidle0', timeout=10000)
        while True:
            htm = await page.content()
            html = etree.HTML(htm)
            image = html.xpath('//div[@class="a-row a-text-center"]/img/@src')
            if image:
              logger.info('出现验证码')
              headers = {'Users-Agent': ua.random}
              img_data = requests.get(url=image[0], headers=headers).content
              code_path = os.path.join(local_image_tmp, 'code.png')
              with open(code_path, 'wb') as fp:
                fp.write(img_data)

              result = find_image(code_path)
              await page.hover('input#captchacharacters')
              await page.type('input#captchacharacters', result)
              await page.hover('button[type="submit"]')
              await page.click('button[type="submit"]')
              await asyncio.sleep(3)  # 等待验证码处理完成
            else:
              logger.info('没有出现验证码, 进入页面成功')
              break

        if fetch_image_success == False:
          # 获取网页信息
          xpath = '//*[@id="landingImage"]'
          await page.waitForXPath(xpath)
          htm = await page.content()
          html = etree.HTML(htm)
          image = html.xpath('//*[@id="landingImage"]/@src')

          if image:
              logger.info('获取图片')
              print('获取图片')
              # 获取图片二进制数据
              headers = {'Users-Agent': ua.random}
              img_data = requests.get(url=image[0], headers=headers).content
              with open(file_full_name, 'wb') as fp:
                fp.write(img_data)
              fetch_image_success = True
              print('获取图片成功')
          else:
              print('页面图片查找失败')
              logger.info('页面图片查找失败')
              with open('./example.html', 'wb') as fp:
                fp.write(etree.tostring(html, encoding='utf-8', pretty_print=True))

        if fetch_price is None and isPrice is True:
          print('======================fetch_price is None 获取商品价格')

          availability_xpath = '//*[@id="availability"]/span[2]/span'
          availability = await get_inner_text(page, availability_xpath)
          if availability is not None:
            print('======================availability is not None 获取商品价格')
            price = 'no_stock'
          else:
            # await page.waitForSelector('#corePriceDisplay_desktop_feature_div', { 'timeout': 30000 })
            # container_xpath = '//*[@id="corePriceDisplay_desktop_feature_div"]'
            # container_text = await get_inner_text(page, container_xpath)

            price_xpath = '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]/span[2]'
            price_xpath2 ='//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]'
            price_xpath3 = '//*[@id="corePrice_desktop"]/div/table/tbody/tr[1]/td[2]/span[1]/span[1]/span[2]'

            # //*[@id="availability"]/span[2]/span
            # //*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]/span[2]
            # //*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]/span[2]
            # //*[@id="corePrice_desktop"]/div/table/tbody/tr[1]/td[2]/span[1]/span[1]/span[2]
            # //*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]/span[2]
            # //*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]/span[2]
            availability_xpath = '//*[@id="availability"]/span[2]/span'

            price = await get_inner_text(page, price_xpath)
            print('======================xpath2, ', price)
            if price is None:
              print("使用价格xpath2")
              price = await get_inner_text(page, price_xpath2)

            if price is None  :
              print("使用价格xpath3")
              price = await get_inner_text(page, price_xpath3)

            if price:
              price = price.replace('€', '')
              price = price.replace('£', '')
              price = price.replace('$', '')
              price = price.replace('\n', '')
              price = price.replace(' ', '')
              price = price.replace(',', '')
        else:
          price = fetch_price

        print('======================PRICE, ', fetch_image_success, price)
        return fetch_image_success, price
    except Exception as e:
      logger.error(f"发生错误: {str(e)}")
      print('发生错误: =====')
      print(e)
      return None
    finally:
      await browser.close()


async def get_inner_text(page, xpath):
  try:
    htm = await page.content()
    html = etree.HTML(htm)
    elements = html.xpath(xpath)
    print(elements)

    if not elements:
      print('===============没有找到元素===============')
      return None

    # 获取元素的outerHTML
    element_html = etree.tostring(elements[0], encoding='unicode')

    inner_text = await page.evaluate("""(element_html) => {
        let div = document.createElement('div');
        div.innerHTML = element_html;
        return div.innerText;
    }""", element_html)

    return inner_text
  except Exception as e:
    print(e)
    return None

# 设置一个商品asin
#ASIN = 'https://www.amazon.co.uk/dp/B0BYRKFH4J?th=1'
#asyncio.get_event_loop().run_until_complete(main(ASIN))
def fetch_img(url, row_index, logger, image_in_cell, isPrice, isFetchImg):
    file_name = f"No{row_index}_row_image.png"
    file_full_name = os.path.join(local_image_tmp, file_name)
    if not os.path.exists(local_image_tmp):
        # 如果不存在，递归地创建文件夹
        os.makedirs(local_image_tmp)
        print(f"文件夹 {local_image_tmp} 创建成功")
    else:
        print(f"文件夹 {local_image_tmp} 已存在")

    result = None
    image_success = False

    url_status = check_url_is_valid(url, file_full_name, logger, image_in_cell, isFetchImg)
    if url_status == 2:
      image_success = True
      return file_full_name, None

    if url_status == 0:
      logger.info('当前商品地址不是amazon的商品页面')
      print('当前商品地址不是amazon的商品页面')
      return file_full_name, None

    logger.info(f"开始获取图片和价格{isPrice}{isFetchImg}")
    _loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_loop)
    res = _loop.run_until_complete(
      main(
        url = url,
        file_full_name = file_full_name,
        logger = logger,
        image_in_cell = image_in_cell,
        isPrice = isPrice,
        isFetchImg = isFetchImg
      )
    )

    if res is not None:
      image_success_status, price = res
      result = price
      image_success = image_success_status
      print(row_index, url, result, file_full_name)

    print("=========最终获取的价格和图片", image_success, result)
    cache_product_price[url] = result
    if image_success:
      cache_product_image[url] = file_full_name

    _loop.close()
    return file_full_name, result

async def destory_browser():
  global browser
  if browser:
      await browser.close()
      browser = None
  cache_product_price = {}

# 检查url是否有效, 如果是图片地址，返回False
def check_url_is_valid(url, file_full_name, logger, image_in_cell, isFetchImg):
  if url.endswith('.png') or url.endswith('.jpg') or url.endswith('.jpeg') or url.endswith('.gif') or url.endswith('.bmp') or url.endswith('.webp'):
    logger.info('当前商品地址是图片地址')
    if image_in_cell is not False or isFetchImg is True:
      # 获取图片二进制数据
      headers = {'Users-Agent': ua.random}
      img_data = requests.get(url=url, headers=headers).content
      with open(file_full_name, 'wb') as fp:
        fp.write(img_data)
    return 2

  # 检查url是否是amazon的商品页面
  if any(domain in url for domain in VALID_DOMAIN_NAMES):
    return 1
  return 0
