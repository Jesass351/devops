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

def competition(driver, address):
    result_add = add(driver)
    if not result_add:
        return False
    
    return True


def add(driver, address):
    # try:
        place = ''
        for i in range(random.randint(1,5)):
            place += rw.generate()
        data = {
            'title':rw.generate(),
            'place': place,
            'date': datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
        }
        driver.get(f"{address}/competitions/create_form")
        input_title = driver.find_element(By.ID, "title")
        input_date = driver.find_element(By.ID, "date")
        input_place = driver.find_element(By.ID, "place")
        
        
        input_title.send_keys(data['title'])
        input_date.send_keys(data['date'])
        input_place.send_keys(data['place'])
        
        horse_select = Select(driver.find_element(By.ID, "horses"))
        horse_select.select_by_index(0)
        horse_select.select_by_index(1)
        
        
        driver.find_element(By.ID, "submit-btn").click()
        if "Соревнование успешно добавлено" in driver.find_element(By.XPATH, "/html/body/div/div").text:
            return True
        else:
            return False
    # except:
    #     return False