from django.db import models


class Orders(models.Model):
    order = models.CharField(max_length=8, verbose_name='Заказ')
    price = models.IntegerField(default=0, verbose_name='Стоимость, $')
    delivery_time = models.DateField(verbose_name='Срок поставки')
    price_by_rubl = models.CharField(max_length=20, verbose_name='Стоимость в рубль', blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'