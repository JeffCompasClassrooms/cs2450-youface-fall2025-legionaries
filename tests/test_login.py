import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

browser_choice = os.getenv("UI_TEST_BROWSER", "chrome").lower()
opera_binary = os.getenv("OPERA_GX_BINARY")

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

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
    test_password_input = "test_password"
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
    time.sleep(2)
    if "dashboard" in driver.current_url:
        print("[PASSED] - User can login with valid credentials.")
        tests_passed += 1
    else:
        print("[FAILED] - User cannot login with valid credentials.")
        
        
    
    
    print(f"--= Ending Tests =--\nResults: {tests_passed} tests passed out of {test_count} total tests.")
        
except Exception as e:
    print("Error:", e)
    
