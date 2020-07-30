from django.shortcuts import render

from django.http import HttpResponseNotAllowed, QueryDict
from django.shortcuts import render, get_object_or_404, redirect

from webapp.forms import ProductForm
from webapp.models import Product


def index_view(request):
    is_admin = request.GET.get('is_admin', None)
    if is_admin:
        order_date = Product.objects.all()
    else:
        data = Product.objects.filter(amount__gt=1)
        order_date = data.order_by('category', 'name')
    return render(request, 'index.html', context={
        'products': order_date
    })


def view_product(request, pk):
    data = get_object_or_404(Product, pk=pk)
    context = {'product': data}
    return render(request, 'product_view.html', context)


def product_create_view(request):
    if request.method == "GET":
        return render(request, 'product_create.html', context={
            'form': ProductForm()
        })
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product = Product.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                category=form.cleaned_data['category'],
                amount=form.cleaned_data['amount'],
                price=form.cleaned_data['price']
            )
            return redirect('view', pk=product.pk)
        else:
            return render(request, 'product_create.html', context={
                'form': form
            })
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "GET":
        form = ProductForm(initial={
            'name': product.name,
            'description': product.description,
            'category': product.category,
            'amount': product.amount,
            'price': product.price})
        return render(request, 'product_update.html', context={
            'form': form,
            'product': product
        })
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.description = form.cleaned_data['description']
            product.category = form.cleaned_data['category']
            product.amount = form.cleaned_data['amount']
            product.price = form.cleaned_data['price']
            product.save()
            return redirect('view', pk=product.pk)
        else:
            return render(request, 'product_update.html', context={
                'product': product,
                'form': form
            })
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
