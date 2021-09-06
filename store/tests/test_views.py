from importlib import import_module

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from store.models import Category, Product
from store.views import product_all


class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        Category.objects.create(name='Mobile', slug='mobile')
        User.objects.create(username='admin')
        Product.objects.create(category_id=1, title='Apple Phone', created_by_id=1, slug='apple-phone', price='20.00', image='image')

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get('/', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 400)
        response = self.c.get('/', HTTP_HOST='yourdomain.com')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """
        Test Product Response Status
        """
        response = self.c.get(reverse('store:product_detail', args=['apple-phone']))
        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):
        """
        Test Category Response Status
        """
        response = self.c.get(reverse('store:category_list', args=['mobile']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        """"
        Example: Code Validation , search HTML for text
        """
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Home</title>', html)
        # self.assertTrue(html.startswith('\n<!Doctype html>\n'))
        self.assertEqual(response.status_code, 200)


