from django.urls import path

from crud_google_sheet.telegram_check import call_test
from crud_google_sheet.views import TestReadWriteSheet, get_sheet_by_google_and_save

urlpatterns = [
    path('', call_test.check_by_date),

]