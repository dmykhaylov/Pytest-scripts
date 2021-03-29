import time
import pytest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

link = " https://qa-ship-tms.zuumapp.com/#/auth/login"
user_info = {"mail": "testshipper5@mailinator.com",
             "password": "111111",
             "pick_up_address": "344 Tully Rd, San Jose, CA 95111, USA ",
             "drop_address": "8687 N Central Expy, Dallas, TX 75231, USA",
             "pickup_date": "30",
             "truck_type": "53' Dry Van",
             "weight": "30000",
             "pickup_name": "games-workshop",
             "drop_name": "my home",
             "appointment_pickup_type": "Appointment Pending",
             "appointment_drop_type": "Appointment Pending",
             "commodity": "some text here"
             }


@pytest.fixture(scope="class")
def browser():
    print("\nstart browser for test..")
    browser = webdriver.Chrome()
    browser.maximize_window()
    yield browser
    print("\nquit browser..")
    time.sleep(15)
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
        time.sleep(2)
        # check_error = browser.find_element(By.ID, "mat-hint-0")
        # assert browser.find_element(By.ID, "mat-error-1"), "ERROR SOMETHING WRONG WITH PASSWORD"

    def test_login_accept_button(self, browser):
        button = browser.find_element(By.CLASS_NAME, "submit-button.mat-raised-button.mat-accent")
        button.click()

    def test_get_quotes_button(self, browser):
        time.sleep(2)
        # button = browser.find_element(By.CLASS_NAME, "nav-link.ng-star-inserted.active")
        # print(button.text)
        # button.click()
        browser.get("https://qa-ship-tms.zuumapp.com/#/main/quotes/new")
        time.sleep(2)

    def test_new_quote_fill_address_pickup_form(self, browser):
        time.sleep(2)
        pickup_address = browser.find_elements(By.XPATH, "//*[@placeholder='Enter a location']")
        pickup_address[2].send_keys(user_info['pick_up_address'])
        time.sleep(2)
        pickup_address[2].send_keys(Keys.DOWN)
        pickup_address[2].send_keys(Keys.ENTER)

    def test_new_quote_fill_address_drop_form(self, browser):
        webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
        drop_address = browser.find_elements(By.XPATH, "//*[@placeholder='Enter a location']")
        drop_address[3].send_keys(user_info['drop_address'])
        time.sleep(2)
        drop_address[3].send_keys(Keys.DOWN)
        drop_address[3].send_keys(Keys.ENTER)
        time.sleep(1)

    def test_new_quote_fill_date_form(self, browser):
        date_form = browser.find_elements(By.CLASS_NAME, 'mat-calendar-body-cell-content')
        for i in date_form:
            if user_info["pickup_date"] == i.text:
                i.click()
                break

    def test_new_quote_fill_track(self, browser):
        track_form = browser.find_elements(By.CLASS_NAME, "mat-checkbox-layout")
        for i in track_form:
            if i.text == user_info['truck_type']:
                i.click()
                break
        button = browser.find_elements(By.CLASS_NAME, "mat-raised-button.mat-primary")
        button[3].click()

    def test_new_quote_fill_weight_form(self, browser):
        time.sleep(2)
        weight_form = browser.find_element(By.XPATH, "//*[@placeholder='Weight (lbs)']")
        weight_form.send_keys(user_info['weight'])
        weight_form.send_keys(Keys.TAB)

    def test_new_quote_confirm(self, browser):
        button = browser.find_element(By.CLASS_NAME, "ml-28.mat-raised-button.mat-primary")
        assert button.is_enabled(), "ERROR"
        button.click()

    def test_new_quote_book_it(self, browser):
        time.sleep(3)
        book_it = browser.find_element(By.CLASS_NAME, "price_main-btn.mat-raised-button.mat-primary")
        book_it.click()
        time.sleep(3)

    def test_details_location_name_pickup(self, browser):
        location_name = browser.find_element(By.XPATH, "//*[@placeholder='Location Name']")
        location_name.send_keys(user_info['pickup_name'])

    def test_details_appointment_type_pickup(self, browser):
        webdriver.ActionChains(browser).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
        types = browser.find_elements(By.CLASS_NAME, "mat-option-text")
        for i in types:
            print(i.text)
            if i.text == user_info['appointment_pickup_type']:
                i.click()
                break

    def test_details_location_name_drop(self, browser):
        location_name = browser.find_elements(By.XPATH, "//*[@placeholder='Location Name']")
        location_name[1].send_keys(user_info['drop_name'])

    def test_details_appointment_type_drop(self, browser):
        webdriver.ActionChains(browser).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
        types = browser.find_elements(By.CLASS_NAME, "mat-option-text")
        for i in types:
            print(i.text)
            if i.text == user_info['appointment_drop_type']:
                i.click()
                break
        time.sleep(1)

    def test_details_commodity(self, browser):
        commodity = browser.find_elements(By.XPATH, "//*[@placeholder='Commodity']")
        webdriver.ActionChains(browser).move_to_element(commodity[1])
        commodity[1].send_keys(user_info['commodity'])

    def test_details_save_and_continue(self, browser):
        button = browser.find_elements(By.CLASS_NAME, "ml-28.mat-raised-button.mat-primary")
        button[1].click()

    def test_book_page_agreed(self, browser):
        time.sleep(2)
        agreed = browser.find_elements(By.CLASS_NAME, "mat-checkbox-inner-container")
        print(agreed)
        webdriver.ActionChains(browser).move_to_element(agreed[3]).perform()
        agreed[3].click()

    def test_book_page_book(self, browser):
        time.sleep(1)
        button = browser.find_element(By.CLASS_NAME, "ml-16.mat-raised-button.mat-primary")
        assert button.is_enabled(), "EROOR"
        button.click()
        time.sleep(3)

    def test_final_ok(self, browser):
        ok = browser.find_element(By.CLASS_NAME, "mat-raised-button.mat-primary")
        ok.click()
