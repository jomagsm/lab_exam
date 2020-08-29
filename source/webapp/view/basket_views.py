from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View, ListView, DeleteView, CreateView
from django.urls import reverse, reverse_lazy

from webapp.forms import ProductForm, BasketForm, OrderForm
from webapp.models import Basket, Product, Order, OrderProduct


class BasketCreateView(View):

    def post(self, request, *args, **kwargs):
        form = BasketForm(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        qty = form.cleaned_data['qty']
        check_basket = Basket.objects.all()
        check_basket = check_basket.filter(product=product)
        if check_basket:
            basket = check_basket[0]
            basket.qty = basket.qty + qty
            if product.amount > basket.qty:
                basket.save()
            else:
                return redirect('index')
        else:
            if product.amount >= qty:
                basket = Basket.objects.create(product=product, qty=qty)
                basket.save()
            else:
                return redirect('index')
        # # form.save_m2m()  ## для сохранения связей многие-ко-многим
        return redirect('index')


class BasketList(ListView):
    template_name = 'basket/basket_list.html'
    context_object_name = 'products'
    model = Basket
    paginate_by = 5
    paginate_orphans = 0

    def get_queryset(self):
        data = Basket.objects.all()
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm
        data = Basket.objects.all()
        total = 0
        for i in data:
            total += i.qty * i.product.price
        context['total'] = total
        return context


class BasketDeleteView(DeleteView):
    template_name = 'basket/basket_list.html'
    model = Basket
    success_url = reverse_lazy('basket_list')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class BasketOneDeleteView(DeleteView):
    template_name = 'basket/basket_list.html'
    model = Basket
    success_url = reverse_lazy('basket_list')

    def get(self,request, *args, **kwargs):
        pk = self.kwargs['pk']
        basket = get_object_or_404(Basket, pk=pk)
        if basket.qty > 1:
            basket.qty = basket.qty-1
            basket.save()
        else:
            return self.delete(request, *args, **kwargs)
        return redirect('basket_list')

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm

    def form_valid(self, form):
        name = form.cleaned_data['name']
        address = form.cleaned_data['address']
        phone = form.cleaned_data['phone']
        order = Order.objects.create(name=name, address=address, phone=phone)
        basket = Basket.objects.all()
        for i in basket:
            product =Product.objects.get(pk=i.product.pk)
            OrderProduct.objects.create(product=i.product,
                                        order=order,
                                        qty=i.qty)
            product.amount = product.amount-i.qty
            product.save()
        basket.delete()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')