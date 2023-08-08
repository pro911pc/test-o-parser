from django.core.management.base import BaseCommand
from bot.bottg import bot
from products.models import ProductPost, Product


class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.infinity_polling()

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, "Привет ✌️ ")

    @bot.message_handler(commands=['productlist'])
    def product_list(message):
        productPost = ProductPost.objects.order_by('-created').first()
        id_request = productPost.id_request
        products = Product.objects.filter(id_request=id_request)
        text = ''
        i = 0
        for product in products:
            i += 1
            text += str(i)+')'+' Название:'+product.name\
                + 'ссылка:'+product.image_url + '\n'
        if text == '':
            bot.send_message(message.chat.id, 'Нет данных id_request:' \
                             + id_request)
        else:
            bot.send_message(message.chat.id, text)
