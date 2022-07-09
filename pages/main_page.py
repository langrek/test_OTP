import allure
import requests
from allure_commons.types import AttachmentType
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class MainPageLocators:
    header = (By.ID, 'mos-header')
    footer = (By.ID, 'mos_footer')


class MainPage(BasePage):
    url = 'https://www.mos.ru/'
    loc = MainPageLocators

    def open(self):
        self.driver.get(self.url)

    def get_urls_from_pages(self, urls):
        list_of_all_urls = []
        for url in urls:
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            for link in soup.find_all('a'):
                if 'https://' in str(link.get('href')):
                    list_of_all_urls.append(link.get('href'))
        list_of_all_urls += urls
        return set(list_of_all_urls)

    def check_presence_of_header(self):
        with allure.step('Проверяем наличие хедера'):
            header = self.driver.find_element(*self.loc.header)
            assert header.is_displayed(), 'Хедер не отображается на странице'

    def check_presence_of_footer(self):
        with allure.step('Проверяем наличие футера'):
            header = self.driver.find_element(*self.loc.footer)
            assert header.is_displayed(), 'Футер не отображается на странице'

    def check_pages_response_200(self, urls):
        with allure.step('Отправляем запрос и проверяем на статус 200'):
            for url in urls:
                r = requests.get(url)
                try:
                    assert 200 == r.status_code, f'\n {url} вернул код: {r.status_code}'
                except AssertionError:
                    print(f'\n {url} вернул код: {r.status_code}')

    def check_correct_url_opened(self, urls):
        with allure.step('Проверяем что по ссылке открывается нужна страница'):
            for url in urls:
                self.driver.get(url)
                try:
                    assert url in self.driver.current_url
                except AssertionError:
                    allure.attach(self.driver.get_screenshot_as_png(), name=f'Screenshot_{url}',
                                  attachment_type=AttachmentType.PNG)
                    print(f'\n По ссылке {url} открывается {self.driver.current_url}')
