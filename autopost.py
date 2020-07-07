from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
import pickle
import time
from pyvirtualdisplay import Display

class AutoPostBot:

    def __init__(self, pagelink):
        self.display = Display(visible=0, size=(800,600))
        self.display.start()
        self.driver = Firefox(executable_path='/home/friend/TF2alertbot/geckodriver')
        self.driver.get('https://mbasic.facebook.com')
        self.cookies = pickle.load(open("cookies.pl", "rb"))
        for cookie in self.cookies:
            self.driver.add_cookie(cookie)
        self.driver.get(pagelink)

    def post_image(self, file_path, message):
        time.sleep(1)
        self.driver.find_element_by_name('view_photo').click()
        self.driver.find_element_by_name('file1').send_keys(file_path)
        self.driver.find_element_by_name('add_photo_done').click()
        time.sleep(1)
        for msg in message:
            self.driver.find_element_by_name(
                'xc_message').send_keys(msg, Keys.ENTER)
        self.driver.find_element_by_name('view_post').click()
        self.driver.quit()
        self.display.stop()
