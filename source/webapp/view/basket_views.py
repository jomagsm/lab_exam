from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View, ListView, DeleteView
from django.urls import reverse, reverse_lazy

from webapp.forms import ProductForm, BasketForm
from webapp.models import Basket, Product


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
                return redirect('view', pk=product.pk)
        else:
            if product.amount > qty:
                basket = Basket.objects.create(product=product, qty=qty)
                basket.save()
            else:
                return redirect('view', pk=product.pk)
        # # form.save_m2m()  ## для сохранения связей многие-ко-многим
        return redirect('view', pk=product.pk)


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
        context['form'] = BasketForm
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