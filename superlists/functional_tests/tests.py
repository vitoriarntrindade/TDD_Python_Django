from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
from django.test import LiveServerTestCase

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        #auxilia a testar se
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_if_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('buy a new notebook')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(0.5)

        self.wait_for_row_in_list_table('1: buy a new notebook')

        #o usuário recebe um url único

        client_list_url = self.browser.current_url
        self.assertRegex(client_list_url, '/lists/.+') #verifica se a string corresponde com a regex
        self.browser.quit()

        #simulando outro usuário acessando e sem poder ver os dados inseridos de outro usuário
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('1: buy a new notebook', page_text)
