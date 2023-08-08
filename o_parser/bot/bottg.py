from telebot import TeleBot
from django.conf import settings

bot = TeleBot(settings.TELEGRAM_TOKEN, threaded=False)


def send_message(message):
    if message:
        bot.send_message(settings.TELEGRAM_CHAT_ID, message)
