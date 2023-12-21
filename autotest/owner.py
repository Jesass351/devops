from selenium.webdriver.common.by import By
from RandomWordGenerator import RandomWord
import random
from phone_gen import PhoneNumber

rw = RandomWord(max_word_size = 13,
                constant_word_size=True,
                include_digits=False,
                special_chars=r"@_!#$%^&*()<>?/\|}{~:",
                include_special_chars=False)

def owner(driver):
    result_add = add(driver)
    if not result_add:
        return False
    
    return True


def add(driver):
    # try:
        address = ''
        phone_number = PhoneNumber("DE").get_number()
        for i in range(random.randint(1,5)):
            address += rw.generate()
        data = {
            'name':rw.generate(),
            'address': address,
            'phone': phone_number
        }
        driver.get("http://127.0.0.1:5000/staff/create_owner")
        input_name = driver.find_element(By.ID, "name")
        input_address = driver.find_element(By.ID, "address")
        input_phone = driver.find_element(By.ID, "phone")
        
        
        input_name.send_keys(data['name'])
        input_address.send_keys(data['address'])
        input_phone.send_keys(data['phone'])
        
        driver.find_element(By.ID, "submit-btn").click()
        if "Владелец успешно добавлен" in driver.find_element(By.XPATH, "/html/body/div/div").text:
            return True
        else:
            return False
    # except:
    #     return False