from django.core.validators import MinValueValidator
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
    amount = models.IntegerField(verbose_name='Остаток', validators=[MinValueValidator(0)])
    price = models.DecimalField(verbose_name='Цена', max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return "{}. {}".format(self.name, self.amount)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Basket(models.Model):
    product = models.ForeignKey('webapp.Product', related_name='basket', verbose_name='Продукт',on_delete=models.CASCADE)
    qty = models.IntegerField(verbose_name='Количество', validators=[MinValueValidator(0)])

    def get_total(self):
        return self.qty * self.product.price


class Tag(models.Model):
    name = models.CharField(max_length=31, verbose_name='Тег')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField(max_length=100, null=False,blank=False, verbose_name='Имя')
    address = models.CharField(max_length=1000, null=False, blank=False, verbose_name='Адрес')
    phone = models.CharField(max_length=100, null=False, blank=False, verbose_name='Телефон')
    data = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')


class OrderProduct(models.Model):
    product = models.ForeignKey('webapp.Product', related_name='product_orders', on_delete=models.CASCADE, verbose_name='Продукт')
    order = models.ForeignKey('webapp.Order', related_name='order_products', on_delete=models.CASCADE, verbose_name='Заказ')
    qty = models.IntegerField(verbose_name='Количество', validators=[MinValueValidator(0)])

    def __str__(self):
        return "{} | {}".format(self.order, self.product)
