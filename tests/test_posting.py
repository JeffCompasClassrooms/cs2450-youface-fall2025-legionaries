from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1200,800")

# Don't specify chromedriver path!
driver = webdriver.Chrome(options=options)
try:
    web_url = "http://localhost:3000/"
    driver.get(web_url)
    time.sleep(2)
    print("Getting into Home Page...")

    username = driver.find_element(
        By.CSS_SELECTOR, "input[type='text'][name='username']"
    )
    password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    username.send_keys("test")
    password.send_keys("test")
    create_user = driver.find_element(By.CSS_SELECTOR, "input[value='Create']")
    create_user.click()

    print("--= Beginning Tests =--")
    print("   --- Fabrizio ---")
    nsfw_check = driver.find_element(
        By.CSS_SELECTOR, "input[type='checkbox'][name='nsfw_toggle']"
    )
    post_input = driver.find_element(By.CSS_SELECTOR, "textarea[name='post']")
    post_submit = driver.find_element(
        By.CSS_SELECTOR, "button[type='submit'][value='manual']"
    )
    ai_submit = driver.find_element(
        By.CSS_SELECTOR, "button[type='submit'][value='ai']"
    )
    media_add = driver.find_element(By.CSS_SELECTOR, "input[type='file'][name='image']")

    if nsfw_check:
        print("[PASSED] - NSFW checkbox Exists.")
    else:
        print("[FAILED] - NSFW checkbox not found.")

    if post_submit:
        print("[PASSED] - Manual post submit button Exists.")
    else:
        print("[FAILED] - Manual post submit button not found.")

    if ai_submit:
        print("[PASSED] - AI submit button Exists.")
    else:
        print("[FAILED] - AI submit button not found.")
    if media_add:
        print("[PASSED] - Link media button Exists.")
    else:
        print("[FAILED] - Link media button not found.")

    nsfw_check.click()
    post_input.send_keys("Check out this super NSFW post")
    post_submit.click()
    time.sleep(1)

    post_input = driver.find_element(By.CSS_SELECTOR, "textarea[name='post']")
    post_submit = driver.find_element(
        By.CSS_SELECTOR, "button[type='submit'][value='manual']"
    )

    post_input.send_keys("sfw labubu post")
    post_submit.click()
    time.sleep(1)
    page_text = driver.find_element("tag name", "body").text
    if "Check out this super NSFW post" in page_text:
        print("[PASSED] - NSFW can post")
    else:
        print("[FAILED] - NSFW post does not work.")
    if "sfw labubu post" in page_text:
        print("[PASSED] - SFW can post")
    else:
        print("[FAILED] - SFW post does not work.")
    time.sleep(1)

    logout = driver.find_element(
        By.CSS_SELECTOR, "button[type='submit'][class='btn btn-secondary']"
    )
    if logout:
        print("[PASSED] - Logout button Exists.")
    else:
        print("[FAILED] - Logout button not found.")
    logout.click()
    time.sleep(1)
    if driver.current_url == (web_url + "loginscreen"):
        print("[PASSED] - Logout sends user to login screen.")
    else:
        print("[FAILED] - Logout does not return to login screen.")

    username = driver.find_element(
        By.CSS_SELECTOR, "input[type='text'][name='username']"
    )
    password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    delete = driver.find_element(By.CSS_SELECTOR, "input[value='Delete']")
    username.send_keys("test")
    password.send_keys("test")
    if delete:
        print("[PASSED] - Delete button Exists.")
    else:
        print("[FAILED] - Delete button not found.")
    delete.click()
    time.sleep(1)
    alert_text = driver.find_element(By.CSS_SELECTOR, "div[role='alert']").text
    if "User test deleted successfully!" in alert_text:
        print("[PASSED] - User deletion pops up alert.")
    else:
        print("[FAILED] - User deletion does not pop up alert.")


except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()
