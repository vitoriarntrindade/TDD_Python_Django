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

    def test_multiple_user_can_start_lists_at_different_urls(self):
        #Maria ouviu falar de um app interesasnte para listar coisas
        self.browser.get(self.live_server_url)

        #Maria é convidada a adicionar um item na lista de "to-do"
        inputbox = self.browser.find_element(By.ID, 'id_new_item')

        #Maria então lembra que precisa comprar um notebook
        inputbox.send_keys('buy a new notebook')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)

        #Maria percebeu que o item foi adicionado a lista
        self.wait_for_row_in_list_table('1: buy a new notebook')

        # maria recebe um url único
        maria_list_url = self.browser.current_url

        # verifica se a string corresponde com a regex
        print("assertregex")
        self.assertRegex(maria_list_url, '/lists/.+')
        #Maria sai do site

        #Agora tem Joao, um novo usuário
        #Usamos um outra sessão para Joao não ver os dados de Maria
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #Joao acessa e não vê nenhum sinal da lista de Maria
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        print("assert notin ")
        self.assertNotIn('1: buy a new notebook', page_text)

        #Joao inicia uma nova lista, inserindo um novo item

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Aula de artes marciais')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(0.5)

        #Joao percebeu que o item foi adicionado a lista
        self.wait_for_row_in_list_table('1: Aula de artes marciais')
        time.sleep(5)
        #Joao obtem seu proprio url

        joao_list_url = self.browser.current_url
        self.assertRegex(joao_list_url, '/lists/.+')
        self.assertNotEquals(joao_list_url, maria_list_url)

        #Não há nenhum registro da lista de maria exposto ao joao
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('1: buy a new notebook', page_text)
        self.assertIn("1: Aula de artes marciais", page_text)