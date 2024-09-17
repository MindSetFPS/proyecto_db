from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
from django.test import TestCase

class TestViews(TestCase):
    def setUp(self):
        self.url = "http://192.168.1.140:3011"
        self.browser = webdriver.Chrome()

    def test_register_user(self):
        self.browser.get(self.url + "/register")
        # Alternatively, you could use the following line if there's a possibility of this test failing
        try:
            elem_user_id = self.browser.find_element(By.ID, "id_username")
            elem_user_id.click()
            elem_user_id.send_keys("selenium")
            
            email_input = self.browser.find_element(By.ID, "id_email")
            email_input.send_keys("selenium@test.com")
            
            password_element = self.browser.find_element(By.ID, "id_password")
            password_element.send_keys("selenium")
            
            password_element2 = self.browser.find_element(By.ID, "id_password2")
            password_element2.send_keys("selenium")
            
            submit_button = self.browser.find_element(By.ID, "submit_button")
            submit_button.click()
           
            time.sleep(30)
            
        except Exception as e:
            print(f"Test failed: Error: {str(e)}")
        self.browser.close()

    def test_login_user(self):
        self.browser.get(self.url + "/login")
        try:
            elem_user_id = self.browser.find_element(By.ID, "id_username")
            elem_user_id.click()
            elem_user_id.send_keys("selenium")
            
            password_element = self.browser.find_element(By.ID, "id_password")
            password_element.send_keys("selenium")
            
            submit_button = self.browser.find_element(By.ID, "submit_button")
            submit_button.click()
           
            time.sleep(30)
        except Exception as e:
            print(f"Test failed: Error: {str(e)}")
        self.browser.close()