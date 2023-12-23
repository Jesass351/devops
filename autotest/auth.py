from selenium.webdriver.common.by import By

def auth(driver, address):
    result_login = login(driver, address)
    if not result_login:
        return False
    
    return True


def login(driver, address):
    try:
        data = {
            'login':'hfgjff',
            'password':'admin'
        }
        driver.get(f"{address}/auth/login")
        input_username = driver.find_element(By.ID, "login")
        input_password = driver.find_element(By.ID, "password")
        input_username.send_keys(data['login'])
        input_password.send_keys(data['password'])
        driver.find_element(By.XPATH, "/html/body/main/div/form/button").click()
        if "Вход выполнен успешно" in driver.find_element(By.XPATH, "/html/body/div/div").text:
            return True
        else:
            return False
    except:
        return False