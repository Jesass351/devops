import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time, sys
from selenium.webdriver.common.by import By

from auth import auth
from jokey import jokey
from owner import owner
from horse import horse
from competition import competition
from results import result

BASE_ADDRESS = 'http://127.0.0.1:5000'

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

driver.maximize_window()
driver.implicitly_wait(60)
   
driver.get(BASE_ADDRESS)


result_auth  = auth(driver=driver, address=BASE_ADDRESS)
assert result_auth == True, "Ошибка при авторизации"

result_jokey  = jokey(driver=driver, address=BASE_ADDRESS)
assert result_jokey == True, "Ошибка при добавлении жокея"

result_owner  = owner(driver=driver, address=BASE_ADDRESS)
assert result_owner == True, "Ошибка при добавлении владельца"


for i in range(2):
    result_horse  = horse(driver=driver, address=BASE_ADDRESS)
    assert result_horse == True, "Ошибка при добавлении лошади"
    
result_competition = competition(driver=driver, address=BASE_ADDRESS)
assert result_competition == True, "Ошибка при добавлении соревнования"

result_results = result(driver=driver, address=BASE_ADDRESS)
assert result_results == True, "Ошибка при добавлении результата сорвенования"



   # result_authorization = authorization(driver=driver)
   # assert result_authorization == True, "Ошибка в регистрации и авторизации."
   # result_mountains = mountains(driver=driver)
   # assert result_mountains == True, "Ошибка при добавлении горы."
   # result_climbers = climbers(driver=driver)
   # assert result_climbers == True, "Ошибка при добавлении альпиниста."
   # result_group = group(driver=driver)
   # assert result_group == True, "Ошибка при создании группы."
   # result_climbing = climbing(driver=driver)
   # assert result_climbing == True, "Ошибка при добавлении восхождения."

driver.close()
driver.quit()
