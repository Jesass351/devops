from selenium.webdriver.common.by import By
from RandomWordGenerator import RandomWord
import random
from selenium.webdriver.support.select import Select

rw = RandomWord(max_word_size = 13,
                constant_word_size=True,
                include_digits=False,
                special_chars=r"@_!#$%^&*()<>?/\|}{~:",
                include_special_chars=False)

def horse(driver, address):
    result_add = add(driver, address)
    if not result_add:
        return False
    
    return True


def add(driver, address):
    # try:
        data = {
            'name':rw.generate(),
            'age': random.randint(2,20),
        }
        driver.get(f"{address}/staff/create_horse")
        input_name = driver.find_element(By.ID, "name")
        input_age = driver.find_element(By.ID, "age")
        gender_select = Select(driver.find_element(By.ID, "gender"))
        owner_select = Select(driver.find_element(By.ID, "owner"))
        jokey_select = Select(driver.find_element(By.ID, "jokey"))
        
        
        gender_select.select_by_index(0)
        owner_select.select_by_index(0)
        jokey_select.select_by_index(0)
        
        input_name.send_keys(data['name'])
        input_age.send_keys(data['age'])
        
        
        
        driver.find_element(By.ID, "submit-btn").click()
        if "Лошадь успешно добавлена" in driver.find_element(By.XPATH, "/html/body/div/div").text:
            return True
        else:
            return False
    # except:
    #     return False