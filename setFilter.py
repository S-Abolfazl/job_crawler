from selenium.webdriver.common.by import By
from time import sleep


def set_filter(driver):
    # go to jobs
    try:
        sleep(1)
        driver.find_element(By.XPATH, '//*[@type="submit"]').click()
    except:
        return False, 'search btn for going to jobs not found!'

    # set job category
    try:
        # more btn
        sleep(3)
        driver.find_element(By.XPATH, '//*[@class="c-jobSearchSide__subListToggler c-jobSearch__subListItem"]').click()
        driver.find_element(By.XPATH, "//span[text()='وب،‌ برنامه‌نویسی و نرم‌افزار']").click()

        # more btn
        sleep(4)
        driver.find_element(By.XPATH, '//*[@class="c-jobSearchSide__subListToggler c-jobSearch__subListItem"]').click()
        driver.find_element(By.XPATH, "//span[text()='IT / DevOps / Server']").click()
    except Exception as e:
        return False, f'job categories checkboxes not found! : {e}'

    # set province to 'Tehran'
    try:
        sleep(1)
        element = driver.find_element(By.XPATH, '//*[@value="تهران" and @type="checkbox"]')
        parent_element = driver.execute_script("return arguments[0].parentNode.parentNode;", element)
        parent_element.click()
    except:
        return False, 'province checkbox not found!'

    return True, 'successfully filtered'
