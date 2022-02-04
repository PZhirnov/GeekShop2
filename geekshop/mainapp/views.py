import os.path
import random
import json
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ProductCategory, Product
from basketapp.models import Basket
from django.http import HttpResponse, JsonResponse
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator


# Create your views here.


''' Главное меню сайта, которое встраивается на каждой странице.
products -- написать так -- products:index сделать обязательно, учитывая то, что использщовался include в urls
'''
main_menu = [
    {'menu_section': 'index', 'main_urls': 'index', 'name': 'Главная'},
    {'menu_section': 'products:index',  'main_urls': 'products', 'name': 'Продукты'},
    {'menu_section': 'contact',  'main_urls': 'contact', 'name': 'Контакты'},
]


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user).select_related()
    else:
        return []

# Горячее предложение
def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]

# Похожие продукты
def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).select_related().exclude(pk=hot_product.pk)[:3]
    return same_products




''' Подгружаем данные о пользователе из json - это только для теста сделано'''
def user_info(user_login):
    with open("users_bd.json", "r", encoding="utf8") as read_file:
        data_user = json.load(read_file)
    return data_user.get(user_login)


user = user_info('user_login')

''' получаем текущую директорию '''
module_dir = os.path.dirname(__file__)


def index(request):
    products = Product.objects.all()[:4]
    content = {
        'title': 'Главная',
        'main_menu': main_menu,
        'user_info': user,
        'products': products
    }
    return render(request, 'mainapp/index.html', content)


# def products(request, pk=None):
#
#     title = 'продукты'
#     basket = []
#     if request.user.is_authenticated:
#         basket = Basket.objects.filter(user=request.user)
#
#     # Вариант вывода по запросу для категории
#     # 1. Получим все категории
#     links_menu = ProductCategory.objects.all()
#
#     if pk is not None:
#         if pk == 0:
#             products = Product.objects.all().order_by('price')
#             category = {'name': 'все'}
#         else:
#             category = get_object_or_404(ProductCategory, pk=pk)
#             products = Product.objects.filter(category__pk=pk).order_by('price')
#         print(basket[0].product)
#         content = {
#             'title': 'Продукты',
#             'links_menu': links_menu,
#             'main_menu': main_menu,
#             'user_info': user,
#             'products': products,
#             'category': category,
#             'basket': basket,
#         }
#         return render(request, 'mainapp/products_list.html', content)
#
#     # Горячее предложение
#     hot_product = get_hot_product()
#     same_products = get_same_products(hot_product)
#
#     content = {
#         'title': 'Продукты',
#         'links_menu': links_menu,
#         'main_menu': main_menu,
#         'hot_product': hot_product,
#         'same_products': same_products,
#     }
#     return render(request, 'mainapp/products.html', content)





def products(request, pk=None, page=1):
    title = 'продукты'
    links_menu = ProductCategory.objects.filter(is_active=True)
    basket = get_basket(request.user)
    # print(links_menu)
    # print(pk)
    if pk is not None:
        if pk == 0:
            category = {
                'pk': 0,
                'name': 'все'
            }
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
        paginator = Paginator(products, 3)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)
        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
            # 'basket': basket
        }
        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'main_menu': main_menu,
        'hot_product': hot_product,
        'same_products': same_products,
        }
    return render(request, 'mainapp/products.html', content)




def contact(request):
    content = {
        'title': 'Контакты',
        'main_menu': main_menu,
        'user_info': user,
    }
    return render(request, 'mainapp/contact.html', content)


''' Тестовая функция '''
def context(request):
    # данные, которые будут передаваться в шаблон
    content = {
        'title': 'магазин',
        'header': 'Добро пожаловать на сайт',
        'username': 'Иван Иванов',
        'products': [
            {'name': 'Стулья', 'price': 4535},
            {'name': 'Диваны', 'price': 1535},
            {'name': 'Кровати', 'price': 2535},
        ]
    }
    return render(request, 'mainapp/test_context.html', content)


# Страница продукта
def product(request, pk):
    title = 'продукты'

    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        # 'basket': get_basket(request.user),
    }

    return render(request, 'mainapp/product.html', content)


# контроллее, который возвращает стоимость выбранного продукта
# def product_price(request):
#     print('сработал')
#     id_product = request.GET.get("pk", "")
#     product = Product.objects.get(pk=id_product)
#     print(product.price)
#     return HttpResponse(product.price)


def product_price(request):
    # print('сработал')
    id_product = request.GET.get("pk", "")
    product = Product.objects.get(pk=id_product)
    if product:
        return JsonResponse({'price': product.price})
    else:
        return JsonResponse({'price': 0})
