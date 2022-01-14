from django.test import TestCase
from .models import ShopUser
from django.utils.timezone import now
from datetime import timedelta


# Create your tests here.
class ModelTests(TestCase):

    # Пример с урока
    def test_user_is_created_with_age(self):
        user = ShopUser.objects.create(age=18)
        self.assertIsNotNone(user.age)

    # Проверка факта создания ключа активации и срока его использования
    def test_user_with_activation_key(self):
        user = ShopUser.objects.create(age=18)
        self.assertIsNotNone(user.activation_key)

    # Проверка срока действия ключа с момента создания
    def test_activation_key_expires(self):
        user = ShopUser.objects.create(age=18)
        # В данном случае решил сравнить значения до минут 2022-01-13 16:42 - или срез [:16]
        valid_val = str(now() + timedelta(hours=48))[:16]
        self.assertTrue(str(user.activation_key_expires)[:16] == valid_val)
