import time
import pytest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

link = " https://qa-ship-tms.zuumapp.com/#/auth/login"
user_info = {"mail": "testshipper5@mailinator.com",
             "password": "111111",
             "pick_up_address": "344 Tully Rd, San Jose, CA 95111, USA ",
             "drop_address": "8687 N Central Expy, Dallas, TX 75231, USA",
             "pickup_date": "3/15/2021",
             "truck_type": "53' Dry Van",
             "weight": "30000", }

ua = dict(DesiredCapabilities.CHROME)


@pytest.fixture(scope="class")
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x935')
    print("\nstart browser for test..")
    browser = webdriver.Chrome(chrome_options=options)
    yield browser
    print("\nquit browser..")
    time.sleep(60)
    browser.quit()


class TestRegisterForm:
    # вызываем фикстуру в тесте, передав ее как параметр

    def test_init(self, browser):
        browser.get(link)
        browser.refresh()
        time.sleep(2)

    def test_login(self, browser):
        mail_field = browser.find_element(By.XPATH, "//*[@placeholder='Email']")
        mail_field.send_keys(user_info['mail'])
        mail_field.send_keys(Keys.TAB)
        time.sleep(2)
        # check_error = browser.find_element(By.ID, "mat-hint-0")
        # assert browser.find_element(By.ID, "mat-error-0"), "ERROR SOMETHING WRONG WITH LOGIN"

        password_field = browser.find_element(By.XPATH, "//*[@placeholder='Password']")
        password_field.send_keys(user_info['password'])
        password_field.send_keys(Keys.TAB)
        time.sleep(2)
        # check_error = browser.find_element(By.ID, "mat-hint-0")
        # assert browser.find_element(By.ID, "mat-error-1"), "ERROR SOMETHING WRONG WITH PASSWORD"

    def test_accept_button(self, browser):
        button = browser.find_element(By.CLASS_NAME, "submit-button.mat-raised-button.mat-accent")
        button.click()

    def test_get_quotes_button(self, browser):
        time.sleep(2)
        # button = browser.find_element(By.CLASS_NAME, "nav-link.ng-star-inserted.active")
        # print(button.text)
        # button.click()
        browser.get("https://qa-ship-tms.zuumapp.com/#/main/quotes/new")
        time.sleep(2)

    def test_fill_address_pickup_form(self, browser):
        time.sleep(2)
        pickup_address = browser.find_elements(By.XPATH, "//*[@placeholder='Enter a location']")
        pickup_address[2].send_keys(user_info['pick_up_address'])
        time.sleep(2)
        pickup_address[2].send_keys(Keys.DOWN)
        pickup_address[2].send_keys(Keys.ENTER)

    def test_fill_address_drop_form(self, browser):
        webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
        time.sleep(2)
        drop_address = browser.find_elements(By.XPATH, "//*[@placeholder='Enter a location']")
        drop_address[3].send_keys(user_info['drop_address'])
        time.sleep(2)
        drop_address[3].send_keys(Keys.DOWN)
        drop_address[3].send_keys(Keys.ENTER)
        time.sleep(1)
        # webdriver.ActionChains(drop_address).send_keys(Keys.ESCAPE).perform()
        # webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()

    def test_fill_date_form(self, browser):
        # webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
        # webdriver.ActionChains(browser).send_keys(Keys.DELETE).perform()
        # webdriver.ActionChains(browser).send_keys(Keys.INSERT('4/13/2021')).perform()
        date_form = browser.find_element(By.XPATH, '//tbody[@class="mat-calendar-body"]//tr[4]//td[4]')
        date_form.click()

    def test_fill_track(self, browser):
        track_form = browser.find_elements(By.CLASS_NAME, "mat-checkbox-layout")
        track_form[4].click()
        time.sleep(2)
        button = browser.find_elements(By.CLASS_NAME, "mat-raised-button.mat-primary")
        button[3].click()

    def test_fill_weight_form(self, browser):
        time.sleep(2)
        #webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
        weight_form = browser.find_element(By.XPATH, "//*[@placeholder='Weight (lbs)']")
        weight_form.send_keys(user_info['weight'])
        weight_form.send_keys(Keys.TAB)

    def test_confirm(self, browser):
        button = browser.find_element(By.CLASS_NAME, "ml-28.mat-raised-button.mat-primary")
        assert button.is_enabled(), "ERROR"
        button.click()
