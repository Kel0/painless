import logging
import time
from typing import Optional, Type

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from settings import KASPI_PASSWORD, KASPI_USERNAME
from src.models.kaspi import KaspiLinks
from src.services.kaspi.authentication import get_confirmation_code
from src.services.kaspi.parsers import get_card_transactions_from_html

logger = logging.getLogger(__name__)


class KaspiAuth:
    def __init__(self, links: Optional[Type[KaspiLinks]] = None):
        self.links = links
        if self.links is None:
            self.links = KaspiLinks

    def _get_login_page(self, driver, delay):
        try:
            logging.info("Redirecting to login page")
            driver.get(self.links.login)
            WebDriverWait(driver, delay).until(
                ec.presence_of_element_located((By.ID, "txtLogin"))
            )
        except TimeoutException:
            driver.execute_script("window.stop();")
            logging.info(
                "Page loading stopped directly, " "cause of load time is out-of-date"
            )

        return driver

    def _fill_credentials(self, driver):
        logger.info("Filling up credentials inputs")
        login_input = driver.find_element_by_id("txtLogin")
        password_input = driver.find_element_by_id("txtPassword")
        login_input.send_keys(KASPI_USERNAME)
        password_input.send_keys(KASPI_PASSWORD)
        return driver

    def _confirm_code(self, driver):
        logger.info("Starting confirm code operations")
        login_button = driver.find_element_by_class_name("entrance__loginButton")
        login_button.click()

        time.sleep(20)

        code = get_confirmation_code()
        code_chars = [num for num in code]

        driver.find_element_by_id("txtOtpChar1").send_keys(code_chars[0])
        driver.find_element_by_id("txtOtpChar2").send_keys(code_chars[1])
        driver.find_element_by_id("txtOtpChar3").send_keys(code_chars[2])
        driver.find_element_by_id("txtOtpChar4").send_keys(code_chars[3])
        return driver

    def login(self):
        delay = 10
        logger.info("Opening the chrome")
        driver = webdriver.Chrome()
        driver.set_page_load_timeout(40)

        driver = self._get_login_page(driver=driver, delay=delay)
        driver = self._fill_credentials(driver=driver)
        driver = self._confirm_code(driver=driver)

        return driver

    def logout(self, driver, delay):
        logger.info("Log outing from system")
        driver.find_element_by_id("headerAuth").click()
        WebDriverWait(driver, delay).until(
            ec.presence_of_element_located(
                (By.CLASS_NAME, "headerSettings__item--logOut")
            )
        )
        driver.find_element_by_class_name("headerSettings__item--logOut").click()


class KaspiTransactions:
    def __init__(
        self, auth_service: KaspiAuth, links: Optional[Type[KaspiLinks]] = None
    ) -> None:
        self.auth_service = auth_service
        self.links = links
        if self.links is None:
            self.links = KaspiLinks

    def get_transactions(self):
        driver = self.auth_service.login()
        try:
            logger.info("Waiting for page load")
            WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, "myProductsMenu__link"))
            )
        except TimeoutException:
            driver.execute("window.stop();")
            logging.info(
                "Page loading stopped directly, " "cause of load time is out-of-date"
            )

        driver.find_elements_by_class_name("myProductsMenu__link")[-1].click()

        try:
            logger.info("Waiting for page load")
            WebDriverWait(driver, 20).until(
                ec.presence_of_element_located((By.CLASS_NAME, "goldOperation__list"))
            )
        except TimeoutException:
            driver.execute("window.stop();")
            logging.info(
                "Page loading stopped directly, " "cause of load time is out-of-date"
            )

        transactions = get_card_transactions_from_html(driver.page_source)
        return transactions
