from selenium import webdriver
import unittest


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
        self.fail('Finish the test!')

