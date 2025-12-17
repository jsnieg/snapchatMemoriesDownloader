from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from typing import LiteralString

FILE_PATH: LiteralString = f'../mydata/html/memories_history.html'

driver = webdriver.Firefox()
file = driver.get(FILE_PATH)
assert "Python" in driver.title
print(file)
assert "No results found." not in driver.page_source
driver.close()