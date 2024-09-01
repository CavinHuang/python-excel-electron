import requests
from bs4 import BeautifulSoup
import re
from sse import logger
import json
import uuid

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

def get_product_detail(url):
    """Extracts product data from an Amazon product page URL.

    This function scrapes the product title, description, and image URLs from a given Amazon product page URL.

    Args:
        url (str): The URL of the Amazon product page.

    Returns:
        dict: A dictionary containing the extracted data, including:
            - title (str): The product title.
            - description (str): The product description.
            - image_urls (list): A list of image URLs for the product.

    Raises:
        Exception: An exception may be raised if there's an issue fetching or parsing the product details.
    """
    # if not is_valid_url(url):
    #     raise Exception("Invalid amazon product URL")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" +
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers, timeout=10000)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    soup = BeautifulSoup(response.content, "html.parser")

    asin_element = soup.find("input", id="ASIN")
    item_id = asin_element["value"] if asin_element else str(uuid.uuid4())

    title_element = soup.find("span", id="productTitle")
    title = title_element.text.strip() if title_element else None

    description_element = soup.find("div", id="feature-bullets")
    description = description_element.text.strip() if description_element else None

    image_block_element = soup.find("div", id="imageBlock_feature_div")

    image_urls = []
    if image_block_element:
        for script_element in image_block_element.find_all("script"):
            script_text = script_element.string if script_element else None
            if script_text and "ImageBlockATF" in script_text:
                image_url_pattern = r'"hiRes":"(.*?)",'
                image_urls.extend(re.findall(image_url_pattern, script_text))

    return {
        "id": item_id,
        "title": title,
        "description": description,
        "image_urls": image_urls,
    }

def is_valid_url(url):
    """Validates the provided URL.

    This function validates the URL and checks if the hostname is a valid domain name.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """

    try:
        parsed_url = parse_url(url)
        if not parsed_url.netloc or not parsed_url.scheme:
            return False  # Not a valid URL format
        domain = parsed_url.netloc.lower()
        print(domain)
        # Check if the domain ends with any of the valid domains
        return any(domain.endswith(tld.lower()) for tld in VALID_DOMAIN_NAMES)
    except Exception as e:
        logger.error(f"Error validating URL: {e}")
        return False