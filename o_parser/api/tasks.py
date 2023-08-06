from bs4 import BeautifulSoup
import requests
import logging
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import time
from products.models import Product
from celery import shared_task
import re

logger = logging.getLogger(__name__)

URL_BASE = 'https://www.ozon.ru'
URL = URL_BASE + '/seller/1/products/'


class Content:

    def __init__(self, current_url):
        self.current_url = current_url 
        self.page = 0


def get_content_website(content):
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument('--headless')
    driver = uc.Chrome(options=options)
    url = content.current_url
    if content.page > 1:
        url += '&page=' + str(content.page)
    driver.get(url)
    if content.page == 1:
        content.current_url = driver.current_url
    page_source = driver.page_source
    driver.close()
    driver.quit()
    return BeautifulSoup(page_source, "html.parser")


def get_int_value(value):
    numbers = re.findall('[0-9]+', value)
    return ''.join(numbers)


def get_description(url_product):
    content = Content(url_product)
    soup = get_content_website(content)
    description_class = 'ra-a1'
    discount = soup.find('div', class_=description_class).text
    return discount


#@shared_task()
def get_content_product(products_count=10):
    content = Content(URL)
    logger.error('test')
    places = []
    i = 0
    while int(products_count or 10) > i:
        content.page += 1
        soup = get_content_website(content)
        places = soup.findAll('div', class_='i1m')
        for place in places:
            products = place.findAll('div', class_='i9j ik')
            for product in products:
                name = product.find('span', class_='tsBody500Medium').text
                price_class = 'c3-a1 tsHeadline500Medium c3-b9'
                price_str = product.find('span',
                                         class_=price_class).text
                price = get_int_value(price_str)
                url_product_class = 'tile-hover-target yh3 h4y'
                url_product = product.find('a',
                                           class_=url_product_class)['href']
                description = get_description(URL_BASE+url_product)
                image_url = product.find('img', class_='c9-a')['src']
                discount_class = 'tsBodyControl400Small c3-a2 c3-a7 c3-b1'
                discount_span = product.find('span',
                                             class_=discount_class)
                discount = None
                if discount_span:
                    discount = discount_span.text

                Product.objects.create(
                                        name=name,
                                        price=price,
                                        description=description,
                                        image_url=image_url,
                                        discount=discount)
                i += 1
                if int(products_count or 10)-1 < i:
                    break
    logger.error(i)
    return i
