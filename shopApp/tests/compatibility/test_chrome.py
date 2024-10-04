from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from django.test import TestCase

class TestChrome(TestCase):
    def setUp(self):
        self.url = "http://192.168.1.140:3011"
        self.browser = webdriver.Chrome()

    def test_navbar(self):
        """ Should be none by default, block when hovering. """
        self.browser.get(self.url)
        action_chains = ActionChains(driver=self.browser)

        # Get products button
        products_button = self.browser.find_element(By.ID, "productos")
        
        # Get dropdown
        product_dropdown = products_button.find_element(By.XPATH, "following-sibling::*")

        # display is none by default
        self.assertEqual(product_dropdown.value_of_css_property("display"), 'none')
        
        # hover button, show dropdown
        action_chains.move_to_element(products_button).perform()
        
        # dropdown's display is block when hovering
        self.assertEqual(product_dropdown.value_of_css_property("display"), 'block')

    def test_navbar_mobile(self):
        """ Should be none by default, block when clicked. """
        self.browser.get(self.url)
        self.browser.set_window_size(412, 915)
        action_chains = ActionChains(driver=self.browser)

        # Get products button
        products_button = self.browser.find_element(By.ID, "productos")
        
        # Get dropdown
        product_dropdown = products_button.find_element(By.XPATH, "following-sibling::*")

        # display is none by default
        self.assertEqual(product_dropdown.value_of_css_property("display"), 'none')
        
        # hover button, show dropdown
        action_chains.move_to_element(products_button).perform()
        
        # dropdown's display is block when hovering
        self.assertEqual(product_dropdown.value_of_css_property("display"), 'block')