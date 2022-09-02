from gtts import gTTS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import os
import time


class pywappbot:
    def __init__(self):
        global driver
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        path = '/home/vaishnav/chromedriver'

        service = ChromeService(executable_path=path)
        driver = webdriver.Chrome(service=service, options=options)

        # login section
        page_url = 'https://web.whatsapp.com/'
        driver.get(page_url)
        input("Press enter")

    def usercheck(self, username):
        # selecting the username
        search_box = driver.find_elements(
            By.XPATH, "//div[@title='Search input textbox']")
        search_box[0].send_keys(username)
        search_box[0].send_keys(Keys.ENTER)  # press ENTER
        print("username match")

    def send_message(self, msg, user):
        self.user = user
        self.msg = msg
        self.usercheck(username=user)
        textbox = driver.find_elements(By.CLASS_NAME, "p3_M1")
        textbox[0].send_keys(msg)
        textbox[0].send_keys(Keys.ENTER)  # press ENTER
        print("Message send successfully")

    def send_attachment(self, file_path, username):
        self.username = username
        self.file_path = file_path
        self.usercheck(username=username)
        attach = driver.find_elements(By.XPATH, "//div[@title='Attach']")
        attach[0].click()
        file_accept_box = driver.find_elements(
            By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']")
        file_accept_box[0].send_keys(file_path)
        time.sleep(3)
        submit_button = driver.find_elements(
            By.XPATH, "//span[@data-icon='send']")
        submit_button[0].click()

    def text_to_audio(self, text, username):
        self.text = text
        self.username = username
        time_class = datetime.now()
        date_time = time_class.strftime("%d-%m-%Y,%H:%M:%S")
        parent_directory = os.getcwd()
        path = os.path.join(parent_directory, "Sounds")
        if not os.path.exists("Sounds"):
            os.mkdir(path)
        language = 'en'
        myobj = gTTS(text="hello world", lang=language, slow=False)
        print(date_time)
        myobj.save("%s.mp3" % os.path.join(path, str(date_time)))
        path_of_sound = path + date_time + ".mp3"
        self.send_attachment(path_of_sound, username)

    def close(self):
        driver.close()
