import ast
import json
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

link = "http://dev-ship-tms.zuumapp.com/#/auth/signup"
data = {"email": "testtetst118@mailinator.com",
                 "companyName": "testttt inc",
                 "firstName": 'test',
                 "lastName": 'test',
                 "phoneNumber": "1131134432",
                 "password": "testtest",
                 "confirmPassword": "testtest",
                 "type": "shipper",
                 "roles": "shipper_admin"}


@pytest.fixture(scope="class")
def browser():
    print("\nstart browser for test..")
    browser = webdriver.Chrome()
    yield browser
    print("\nquit browser..")
    time.sleep(60)
    browser.quit()


class TestRegisterForm:
    # вызываем фикстуру в тесте, передав ее как параметр

    def test_init(self, browser):
        browser.get(link)
        browser.refresh()
        browser.maximize_window()
        time.sleep(5)

    def test_mail(self, browser):
        mail_field = browser.find_element(By.XPATH, "//*[@placeholder='Email']")
        mail_field.send_keys(data['email'])

        mail_field.send_keys(Keys.TAB)
        time.sleep(2)
        check_accept = browser.find_element(By.ID, "mat-hint-0")
        assert check_accept.text == "Available", "ERROR SOMETHING WRONG"

    def test_company_name(self, browser):
        company_name_field = browser.find_element(By.XPATH, "//*[@placeholder='Company Name']")
        company_name_field.send_keys(data['companyName'])

        company_name_field.send_keys(Keys.TAB)
        time.sleep(2)
        check_accept = browser.find_element(By.ID, "mat-hint-1")
        assert check_accept.text == "Available", "ERROR SOMETHING WRONG"

    def test_first_name(self, browser):
        first_name_field = browser.find_element(By.XPATH, "//*[@placeholder='First Name']")
        first_name_field.send_keys(data['firstName'])

    def test_last_name(self, browser):
        last_name_field = browser.find_element(By.XPATH, "//*[@placeholder='Last Name']")
        last_name_field.send_keys(data['lastName'])

    def test_phone_number(self, browser):
        phone_number_field = browser.find_element(By.XPATH, "//*[@placeholder='Phone Number']")
        phone_number_field.send_keys(data['phoneNumber'])

        phone_number_field.send_keys(Keys.TAB)
        time.sleep(2)
        check_accept = browser.find_element(By.ID, "mat-hint-2")
        assert check_accept.text == "Available", "ERROR SOMETHING WRONG"

    def test_password(self, browser):
        password_field = browser.find_element(By.XPATH, "//*[@placeholder='Password']")
        password_field.send_keys(data['password'])

    def test_confirm_password(self, browser):
        confirm_password_field = browser.find_element(By.XPATH, "//*[@placeholder='Confirm Password']")
        confirm_password_field.send_keys(data['confirmPassword'])

        confirm_password_field.send_keys(Keys.TAB)
        time.sleep(2)
        check_password = browser.find_element(By.ID, "mat-hint-3")
        assert check_password.text == "Password matched!", "ERROR SOMETHING WRONG"

    def test_checkbox(self, browser):
        conf = browser.find_element(By.ID, "mat-checkbox-1-input")
        # x = browser.find_element(By.XPATH, ".//span[@class = 'terms-text ml-4']")

        actions = ActionChains(browser)
        actions.move_to_element(conf).perform()
        browser.execute_script("arguments[0].click();", conf)

    def test_accept_button(self, browser):
        button = browser.find_element(By.CLASS_NAME, "mat-raised-button.mat-primary")
        button.click()

    def test_response(self, browser):
        time.sleep(6)
        url = "http://dev-ship-api.zuumapp.com/users/shipper?key=null"
        response = requests.post(url, json=data)
        res = json.loads(response.text)
        print(res)
        time.sleep(2)
        form = browser.find_element(By.XPATH, "//*[@formcontrolname='firstChar']")
        form.send_keys(res['data']['activationCode'])

        button = browser.find_elements(By.CLASS_NAME, "mat-raised-button.mat-primary")
        button[1].click()
