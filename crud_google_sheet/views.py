import json
import logging
import requests
import xmltodict
import gspread as gs
import pandas as pd
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from dotenv import load_dotenv

from crud_google_sheet.models import Orders
from crud_google_sheet.serializers import OrdersSerializer

load_dotenv()


def get_daily(date) -> str:
    date = date.replace('.', '/')
    url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}'
    response = requests.get(url)
    if response.status_code == 200:
        currency = json.loads(json.dumps(xmltodict.parse(response.text)))
        for item in currency['ValCurs']['Valute']:
            if item['CharCode'] == 'USD':
                return item['Value']
    else:
        logging.warning(response.text)
        raise Exception(f'Error from request {response.text}')


def save_data(df):
    '''
        in this function save data to database
    '''
    items = list()
    for item in df.values:
        items.append(
            Orders(order=item[0], price=item[1], delivery_time=item[2], price_by_rubl=item[4])
        )
    try:
        Orders.objects.bulk_create(items)
    except Exception as ex:
        logging.warning(ex)


def get_sheet_by_google_and_save():
    '''
        In this function get google sheet and add to pandas than by convert dollar to ruble by course.
        In the end call function to save data to db
    '''
    Orders.objects.all().delete()  # delete all data on the db
    gc = gs.service_account()  # get access to google drive and google sheet
    sh = gc.open_by_key('1f-qZEX1k_3nj5cahOzntYAnvO4ignbyesVO7yuBdv_g')  # get google sheet by id
    worksheet = sh.worksheet("Лист1")  # read google sheet by page "Лист1"
    df = pd.DataFrame(worksheet.get_all_records())  # worksheet add to pandas dataframe
    df = df.drop(['№'], axis=1)  # delete index sheet
    df['course_to_date'] = df['срок поставки'].apply(get_daily)  # get course in the bank history and add to new column
    df['срок поставки'] = pd.to_datetime(df['срок поставки'], infer_datetime_format=True)  # correct date format to save
    df['price_by_rubl'] = df['стоимость,$'].astype(float) * df['course_to_date'].str.replace(',', '.').astype(float)  # convert dollar to ruble by course
    save_data(df)  # call function to save


class TestReadWriteSheet(APIView):

    # List all
    def get(self, request, *args, **kwargs):
        '''
        List all the order
        '''
        order = Orders.objects.all()
        serializer = OrdersSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # # Get by id
    # def get_object(self, pk):
    #     try:
    #         return Orders.objects.get(pk=pk)
    #     except Orders.DoesNotExist:
    #         raise Http404
    #
    # # Create
    # def post(self, request, *args, **kwargs):
    #         '''
    #         Create the Order
    #         '''
    #         data = {
    #             'order': request.data.get('order'),
    #             'price': request.data.get('price'),
    #             'delivery_time': request.data.get('delivery_time'),
    #             'course_to_date': request.data.get('course_to_date'),
    #             'price_by_rubl': request.data.get('price_by_rubl'),
    #         }
    #         serializer = OrdersSerializer(data=data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # # Update data by id
    # def put(self, request, pk, format=None):
    #     order = self.get_object(pk)
    #     serializer = OrdersSerializer(order, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # # Delete data by id
    # def delete(self, request, pk, format=None):
    #     order = self.get_object(pk)
    #     order.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)