from django.test import TestCase
from django.urls import resolve
from .views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string

# class SmokeTest(TestCase):
#
#     def test_bad_math(self):
#         self.assertEqual(1 + 1, 3)
#

class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')

        html = response.content.decode('utf8')
        self.assertTemplateUsed(response, 'home.html')

