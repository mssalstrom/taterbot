# Used to make sure the amount of api request is < 150
import codecs
import time
from selenium import webdriver
from dotenv import load_dotenv
import os
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import re
from datetime import date
from bs4 import BeautifulSoup
import json
import asyncio
load_dotenv('.env')


def request_check():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://spoonacular.com/food-api/console#")
    # driver.minimize_window()
    driver.implicitly_wait(0.8)
    already_have_acn = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[1]/p[1]/a")
    already_have_acn.click()
    usr_login = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[1]/input[1]")
    usr_pw = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[1]/input[2]")
    usr_login.send_keys(os.getenv('user_name'))
    usr_pw.send_keys(os.getenv('pw'))
    login_click = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[1]/button")
    login_click.click()


def new_request_page():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://api.spoonacular.com/spoonacular-api/callStats?apiKey=b015b2c2c8eb4ddcbd0f86bbe946eb27")
    file_save = os.path.join("C:\\Users\\salst\\Desktop\\TaterBot2.0", "PageSave.html")
    f = codecs.open(file_save, "w", "utf-8")
    h = driver.page_source
    f.write(h)

 def get_request_amount():
    with open('PageSave.html') as fp:
        soup = BeautifulSoup(fp, 'lxml')
    d = json.loads(soup.find("pre").string)
    new_list = d[6]
    request_total = new_list["requests"]
    print(request_total)
    return request_total


get_request_amount()
