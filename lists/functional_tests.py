from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from lists.models import Item
import time

class NewVisitorTest(StaticLiveServerTestCase):
    reset_sequences = True  # ensures auto-reset of auto-increment IDs

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_todo_list(self):
        # Database is automatically flushed, should be empty
        self.assertEqual(Item.objects.count(), 0)

        self.browser.get(self.live_server_url)

        # User enters a new to-do item
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Check the item appears
        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertTrue(any("Buy peacock feathers" in row.text for row in rows))

        # Only one item in the DB
        self.assertEqual(Item.objects.count(), 1)

        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly"
        # (Edith is very methodical)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both items on her list
        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn(
            "2: Use peacock feathers to make a fly",
            [row.text for row in rows],
        )
        self.assertIn(
            "1: Buy peacock feathers",
            [row.text for row in rows],
        )

        # Satisfied, she goes back to sleep