import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

TROLLR_URL = "http://127.0.0.1:5005/loginscreen"

def perform_login(driver, username, password):
    """
    Logs into the app using the given driver and credentials.
    Returns True if successful, False if failed.
    """
    driver.get(TROLLR_URL)
    time.sleep(1)

    try:
        username_box = driver.find_element(By.NAME, "username")
        password_box = driver.find_element(By.NAME, "password")
        login_btn = driver.find_element(By.CLASS_NAME, "btn-primary")
    except NoSuchElementException:
        print("[ERROR] Login form elements not found.")
        return False

    print("USERNAME IS ",username)
    print("PASSWORD IS ",password)
    username_box.send_keys(username)
    password_box.send_keys(password)
    login_btn.click()

    time.sleep(1)  # can replace with WebDriverWait later

    if "loginscreen" in driver.current_url:
        print("[FAILED] Login failed.")
        return False

    print("[SUCCESS] Login succeeded.")
    return True

