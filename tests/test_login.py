import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser_choice = os.getenv("UI_TEST_BROWSER", "chrome").lower()
opera_binary = os.getenv("OPERA_GX_BINARY")

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

if browser_choice == "opera":
    if not opera_binary:
        raise RuntimeError("Set OPERA_GX_BINARY to the Opera GX executable when UI_TEST_BROWSER=opera.")
    options.binary_location = opera_binary
    print(f"Launching Opera GX via ChromeDriver using binary: {opera_binary}")
else:
    print("Launching Chrome via ChromeDriver (default).")

driver = webdriver.Chrome(options=options)

test_count = 0
tests_passed = 0

def delete_account(username, password):
    driver.get("http://localhost:5005/loginscreen")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    username_field.clear()
    password_field.clear()
    username_field.send_keys(username)
    password_field.send_keys(password)
    delete_account_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Delete']")
    delete_account_button.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )

def dashboard_to_login():
    print(driver.current_url)
    print("on step 1 of return login")
    logout_button = None
    logout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "form[action='/logout'] button[type='submit']"))
    )
    print(logout_button)
    print("on step 2 of return login")
    logout_button.click()
    print("on step 3 of return login")
    print(driver.current_url)
    if "loginscreen" in driver.current_url or "login" in driver.current_url:
        print("[INFO] - Returned to login screen after logout.")

try:
    driver.get("http://localhost:5005/loginscreen")
    time.sleep(2)
    
    print("--= Beginning Tests =--")
    
    # Test: Verify that the login button exists
    test_count += 1
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")
    if login_button:
        print("[PASSED] - Login button exists.")
        tests_passed += 1
    else:
        print("[FAILED] - Login button not found")
        
    # Test: Verify that the create account button exists
    test_count += 1
    create_account_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create']")
    if create_account_button:
        print("[PASSED] - Create Account button exists.")
        tests_passed += 1
    else:
        print("[FAILED] - Create Account button not found")
    
    # Test: Verify that the username and password input fields exist
    test_count += 1
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    if username_field and password_field:
        print("[PASSED] - Username and Password input fields exist.")
        tests_passed += 1
    else:
        print("[FAILED] - Username and/or Password input fields not found.")
        
    # Test: Verify that a user can enter text into the username and password fields
    test_count += 2
    test_username_input = "test_user"
    test_password_input = "test_login"
    username_field.send_keys(test_username_input)
    password_field.send_keys(test_password_input)
    if username_field.get_attribute("value") == test_username_input:
        print("[PASSED] - Username input field accepts text.")
        tests_passed += 1
    else:
        print("[FAILED] - Username input field does not accept text.")
    if password_field.get_attribute("value") == test_password_input:
        print("[PASSED] - Password input field accepts text.")
        tests_passed += 1
    else:
        print("[FAILED] - Password input field does not accept text.")
        
    # Test: Verify that a user cannot see the password in plain text
    test_count += 1
    if password_field.get_attribute("type") == "password":
        print("[PASSED] - Password input field masks the input.")
        tests_passed += 1
    else:
        print("[FAILED] - Password input field does not mask the input.")
        
    # Test: Verify that a user can login with valid credentials
    test_count += 1
    login_button.click()
    WebDriverWait(driver, 10).until(lambda d: "loginscreen" not in d.current_url)
    if "loginscreen" not in driver.current_url:
        print("[PASSED] - User can login with valid credentials.")
        tests_passed += 1
    else:
        print("[FAILED] - User cannot login with valid credentials.")
            
    # Return to login screen
    dashboard_to_login()
        
    # Test: Verify that a user cannot login with invalid credentials
    test_count += 1
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    username_field.clear()
    password_field.clear()
    username_field.send_keys("invalid_user")
    password_field.send_keys("wrong_password")
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")
    login_button.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    if "loginscreen" in driver.current_url or "login" in driver.current_url:
        print("[PASSED] - User cannot login with invalid credentials.")
        tests_passed += 1
    else:
        print("[FAILED] - User logged in with invalid credentials.")
    
    # Test: Verify that a user can create a new account
    test_count += 1
    delete_account("new_user", "new_password")
    print("[INFO] - Ensured 'new_user' does not exist before account creation test.")
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    username_field.clear()
    password_field.clear()
    new_username = "new_user"
    new_password = "new_password"
    username_field.send_keys(new_username)
    password_field.send_keys(new_password)
    create_account_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create']")
    create_account_button.click()
    print(driver.current_url)
    WebDriverWait(driver, 10).until(lambda d: "login" not in d.current_url)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.row h1"))
    )
    flash_messages = driver.find_elements(By.CSS_SELECTOR, "div.alert-success")
    account_created = any('created successfully' in msg.text for msg in flash_messages)
    if account_created:
        print("[PASSED] - User can create a new account.")
        tests_passed += 1
    else:
        print("[FAILED] - User cannot create a new account.")
        
    # Return to login screen
    dashboard_to_login()
        
    # Delete the newly created account to clean up
    delete_account(new_username, new_password)
    print("[INFO] - Deleted the newly created account to clean up.")
        
    # Summary of test results
    print(f"--= Ending Tests =--\nResults: {tests_passed} tests passed out of {test_count} total tests.")
        
except Exception as e:
    print(f"[ERROR] - An exception occurred during testing: {e}")
    
