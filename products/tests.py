from django.test import TestCase
from django.http import HttpRequest
from django.urls import reverse

from products import views

class ProductPageTests(SimpleTestCase):
    def test_product_list_page(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_product_add_page(self):
        response = self.client.get('/products/add')
        self.assertEquals(response.status_code, 200)
