from gtts import gTTS
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import os


class pywhtsapp:
    def __init__(self, path='/home/vaishnav/chromedriver'):
        global driver
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        # path = '/home/vaishnav/chromedriver'

        service = ChromeService(executable_path=path)
        driver = webdriver.Chrome(service=service, options=options)

        # login section
        page_url = 'https://web.whatsapp.com/'
        driver.get(page_url)

    def pageLoadCheck(self, loc, _time = 2):
        try:
            WebDriverWait(driver, _time).until(
                EC.presence_of_element_located((loc))
            )
            return True
        except:
            return (self.pageLoadCheck(loc, 2.5))

    def usercheck(self, username):
        # selecting the username
        # The username input box
        username_box = By.XPATH, "//div[@title='Search input textbox']"
        chkLoaded = self.pageLoadCheck(loc=username_box, _time=15)
        username_box = str(username_box)
        if chkLoaded:
            search_box = driver.find_elements(By.XPATH, "//div[@title='Search input textbox']")
            search_box[0].send_keys(username)
            search_box[0].send_keys(Keys.ENTER)  # press ENTER

    def send_message(self, msg, user):
        msg_box = By.CLASS_NAME, "p3_M1"
        self.usercheck(username=user)
        loadCheck =self.pageLoadCheck(msg_box)
        if loadCheck:
            textbox = driver.find_elements(By.CLASS_NAME, "p3_M1")
            textbox[0].send_keys(msg)
            textbox[0].send_keys(Keys.ENTER)  # press ENTER
            return "Message send Successfully"

    def send_attachment(self, file_path, username):
        Attach_button = By.XPATH, "//div[@title='Attach']"
        video_audio_img = By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']"
        file_send_button = By.XPATH, "//span[@data-icon='send']"
        
        self.usercheck(username=username)
        self.pageLoadCheck(Attach_button, 1)
        attach = driver.find_elements(Attach_button)
        attach[0].click()
        self.pageLoadCheck(video_audio_img, 1)
        file_accept_box = driver.find_elements(video_audio_img)
        file_accept_box[0].send_keys(file_path)
        self.pageLoadCheck(file_send_button, 1)
        submit_button = driver.find_elements(file_send_button)
        submit_button[0].click()
        return "Attchment sene successfully"

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
        myobj = gTTS(text=text, lang=language, slow=False)
        print(date_time)
        myobj.save("%s.mp3" % os.path.join(path, str(date_time)))
        path_of_sound = path + date_time + ".mp3"
        self.send_attachment(path_of_sound, username)

    def close(self):
        driver.close()
