import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

class TestYouface(unittest.TestCase):

    def test_verify_token(self):
        from youface import verify_token
        token = "wrong"
        self.assertFalse(verify_token(token), "Does not properly flag when "
                "given invalid token.")

    def test_login_fails_with_invalid_token(self):
        # Hook up driver to browser
        driver = webdriver.Chrome(executable_path="./chromedriver")
        # Pull web page
        driver.get("http://localhost:5000")

        userinput = driver.find_element_by_name('username')
        userinput.send_keys("ren")

        passinput = driver.find_element_by_name('password')
        passinput.send_keys("ren")

        # find 2fa box
        try:
            twofa = driver.find_element_by_name('2fa')
        except NoSuchElementException:
            self.fail("The 2fa input box is missing.")
        wrong_token = "wrong"
        twofa.send_keys(wrong_token)

        login = driver.find_element_by_id("login-button")
        login.click()

        alerts = driver.find_elements_by_class_name("alert")
        self.assertEqual(len(alerts), 1, "You did not have the right number of alerts")
        self.assertIn("Invalid token: " + wrong_token, alerts[0].text, "Alert text not correct.")


        # Close driver
        driver.close()


if __name__ == "__main__":
    unittest.main()
