from gtts import gTTS
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import os
import time


class pywhtsapp:
    def __init__(self, path='/home/vaishnav/Developments/Python/whatsapp_automation/chromedriver'):
        global driver
        options = Options()
        options.add_argument(
            r"--user-data-dir=C:/home/vaishnav/.config/google-chrome/Profile 1")

        # options.add_argument("--headless") # To run in background

        driver = webdriver.Chrome(executable_path=path, chrome_options=options)

        # login section
        page_url = 'https://web.whatsapp.com/'
        driver.get(page_url)

    def pageLoadCheck(self, loc, _time=2):
        try:
            WebDriverWait(driver, _time).until(
                EC.presence_of_element_located((loc))
            )
            return True
        except KeyboardInterrupt:
            print("[ "+'\033[91m' + "FAILED" +
                  "\033[0m" + " ] Keyboard Interrupt ")
        except:
            return (self.pageLoadCheck(loc, 2.5))

    def usercheck(self, username):
        try:
            # selecting the username
            username_box = By.XPATH, "//div[@title='Search input textbox']"
            chkLoaded = self.pageLoadCheck(loc=username_box, _time=15)

            username_box = str(username_box)
            if chkLoaded:
                search_box = driver.find_elements(
                    By.XPATH, "//div[@title='Search input textbox']")
                search_box[0].send_keys(username)
                search_box[0].send_keys(Keys.ENTER)  # press ENTER
                return "[ "+'\033[92m' + "Ok" + "\033[0m" + " ] User Found"
        except:
            print("[ "+'\033[91m' + "FAILED" + "\033[0m" + " ] User Not Found")

    def send_message(self, text, user):
        # Sending Message
        try:
            msg_box = By.CLASS_NAME, "p3_M1"
            self.usercheck(username=user)
            loadCheck = self.pageLoadCheck(msg_box)
            if loadCheck:
                textbox = driver.find_elements(By.CLASS_NAME, "p3_M1")
                textbox[0].send_keys(text)
                textbox[0].send_keys(Keys.ENTER)  # press ENTER
                return "[ "+'\033[92m' + "OK" + "\033[0m" + " ] Message Send Successfully"
        except:
            print("[ "+'\033[91m' + "FAILED" +
                  "\033[0m" + " ] Messge send Failed")

    def send_attachment(self, _path, user):
        # Sending attachements video / audio / pdf
        try:
            Attach_button = By.XPATH, "//div[@title='Attach']"
            video_audio_img = By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']"
            file_send_button = By.XPATH, "//span[@data-icon='send']"
            self.usercheck(user)
            self.pageLoadCheck(Attach_button, 1)
            attach = driver.find_elements(By.XPATH, "//div[@title='Attach']")
            attach[0].click()
            self.pageLoadCheck(video_audio_img, 1)
            file_accept_box = driver.find_elements(
                By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']")
            file_accept_box[0].send_keys(_path)
            self.pageLoadCheck(file_send_button, 1)
            submit_button = driver.find_elements(
                By.XPATH, "//span[@data-icon='send']")
            submit_button[0].click()
            return "[ "+'\033[92m' + "OK" + "\033[0m" + " ] File Send Successfully"
        except:
            print("[ "+'\033[91m' + "FAILED" +
                  "\033[0m" + " ] File Send Failed")

    def text_to_audio(self, text, user):
        try:
            # Convert the text to audio and send to whatsapp
            time_class = datetime.now()
            date_time = time_class.strftime("%d-%m-%Y,%H:%M:%S")
            parent_directory = os.getcwd()
            path = os.path.join(parent_directory, "Sounds/")
            if not os.path.exists("Sounds"):
                os.mkdir(path)
            language = 'en'
            myobj = gTTS(text=text, lang=language, slow=False)
            myobj.save("%s.mp3" % os.path.join(path, str(date_time)))
            path_of_sound = path + date_time + ".mp3"
            self.send_attachment(path_of_sound, user)
        except:
            print("[ "+'\033[91m' + "FAILED" +
                  "\033[0m" + " ] Error converting to Audio ")

    def close(self, _time=10):
        print("[ "+'\033[92m' + "OK" + "\033[0m" +
              " ] The Browser will close in ", _time, " sec")
        time.sleep(_time)
        driver.close()
