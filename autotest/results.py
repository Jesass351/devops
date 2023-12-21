from selenium.webdriver.common.by import By
from RandomWordGenerator import RandomWord
import random
from selenium.webdriver.support.select import Select
import datetime

rw = RandomWord(max_word_size = 13,
                constant_word_size=True,
                include_digits=False,
                special_chars=r"@_!#$%^&*()<>?/\|}{~:",
                include_special_chars=False)

def result(driver):
    result_add = add(driver)
    if not result_add:
        return False
    
    return True


def add(driver):
    # try:
        place = ''
        for i in range(random.randint(1,5)):
            place += rw.generate()
        data = {
            'title':rw.generate(),
            'place': place,
            'date': datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
        }
        driver.get("http://127.0.0.1:5000/results/create_form/1")
        horses_times = driver.find_elements(By.ID, 'horse_time')
        horses_places = driver.find_elements(By.ID, 'horse_place')
        
        horses_times[0].send_keys('1:47.1')
        horses_places[0].send_keys('1')
        
        
        horses_times[1].send_keys('1:48.3')
        horses_places[1].send_keys('2')
        
        
        
        driver.find_element(By.ID, "submit-btn").click()
        if "Результаты добавлены" in driver.find_element(By.XPATH, "/html/body/div/div").text:
            return True
        else:
            return False
    # except:
    #     return False