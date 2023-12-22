from selenium.webdriver.common.by import By
from RandomWordGenerator import RandomWord
from selenium.webdriver.support.select import Select
import random

rw = RandomWord(max_word_size = 13,
                constant_word_size=True,
                include_digits=False,
                special_chars=r"@_!#$%^&*()<>?/\|}{~:",
                include_special_chars=False)

def jokey(driver, address):
    result_add = add(driver, address)
    if not result_add:
        return False
    return True


def add(driver, addr):
    try:
        address = ''
        for i in range(random.randint(1,5)):
            address += rw.generate()
        data = {
            'name':rw.generate(),
            'address': address,
            'age': random.randint(18,90),
            'rating': random.randrange(11, 50) / 10
        }
        driver.get(f"{addr}/staff/create_jokey")
        input_name = driver.find_element(By.ID, "name")
        input_address = driver.find_element(By.ID, "address")
        input_age = driver.find_element(By.ID, "age")
        input_rating = driver.find_element(By.ID, "rating")
        
        input_name.send_keys(data['name'])
        input_address.send_keys(data['address'])
        input_age.send_keys(data['age'])
        input_rating.send_keys(data['rating'])
        
        driver.find_element(By.ID, "submit-btn").click()
        if "Жокей успешно добавлен" in driver.find_element(By.XPATH, "/html/body/div/div").text:
            return True
        else:
            return False
    except:
        return False
    