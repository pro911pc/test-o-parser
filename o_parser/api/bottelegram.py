from telegram import Bot
from django.conf import settings


async def sendMassage(massage):
    bot = Bot(token='1208392564:AAF6ykrCjBlQxCHUKkQEa7Gi-WOxzY2pnuI')
    chat_id = '215048117'
    await bot.send_message(chat_id, massage)
