from django.test import TestCase
from lists.models import Item



class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")  

    def test_renders_input_form(self):
        response = self.client.get("/")
        self.assertContains(response, '<form method="POST">')
        self.assertContains(response, '<input name="item_text"')
        
    def test_can_save_a_POST_request(self):
        response = self.client.post("/", data={"item_text": "A new list item"}, follow=True)
        self.assertContains(response, "A new list item")

class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(second_saved_item.text, "Item the second")

class DataIsolationTest(TestCase):

    def test_data_not_persisted_between_tests(self):
        # At the start of this test, the database should be empty
        self.assertEqual(Item.objects.count(), 0)

        # Add an item
        Item.objects.create(text="Temporary item")
        self.assertEqual(Item.objects.count(), 1)

    def test_database_is_clean_in_a_new_test(self):
        # This test runs after the previous one
        # The database should be empty again
        self.assertEqual(Item.objects.count(), 0)