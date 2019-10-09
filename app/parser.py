import logging
import platform
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from bs4 import BeautifulSoup

from app.client import Client


class Parser:
    def __init__(self):
        self.__url = "https://www.olx.ua/list/"
        self.__init_browser()

    def __del__(self):
        self.__driver.close()
        logging.info("Browser kill.")

    def __init_browser(self):
        logging.info("Browser starting...")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-setuid-sandbox")

        if platform.system() == 'Linux':
            self.__driver = webdriver.Chrome(executable_path="./app/files/chromedriver",
                                             chrome_options=chrome_options)
        else:
            self.__driver = webdriver.Chrome(executable_path="./app/files/chromedriver.exe",
                                             chrome_options=chrome_options)

        logging.info("Browser start!")

    def __get_products(self) -> list:
        soup = BeautifulSoup(self.__driver.page_source, 'html.parser')

        all_offers = []
        top_offers = soup.find('table', class_='offers--top').find_all('tr', class_='wrap')
        offers = soup.find('table', id='offers_table').find_all('tr', class_='wrap')

        all_offers += top_offers
        all_offers += offers

        return all_offers

    @staticmethod
    def __get_urls(offers: list) -> list:
        urls = []
        for offer in offers:
            url = offer.find('a', class_='detailsLink')['href']
            urls.append(url)
        return urls

    @staticmethod
    def __filter_url(urls: list) -> list:
        filter_urls = []

        with open('./app/files/blacklist', 'rt') as f:
            black_urls = f.read().split('\n')

        with open('./app/files/blacklist', 'at') as f:
            for url in urls:
                if url not in black_urls:
                    filter_urls.append(url)
                    f.write(f"{url}\n")
        return filter_urls

    @staticmethod
    def __get_phone_html(html: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        phone = soup.find('ul', id='contact_methods').find('strong', class_='xx-large').text

        return phone

    def get_phone(self, urls: list) -> list:
        page_data_set = []

        for url in urls:
            data = dict()
            self.__driver.get(url)
            try:
                self.__driver.find_element_by_class_name('cookie-close').click()
            except (ElementNotInteractableException, NoSuchElementException):
                pass

            try:
                self.__driver.find_element_by_id('contact_methods').find_element_by_class_name('link-phone').click()
            except (ElementNotInteractableException, NoSuchElementException):
                logging.warning(f"Page don't have phone number.\nURL:{url}")
                continue

            sleep(3)

            data['url'] = url
            data['phone'] = self.__get_phone_html(self.__driver.page_source)

            logging.info('Data parsed:' + str(data))
            page_data_set.append(data)

        return page_data_set

    def parse(self):
        logging.info("Starting parse process.")
        self.__driver.get(self.__url)
        offers = self.__get_products()
        urls = self.__get_urls(offers)
        filter_urls = self.__filter_url(urls)

        data_list = self.get_phone(filter_urls)
        for data in data_list:
            Client.send(data)
