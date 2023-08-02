from bs4 import BeautifulSoup
import requests
import logging
import undetected_chromedriver as uc
import time
from products.models import Product


logger = logging.getLogger(__name__)


def get_content_product(products_count):
    url_base = 'https://www.ozon.ru'
    url = url_base + '/seller/1/products/'
    driver = uc.Chrome()
    driver.get(url)
    logger.error(driver.current_url)
    places = []
    soup = BeautifulSoup(driver.page_source, "html.parser")
    places = soup.findAll('div', class_='i1m')
    for place in places:
        products = place.findAll('div', class_='i9j ik')
        for product in products:
            name = product.find('span', class_='tsBody500Medium').text
            url = url_base+product.find('a', class_='tile-hover-target yh3 h4y')['href']
            Product.objects.create(
                                   name=name,
                                   url=url)
            logger.error(url)
    driver.close()
    driver.quit()
