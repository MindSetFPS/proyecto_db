from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("http://localhost:3011")
assert "Python" in driver.title
elem = driver.find_element(By.NAME, "q")

driver.close()
