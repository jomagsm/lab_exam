from django.contrib import admin
from webapp.models import Product, Basket, OrderProduct, Order


class ProductAdmin(admin.ModelAdmin):
    list_filter = ('category',)
    list_display = ('pk', 'name', 'amount', 'price')
    list_display_links = ('pk', 'name')
    search_fields = ('name',)


class OrderAdmin(admin.ModelAdmin):

    list_display = ['pk', 'name', 'phone', 'data']
    list_filter = ['data']


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'qty']


admin.site.register(Product, ProductAdmin)
admin.site.register(Basket)
admin.site.register(OrderProduct,OrderProductAdmin)
admin.site.register(Order,OrderAdmin)

# В списке заказов в админке выведите pk, имя, телефон и дату и время создания.
# В списке заказов в админке отсортируйте их по дате и времени создания в убывающем порядке

