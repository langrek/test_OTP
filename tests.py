from pages.main_page import MainPage


def test_case_01(driver):
    """
    1) Перейти на страницу https://www.mos.ru/
    2) Проверить наличие шапки подвала.
    3) Вытащить все ссылки со страницы и проверить их на 200
    4) Открыть каждую ссылку и проверить адресную строку браузера, что открывается нужная ссылка
    """
    # Тестовые данные
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
    main_page = MainPage(driver)
    main_page.open()
    main_page.check_presence_of_header()
    main_page.check_presence_of_footer()
    # Парсим не только на главной странице, но и по всем ссылкам меню разделов
    list_of_all_urls = main_page.get_urls_from_pages(urls=site_urls)
    main_page.check_pages_response_200(urls=list_of_all_urls)
    main_page.check_correct_url_opened(urls=list_of_all_urls)

