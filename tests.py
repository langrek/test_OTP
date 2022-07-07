import allure
import requests
from allure_commons.types import AttachmentType
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# Начальный список ссылок
site_urls = ['https://www.mos.ru/',
             'https://www.mos.ru/news/',
             'https://www.mos.ru/afisha/',
             'https://www.mos.ru/uslugi/',
             'https://www.mos.ru/mayor/themes/',
             'https://www.mos.ru/authority/',
             'https://www.mos.ru/map/',
             'https://www.mos.ru/moi-raion/',
             'https://www.mos.ru/otvet/',
             'https://www.mos.ru/feedback/'
             ]

# Селекторы хедера и футера
header = 'mos-header'
footer = 'mos_footer'

# Инициализация драйвера
driver = webdriver.Chrome('./chromedriver')


# Парсинг главной страницы и хеддера
def get_urls_from_pages(urls):
    # Создаем пустой список
    list_of_all_urls = []
    for url in urls:
        # Форумируем реквест
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        for link in soup.find_all('a'):
            if 'https://' in str(link.get('href')):
                list_of_all_urls.append(link.get('href'))
    list_of_all_urls += urls
    # Возвращаем список уникальных значений
    return set(list_of_all_urls)


# Проверка наличия хедера на странице
def test_check_presence_of_header():
    # Открываем страницу
    driver.get('https://www.mos.ru/')
    # Проверяем, что было найдено больше, чем 0 элементов
    assert len(driver.find_elements(By.ID, header)) > 0


# Проверка наличия футтера на странице
def test_check_presence_of_footer():
    # Открываем страницу
    driver.get('https://www.mos.ru/')
    # Проверяем, что было найдено больше, чем 0 элементов
    assert len(driver.find_elements(By.ID, footer)) > 0


# Тест на проверку того, что ссылка возвращает 200 код
def test_pages_response():
    urls = get_urls_from_pages(site_urls)
    for url in urls:
        # Формируем реквест
        r = requests.get(url)
        try:
            # Проверяем условие
            assert 200 == r.status_code
        except AssertionError:
            # В случае ошибки выводим в консоль url с кодом
            print(f'{url} вернул код: {r.status_code}')


# Тест на проверку того, что по ссылке открывается нужная страница
def test_correct_url_opened():
    # Получаем список всех ссылок
    urls = get_urls_from_pages(site_urls)
    # Проходимся циклом по списку
    for url in urls:
        # Открываем ссылку
        driver.get(url)
        try:
            # Проверяем что по ссылке, открывается нужная страница в браузере
            assert url == driver.current_url
        # В случае ошибки ассерта - делаем скриншот и выводим сообщение об ошибке в консоль
        except AssertionError:
            allure.attach(driver.get_screenshot_as_png(), name=f"Screenshot_{url}", attachment_type=AttachmentType.PNG)
            print(f'По ссылке {url} открывается {driver.current_url}')
