from django.shortcuts import render

from django.http import HttpResponseNotAllowed, QueryDict
from django.shortcuts import render, get_object_or_404, redirect

from webapp.forms import ProductForm
from webapp.models import Product


def index_view(request):
    is_admin = request.GET.get('is_admin', None)
    if is_admin:
        data = Product.objects.all()
    else:
        data = Product.objects.filter(amount__gt=1)
        data.order_by('category', 'name')
    return render(request, 'index.html', context={
        'products': data
    })


def view_product(request, pk):
    data = get_object_or_404(Product, pk=pk)
    context = {'product': data}
    return render(request, 'product_view.html', context)
