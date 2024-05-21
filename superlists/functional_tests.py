from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest
import time


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_if_can_start_a_list_and_retrieve_it_later(self):
        #Usuária Maria ouviu falar de app online para listar tarefas
        #Maria decidiu ir até homepage
        #Percebe que o título menciona "To-Do"
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        #Maria é convidada a inserir um item de uma tarefa
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item!'
        )

        inputbox.send_keys('Buy a new notebook')

        #Quando Maria clica enter, a página é atualizada, e agora pagina lista "1: buy a notebook"
        inputbox.send_keys(Keys.ENTER)
        time.sleep(5)

        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_element(By.TAG_NAME, 'tr')
        self.assertTrue(any(row.text == '1: Buy a new notebook' for row in rows),
                        f'New to-do item did  not appear in table. Contents were:\n{table.text}')

        #Continua sendo exibida um caixa de txt a convidando para inserir outro item "to_do"
        #Ela insere "Tidy up the house"
        self.fail("finish the test!")

        #A página é atualizada e agora existem dois itens na lista [...]