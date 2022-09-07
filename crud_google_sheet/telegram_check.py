import datetime
import os

from aiogram import Bot
from asgiref.sync import sync_to_async
from dotenv import load_dotenv

from crud_google_sheet.models import Orders

load_dotenv()


class CheckAndSendByTelegram:

    async def check_by_date(self, *args, **kwargs):
        bot = Bot(token=os.getenv('BOT_TOKEN'))
        now = datetime.datetime.now()
        currency_date_now = now.strftime("%Y-%m-%d")
        orders = await sync_to_async(Orders.objects.filter)(delivery_time=currency_date_now)
        async for item in orders:
            text = f'Срок прошел\n' \
                   f'Номер заказа: {item.order}\n' \
                   f'Срок заказа: {item.delivery_time}\n' \
                   f'Сотимость в доллар: {item.price}\n' \
                   f'Стоимость в рубль: {item.price_by_rubl}'
            await bot.send_message(os.getenv('USER_TELEGRAM_ID'), text)


call_test = CheckAndSendByTelegram()
