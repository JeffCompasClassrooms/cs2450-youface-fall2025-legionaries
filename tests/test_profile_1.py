from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Don't specify chromedriver path!
driver = webdriver.Chrome(options=options)

def test_username_displays():
    username = driver.find_element(By.NAME, "username")
    if username:
        return True
    else:
        return False
def test_profile_image_displays1():
    image = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "profile-image"))
    )
    return image.is_displayed()

def test_profile_image_displays():
    image = driver.find_element(By.ID, "profile-image-3")
    #image = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div/div[2]/div[1]/img")
    #image = driver.find_element(By.CSS_SELECTOR, "body > div.container > div > div > div > div > div:nth-child(2) > div:nth-child(1) > img")
    #image = None
    if image:
        return True
    else:
        return False

def test_userne():
    username = driver.find_element(By.ID, "userne")
    if username:
        return True
    else:
        return False

def test_profile_banner_displays():
    banner = driver.find_element(By.NAME, "profile-banner")
    if banner:
        return True
    else:
        return False

def test_profile_picture_updates():
    pass

def test_profile_bio_updates():
    pass

def test_audio_player_displays():
    pass

def test_bio_displays():
    pass

def test_profile_picture_selector_displays():
    pass

def test_profile_banner_selector_displays():
    pass

def test_profile_audio_selector_displays():
    pass

try:
    driver.get("http://127.0.0.1:5005/profile/newuser1")
    time.sleep(2)

    print("--= Beginning Tests =--")

    username_displays = test_username_displays()
    if username_displays:
        print("[PASSED] - Username displays.")
    else:
        print("[FAILED] - Username not found.")

#    userne_displays = test_userne()
#    if userne_displays:
#        print("[PASSED] - Userne displays.")
#    else:
#        print("[FAILED] - Userne not found.")

    profile_image_displays = test_profile_image_displays()
    if profile_imagee_displays:
        print("[PASSED] - Profile image displays.")
    else:
        print("[FAILED] - Profile image not found.")

    profile_banner_displays = test_profile_banner_displays()
    if profile_banner_displays:
        print("[PASSED] - Profile banner displays.")
    else:
        print("[FAILED] - Profile banner not found.")

except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()
