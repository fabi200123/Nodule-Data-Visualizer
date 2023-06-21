# dash_test.py

import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

class MyE2ETests(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(executable_path=r'C:/Users/fabi2/Downloads/chromedriver_win32/chromedriver') # Provide path to your ChromeDriver here
        self.browser.get('http://192.168.101.31:3000/visualize?cnp=3456789989951')

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

    def test_app_title(self):
        WebDriverWait(self.browser, 20).until(EC.title_is("Dash"))

    def test_dropdown_options_and_graphs(self):
        dropdown = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.ID, "feature-dropdown")))
        dropdown.click()  # open the dropdown
        time.sleep(2)  # wait a bit for the dropdown to open

        # Select the option by its text
        option = self.browser.find_element(By.XPATH, "//div[@id='feature-dropdown']//div[contains(text(), 'Nodule Volume')]")
        option.click()

        # Check that graphs are loaded properly
        graph = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.ID, "graph-with-selector")))
        self.assertIsNotNone(graph)

    def test_folder_selector_and_graphs(self):
        folder_selector = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.ID, "folder-selector")))
        folder_selector.click()  # open the folder selector
        time.sleep(2)  # wait a bit for the folder selector to open

        # Select the option by its text
        option = self.browser.find_element(By.XPATH, "//div[@id='folder-selector']//div[contains(text(), '1672277350373_1-1')]")
        option.click()

        # Check that graphs are loaded properly
        graph = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.ID, "graph-with-selector")))
        self.assertIsNotNone(graph)

    def test_png_viewer(self):
        png_viewer = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.ID, "png-viewer")))
        self.assertIsNotNone(png_viewer)
