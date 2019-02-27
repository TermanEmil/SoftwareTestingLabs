import unittest
from selenium import webdriver


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = "http://127.0.0.1:8000/"

    def test_login(self):
        driver = self.driver
        driver.get(self.base_url + "login/")

        driver.find_element_by_id("id_username").send_keys("victo")
        driver.find_element_by_id("id_password").send_keys("password")
        driver.find_element_by_class_name("submit-btn").click()

        assert 'login' not in self.get_relative_url()

    def get_relative_url(self):
        current_url = self.driver.current_url
        return current_url.replace(self.base_url, "")

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
