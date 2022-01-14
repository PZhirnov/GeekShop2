from django.test import TestCase
from .models import Product, ProductCategory
from django.db.models import Sum
# Create your tests here.


class CatalogTest(TestCase):

    def setUp(self):
        self.test_name = 'Тест'
        self.new_catalog = ProductCategory.objects.create(name=self.test_name, description='Удобные стулья', is_active=True)

    # проверим факт создания категории товаров
    def test_create(self):
        self.assertTrue(self.new_catalog.is_active)

    def test_create_product(self):
        # создадим 100 продуктов в каталоге по 100 рублей и проверим логику расчета - т.е. 10000 продуктов должно быть
        # на 10 тыс. рублей.
        for i in range(100):
            Product.objects.create(category_id=self.new_catalog.id, name=f'Стул {i}', price=100)
        select_all = Product.objects.all()
        all_sum = select_all.aggregate(Sum('price'))
        print('Создано записей:', select_all.count(), " Итого:", all_sum['price__sum'])
        self.assertTrue(select_all.count() * 100 == all_sum['price__sum'])



