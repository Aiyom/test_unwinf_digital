import asyncio

from crud_google_sheet.telegram_check import call_test
from crud_google_sheet.views import get_sheet_by_google_and_save
from test_unwind_digital.celery import app


@app.task
def get_ordersWild():
    get_sheet_by_google_and_save()


@app.task
def call_check():
    asyncio.run(call_test.check_by_date())