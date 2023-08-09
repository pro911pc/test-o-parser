import logging
import re
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

from bot.bottg import send_message
from products.models import Product

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
    if value:
        numbers = re.findall('[0-9]+', value)
        return ''.join(numbers)
    return None


def get_value(name, content, teg, listclass):
    for class_ in listclass:
        places = content.find(teg, class_=class_)
        if places:
            return places
    send_message('не удалось найти ' + name + ' в документе html')
    return None


def get_all_value(name, content, teg, listclass):
    for class_ in listclass:
        places = content.findAll(teg, class_=class_)
        if len(places) != 0:
            return places
    send_message('не удалось найти ' + name + ' в документе html')
    return []


def getplaces(content):
    class_places = ['i1m', 'iq5']
    return get_all_value('places', content, 'div', class_places)


def getproducts(content):
    class_product = ['i9j ik', 'oi2 i3o']
    return get_all_value('product', content, 'div', class_product)


def get_name(content):
    class_name = ['tsBody500Medium']
    name_span = get_value('name', content, 'span', class_name)
    if name_span:
        return name_span.text
    return ''


def grt_price(content):
    price_class = ['c3-a1 tsHeadline500Medium c3-b9']
    price_span = get_value('price', content, 'span', price_class)
    if price_span:
        price_str = price_span.text
        price = get_int_value(price_str)
        if price:
            return price
    return 0


def get_url_product(content):
    url_product_class = ['tile-hover-target yh3 h4y',
                         'il9 tile-hover-target']
    url_product_a = get_value('url_product', content, 'a', url_product_class)
    if url_product_a:
        return url_product_a['href']
    return ''


def get_image_url(content):
    image_url_class = ['c9-a']
    image_url_img = get_value('image_url', content, 'img', image_url_class)
    if image_url_img:
        return image_url_img['src']
    return ''


def get_description(url_product):
    content = Content(url_product)
    soup = get_content_website(content)
    description_class = ['ra-a1']
    description_plase = get_value('description', soup, 'div',
                                  description_class)
    if description_plase:
        return description_plase.text
    send_message(url_product)
    return ''


def get_discount(content):
    discount_class = ['tsBodyControl400Small c3-a2 c3-a7 c3-b1']
    discount_span = get_value('discount', content, 'span', discount_class)
    if discount_span:
        return discount_span.text
    return None


#@shared_task
def get_content_product(products_count=10, id_request=''):
    send_message('start')
    try:
        content = Content(URL)
        places = []
        i = 0
        while int(products_count or 10) > i:
            content.page += 1
            soup = get_content_website(content)
            places = getplaces(soup)
            if len(places) == 0:
                break
            for place in places:
                products = getproducts(place)
                if len(products) == 0:
                    break
                for product in products:
                    url_description = URL_BASE+get_url_product(product)
                    description = get_description(url_description)
                    Product.objects.create(
                                        name=get_name(product),
                                        price=grt_price(product),
                                        description=description,
                                        image_url=get_image_url(product),
                                        discount=get_discount(product),
                                        id_request=id_request)
                    i += 1
                    if int(products_count or 10)-1 < i:
                        break
        logger.error(i)
        message = 'Задача на парсинг товаров с сайта Ozon завершена.\
                Сохранено: '+str(i) + ' товаров.'
        send_message(message)
    except Exception as err:
        send_message(err)
