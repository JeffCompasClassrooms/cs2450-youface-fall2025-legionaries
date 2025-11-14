from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from helpers.login_helper import perform_login
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
#options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Don't specify chromedriver path!
#driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

passed = 0
failed = 0
total = 10

def test_username_displays():
    username = driver.find_element(By.NAME, "username")
    if username:
        return True
    else:
        return False

def test_profile_image_displays():
    image = driver.find_element(By.ID, "profile-image")
    if image:
        return True
    else:
        return False

def test_profile_banner_displays():
    banner = driver.find_element(By.ID, "banner-image")
    if banner:
        return True
    else:
        return False

def test_profile_picture_updates(driver, needs_rerouting=False):
    if needs_rerouting:
        driver.get("http://127.0.0.1:5005/profile/edit")
        time.sleep(2)
    try: 
        old_image = driver.find_element(By.ID, "profile-image")
        old_image_content = old_image.get_attribute("src")
        upload_profile_picture_button = driver.find_element(By.ID, "upload-profile-picture-button")
        image_path = "/Users/corbinbroadhead/Documents/test_image.jpg"
        upload_profile_picture_button.send_keys(image_path)
        save_button = driver.find_element(By.ID, "save-button")
        save_button.click()
        new_image = driver.find_element(By.ID, "profile-image")
        new_image_content = new_image.get_attribute("src")
        if new_image_content == old_image_content:
            return False
    except Exception as e:
        print("Test failed due to error: ",str(e))
        return False
    return True

def test_profile_bio_displays(driver, needs_rerouting=False):
    if needs_rerouting:
        driver.get("http://127.0.0.1:5005/profile/edit")
        time.sleep(2)
    bio_entry_field = driver.find_element(By.ID, "bio-entry-field")
    if not bio_entry_field:
        return False
    return True

def test_audio_player_displays(driver, needs_rerouting=False):
    if needs_rerouting:
        driver.get("http://127.0.0.1:5005/profile/edit")
        time.sleep(2)
    audio_player_display = driver.find_element(By.ID, "audio-player")
    if not audio_player_display:
        return False
    return True

def test_profile_bio_updates(driver, needs_rerouting=False):
    if needs_rerouting:
        driver.get("http://127.0.0.1:5005/profile/edit")
        time.sleep(2)
    bio_field = driver.find_element(By.ID, "bio-entry-field")
    bio_field.send_keys("suffix")
    save_button = driver.find_element(By.ID, "save-button")
    save_button.click()
    bio = driver.find_element(By.ID, "bio")
    if not bio.text.endswith("suffix"):
        return False
    return True

def test_profile_picture_selector_displays(driver, needs_rerouting=False):
    if needs_rerouting:
        driver.get("http://127.0.0.1:5005/profile/edit")
        time.sleep(2)
    upload_profile_picture_selector = driver.find_element(By.ID, "upload-profile-picture-button")
    if not upload_profile_picture_selector:
        return False
    return True

def test_profile_banner_selector_displays(driver, needs_rerouting=False):
    if needs_rerouting:
        driver.get("http://127.0.0.1:5005/profile/edit")
        time.sleep(2)
    upload_profile_banner_selector = driver.find_element(By.ID, "upload-profile-banner-button")
    if not upload_profile_banner_selector:
        return False
    return True

def test_profile_audio_selector_displays(driver, needs_rerouting=False):
    if needs_rerouting:
        driver.get("http://127.0.0.1:5005/profile/edit")
    time.sleep(2)
    upload_profile_audio_selector = driver.find_element(By.ID, "upload-profile-audio-button")
    if not upload_profile_audio_selector:
        return False
    return True

try:
    username = "newuser1"
    password = "1"
    if perform_login(driver, username, password):
        driver.get("http://127.0.0.1:5005/profile/newuser1")
        time.sleep(2)

        print("--= Beginning Tests =--")

        username_displays = test_username_displays()
        if username_displays:
            print("[PASSED] - Username displays.")
            passed += 1
        else:
            print("[FAILED] - Username not found.")
            failed += 1

        profile_image_displays = test_profile_image_displays()
        if profile_image_displays:
            print("[PASSED] - Profile image displays.")
            passed += 1
        else:
            print("[FAILED] - Profile image not found.")
            failed += 1

        profile_banner_displays = test_profile_banner_displays()
        if profile_banner_displays:
            print("[PASSED] - Profile banner displays.")
            passed += 1
        else:
            print("[FAILED] - Profile banner not found.")
            failed += 1

        profile_picture_updates = test_profile_picture_updates(driver=driver, needs_rerouting=True)
        if profile_picture_updates:
            print("[PASSED] - Profile image updated.")
            passed += 1
        else:
            print("[FAILED] - Profile image did not update.")
            failed += 1

        profile_bio_displays = test_profile_bio_displays(driver=driver, needs_rerouting=True)
        if profile_bio_displays:
            print("[PASSED] - Profile bio displays.")
            passed += 1
        else:
            print("[FAILED] - Profile bio not found.")
            failed += 1

        audio_player_displays = test_audio_player_displays(driver=driver, needs_rerouting=True)
        if audio_player_displays:
            print("[PASSED] - Audio player displays.")
            passed += 1
        else:
            print("[FAILED] - Audio player not found.")
            failed += 1

        bio_updates = test_profile_bio_updates(driver)
        if bio_updates:
            print("[PASSED] - Bio successfully updated.")
            passed += 1
        else:
            print("[FAILED] - Failed to update bio.")
            failed += 1
        
        profile_picture_selector_displays = test_profile_picture_selector_displays(driver=driver, needs_rerouting=True)
        if profile_picture_selector_displays:
            print("[PASSED] - Profile picture selector displays.")
            passed += 1
        else:
            print("[FAILED] - Profile picture selector not found.")
            failed += 1

        profile_banner_selector_displays = test_profile_banner_selector_displays(driver)
        if profile_banner_selector_displays:
            print("[PASSED] - Profile banner selector displays.")
            passed += 1
        else:
            print("[FAILED] - Profile banner selector found.")
            failed += 1

        profile_audio_selector_displays = test_profile_audio_selector_displays(driver)
        if profile_audio_selector_displays:
            print("[PASSED] - Profile audio selector displays.")
            passed += 1
        else:
            print("[FAILED] - Profile audio selector not found.")
            failed += 1
        

except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    print("--= Passed: "+str(passed)+" Failed: "+str(failed)+" =--")
    driver.quit()
