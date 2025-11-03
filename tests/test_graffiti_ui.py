# tests/test_graffiti_ui.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE = "http://127.0.0.1:5005"
PROFILE_URL = f"{BASE}/profile/r"
DUMP_PATH = "tests/_last_page.html"

def p(ok, msg):
    print(f"[{'PASSED' if ok else 'FAILED'}] - {msg}")

def find(wait, by, sel, label):
    try:
        wait.until(EC.presence_of_element_located((by, sel)))
        p(True, f"{label} exists.")
        return True
    except Exception:
        p(False, f"{label} not found.")
        return False

def try_login(driver, wait):
    # If a login form is present, try credentials.
    page = driver.page_source.lower()
    if ("login" in page) and ("password" in page):
        try:
            # common inputs
            user = driver.find_element(By.CSS_SELECTOR, "input[name='username'], input#username")
            pw   = driver.find_element(By.CSS_SELECTOR, "input[name='password'], input#password")
        except Exception:
            return False

        for creds in [("r","r"), ("Jeff","Gumby"), ("jeff","gumby")]:
            try:
                user.clear(); pw.clear()
                user.send_keys(creds[0]); pw.send_keys(creds[1])
                # submit
                btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
                btn.click()
                # wait a moment for nav to settle
                wait.until(lambda d: "/login" not in d.current_url.lower())
                return True
            except Exception:
                # try next pair
                continue
    return True  # no login form detected; assume already allowed

def dump(driver):
    try:
        with open(DUMP_PATH, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"[info] Wrote page HTML to {DUMP_PATH}")
    except Exception:
        pass

def main():
    print("--= Beginning Tests =--")
    print("--- Graffiti Mode (YouFace) ---")

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=opts)

    try:
        driver.set_window_size(1280, 1000)
        wait = WebDriverWait(driver, 10)

        # Hit base, login if needed
        driver.get(BASE)
        try_login(driver, wait)

        # Go to profile
        driver.get(PROFILE_URL)
        wait.until(lambda d: "TrollR" in (d.title or ""))

        p("TrollR" in (driver.title or ""), f"Page title: {driver.title or '(empty)'}")
        has_copy = "Graffiti Mode" in driver.page_source
        p(has_copy, "Page source contained 'Graffiti Mode'.")

        # Look for elements
        ok_all = True
        ok_all &= find(wait, By.ID, "c", "Graffiti canvas")
        ok_all &= find(wait, By.ID, "toggle", "Graffiti toggle")
        ok_all &= find(wait, By.ID, "push", "Push button")
        ok_all &= find(wait, By.ID, "clear", "Clear button")
        ok_all &= find(wait, By.ID, "pen", "Pen button")
        ok_all &= find(wait, By.ID, "eraser", "Eraser button")
        ok_all &= find(wait, By.ID, "color", "Color picker")
        ok_all &= find(wait, By.ID, "size", "Size slider/number")

        # Toggle try
        try:
            driver.find_element(By.ID, "toggle").click()
            p(True, "Toggle click worked (ON).")
            driver.find_element(By.ID, "toggle").click()
            p(True, "Toggle click worked (OFF).")
        except Exception:
            p(False, "Toggle click failed.")

        if not has_copy or not ok_all:
            dump(driver)

    finally:
        print("--= Ending Tests =--")
        driver.quit()

if __name__ == "__main__":
    main()
