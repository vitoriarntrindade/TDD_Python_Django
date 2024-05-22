from django.test import TestCase
from .views import home_page
from django.http import HttpRequest
from .models import Item, List


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "first item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "item the second"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        saved_items = Item.objects.all()
        print(f"Total de itens salvos: {saved_items.count()}")
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(saved_list, list_)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "first item")
        self.assertEqual(second_saved_item.text, "item the second")


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')

        html = response.content.decode('utf8')
        self.assertTemplateUsed(response, 'home.html')

    def test_only_save_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirect_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lists/the-list')

