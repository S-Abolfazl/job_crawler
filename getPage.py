from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

username = 'qseyyed@gmail.com'
password = '32520146saq'


def getPage():
    # settings
    driver = webdriver.Chrome()
    url = 'https://jobinja.ir/'

    # start driver
    driver.get(url)

    # find and login
    # input btn
    try:
        sleep(1)
        driver.find_element(By.CSS_SELECTOR,
                            'a.c-nav2__extraLink.c-nav2IconLink.c-nav2IconLink--hasText.o-iconLink').click()
    except:
        return False, 'input button not found'

    # username field
    try:
        sleep(1)
        driver.find_element(By.XPATH, '//*[@placeholder="آدرس ایمیل خود را وارد نمایید"]').send_keys(username)
    except:
        return False, 'email box not found!'

    # password field
    try:
        sleep(1)
        driver.find_element(By.XPATH, '//*[@placeholder="رمز عبور خود را وارد نمایید"]').send_keys(password)
    except:
        return False, 'email box not found!'

    try:
        driver.find_element(By.XPATH, '//*[@name="remember_me"]').click()
    except:
        pass

    # submit btn
    try:
        sleep(1)
        driver.find_element(By.XPATH, '//*[@value="وارد شوید"]').click()
    except:
        return False, 'submit btn not found!'

    # page is ready
    return True, driver
