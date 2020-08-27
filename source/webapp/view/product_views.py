from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from webapp.forms import ProductForm
from webapp.models import Product, CATEGORY_CHOICE


class IndexView(ListView):
    template_name = 'product/index.html'
    context_object_name = 'products'
    model = Product
    paginate_by = 5
    paginate_orphans = 0

    # def get_queryset(self):
    #     data = Project.objects.all()
    #     if not self.request.GET.get('is_admin', None):
    #         data = Project.objects.all()

        # http://localhost:8000/?search=ygjkjhg
        # form = SimpleSearchForm(data=self.request.GET)
        # if form.is_valid():
        #     search = form.cleaned_data['search']
        #     if search:
        #         data = data.filter(Q(title__icontains=search) | Q(author__icontains=search))

        # return data


# def index_view(request):
#     is_admin = request.GET.get('is_admin', None)
#     is_name = request.GET.get('name')
#     if is_admin:
#         order_date = Product.objects.all()
#     if is_name:
#         order_date = Product.objects.filter(name__icontains=is_name)\
#             .order_by('category', 'name')
#     else:
#         data = Product.objects.filter(amount__gt=0)
#         order_date = data.order_by('category', 'name')
#     return render(request, 'product/index.html', context={
#         'products': order_date,
#         'category': CATEGORY_CHOICE
#     })


def view_product(request, pk):
    data = get_object_or_404(Product, pk=pk)
    context = {'product': data}
    return render(request, 'product/product_view.html', context)


def product_create_view(request):
    if request.method == "GET":
        return render(request, 'product/product_create.html', context={
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
            return render(request, 'product/product_create.html', context={
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
        return render(request, 'product/product_update.html', context={
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
            return render(request, 'product/product_update.html', context={
                'product': product,
                'form': form
            })
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        return render(request, 'product/product_delete.html', context={'product': product})
    elif request.method == 'POST':
        product.delete()
        return redirect('index')


def filter_name_view(request, category):
    name = request.GET['name']
    data = Product.objects.filter(name__icontains=name, category=category).order_by('name')
    if data:
        return render(request, 'product/index.html', context={
            'products': data,
            'category': CATEGORY_CHOICE})
    return redirect('index')


def filter_category(request, category):
    data = Product.objects.filter(category=category)
    if data:
        order_date = data.order_by('name')
        for i in CATEGORY_CHOICE:
            if category in i:
                sel_cat = i
        return render(request, 'product/product_category_filter.html', context={
            'products': order_date,
            'category': CATEGORY_CHOICE,
            'sel_cat': sel_cat})
    return redirect('index')