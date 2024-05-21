from django.test import TestCase
from .views import home_page
from django.http import HttpRequest
from .models import Item


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "first ever list item"
        first_item.save()

        second_item = Item()
        second_item.text = "item the second"
        second_item.save()

        saved_items = Item.objects.all()
        print(f"Total de itens salvos: {saved_items.count()}")
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "first ever list item")
        self.assertEqual(second_saved_item.text, "item the second")


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')

        html = response.content.decode('utf8')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
