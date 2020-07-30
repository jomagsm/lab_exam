from django.db import models

DEFAUL_CATEGORY = 'other'
CATEGORY_CHOICE = [(DEFAUL_CATEGORY, 'Разное'), ('food', 'Продукты питания'),
                   ('household', 'Хоз.товары'), ('toys', 'Детские игрушки'),
                   ('electronics', 'Электроника')]


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание')
    category = models.CharField(max_length=20, verbose_name='Категория', choices=CATEGORY_CHOICE,
                                default=DEFAUL_CATEGORY)
    amount = models.IntegerField(verbose_name='Остаток')
    price = models.DecimalField(verbose_name='Цена', max_digits=7, decimal_places=2)

    def __str__(self):
        return "{}. {}".format(self.name, self.amount)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'