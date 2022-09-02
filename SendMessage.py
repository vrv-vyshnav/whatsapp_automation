from gtts import gTTS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
path = '/home/vaishnav/chromedriver'
service = ChromeService(executable_path=path)
driver = webdriver.Chrome(service=service, options=options)


def sendMessage():
    while True:
        textbox = driver.find_elements(By.CLASS_NAME, "p3_M1")
        # Adding text to the text field
        msg = input("Enter the message: ")
        textbox[0].send_keys(msg)
        textbox[0].send_keys(Keys.ENTER)  # press ENTER
        print("\t Message send successfully")
        again = input("Do you want to send more message 1/0: ")
        if again == '0':
            break


def sendAttachments(filepath=None):

    if filepath == None:
        filepath = input("  Enter the file path: ")
    attach = driver.find_elements(By.XPATH, "//div[@title='Attach']")
    attach[0].click()
    file_accept_box = driver.find_elements(
        By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']")
    file_accept_box[0].send_keys(filepath)
    time.sleep(3)
    submit_button = driver.find_elements(
        By.XPATH, "//span[@data-icon='send']")
    submit_button[0].click()
    print("\t Attachment send successfully")


def making_text_to_audio():
    while True:
        mytext = input("  Enter the text: ")
        language = 'en'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("message.mp3")
        # os.system("message.mp3") to play the music
        sendAttachments(
            filepath="/home/vaishnav/developments/Python/selenium/message.mp3")
        again = input("Do you want to continue 1/0: ")
        if again == '0':
            break


def usercheck():
    # selecting the username
    username = input("Enter the name / number / group: ")
    # username = "vaishnav"
    search_box = driver.find_elements(
        By.XPATH, "//div[@title='Search input textbox']")
    search_box[0].send_keys(username)
    search_box[0].send_keys(Keys.ENTER)  # press ENTER
    print("username match")


# login section
page_url = 'https://web.whatsapp.com/'
driver.get(page_url)
input("")  # press enter after scanning the QR code
print("Loginned successfully")


while True:
    print("""
          1. send text message
          2. send attachments
          3. send audio message
          4. change user
          5 exit
          """)
    choice = input("Enter your choice: ")
    if choice == '1':
        sendMessage()
    elif choice == '2':
        sendAttachments()
    elif choice == '3':
        making_text_to_audio()
    elif choice == '4':
        usercheck()
    else:
        break

driver.close()
