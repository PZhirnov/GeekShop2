from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from basketapp.models import Basket
from mainapp.models import Product
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator


# метод по условию ДЗ -
# def basket_info(id):
#    bi = Basket.objects.filter(user_id=1)
#    print(bi)

# @login_required
# def basket(request):
#     title = 'корзина'
#     basket_items = Basket.objects.filter(user=request.user). \
#         order_by('product__category')
#
#     content = {
#         'title': title,
#         'basket_items': basket_items,
#     }
#     return render(request, 'basketapp/basket.html', content)

class BasketListView(ListView):
    model = Basket
    template_name = 'basketapp/basket.html'

    # @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user).order_by('product__category')


@login_required
def basket_add(request, pk):
    print(request.META.get('HTTP_REFERER'))
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))

    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)
    basket.quantity += 1
    basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user). \
            order_by('product__category')

        content = {
            'basket_items': basket_items,
        }
        result = render_to_string('basketapp/includes/inc_basket_list.html', \
                                  content)
        return JsonResponse({'result': result})



