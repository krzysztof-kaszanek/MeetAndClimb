from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User

from WebApp.models import Wyjazd, Wspinacz, Wiadomosc, UczestnikWyjazdu


class AccountTestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox(executable_path=r'C:/geckodriver/geckodriver.exe')
        super(AccountTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(AccountTestCase, self).tearDown()

    def test_register(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/accounts/login/')
        username = selenium.find_element_by_name('username')
        password = selenium.find_element_by_name('password')
        submit = selenium.find_element_by_id('login')
        username.send_keys('Herbert123')
        password.send_keys('klausZukowski')
        submit.click()

        # Początek przypadku testowego 1.1
        selenium.find_element_by_link_text('Wyjazdy').click()
        selenium.find_element_by_link_text('Szczegóły').click()
        selenium.find_element_by_link_text('Zgłoś chęć udziału').click()
        assert 'Zgłoszenie wysłane pomyślnie!' in selenium.page_source

    def test_odebranie_wiadomosci(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/accounts/login/')
        username = selenium.find_element_by_name('username')
        password = selenium.find_element_by_name('password')
        submit = selenium.find_element_by_id('login')
        username.send_keys('Herbert123')
        password.send_keys('klausZukowski')
        submit.click()

        # Początek przypadku testowego 1.2
        selenium.find_elements_by_class_name('nav-link')[3].click()
        selenium.find_element_by_link_text('Zgłoszenie zaakceptowane').click()
        assert 'Twoje zgłoszenie na wyjazd Kurs skałkowy zostało zaakceptowane przez organizatora!' in selenium.page_source
