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
           
        except Exception as e:
            print(f"Test failed: Error: {str(e)}")
        self.browser.close()
        
    def test_buy_mp(self):
        tarjeta_prueba = "5474 9254 3267 0366"
        codigo_seguridad = "123"
        caducidad = "11/25"
        nombre = "APRO" 

        self.browser.get(self.url + "/login") # Login
        elem_user_id = self.browser.find_element(By.ID, "id_username")
        elem_user_id.click()
        elem_user_id.send_keys("selenium")
        
        password_element = self.browser.find_element(By.ID, "id_password")
        password_element.send_keys("selenium")
        
        submit_button = self.browser.find_element(By.ID, "submit_button")
        submit_button.click()
    
        time.sleep(3)
        # Go to product
        self.browser.get(self.url + "/product/1")
        
        add_to_cart_button = self.browser.find_element(By.ID, "add_to_cart_button")
        add_to_cart_button.click()
        
        time.sleep(3)
        
        checkout_button = self.browser.find_element(By.ID, "checkout-button")
        checkout_button.click()
        time.sleep(10) 

        debit_button = self.browser.find_element(By.ID, "debit_and_prepaid_card_row")
        debit_button.click()
        
        debit_input = self.browser.find_element(By.ID, "card_number")
        debit_button.send_keys(tarjeta_prueba)
        
        name_input = self.browser.find_element(By.ID, "fullname")
        name_input.send_keys(nombre)
        
        expiration_input = self.browser.find_element(By.ID, "expiration_date")
        expiration_input.send_keys(caducidad)
        
        security_code_input = self.browser.find_element(By.ID, "securityCode")
        security_code_input.send_keys(codigo_seguridad)
        
        mp_submit_button = self.browser.find_element(By.ID, "submit")
        mp_submit_button.click()
        
        final_pay_button = self.browser.find_element(By.ID, ":r1j:")
        final_pay_button.click()
        
        time.sleep(50)