# .\chrome.exe --remote-debugging-port=9898 --user-data-dir="C:\selenium\ChromeProfile"

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time
import re
import random

message = """Hello, I'm Sajith Madhubashana. How are you?"""

def attach_to_session(debugger_address):
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", debugger_address)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

debugger_address = "127.0.0.1:9898"
driver = attach_to_session(debugger_address)

def format_number(number):
    if number.startswith('+49'):
        # Germany: +49 XXX XXX XXXX
        formatted_number = re.sub(r'(\+\d{2})(\d{3})(\d{7})', r'\1 \2 \3', number)
    elif number.startswith('+61'):
        # Australia: +61 XXX XXX XXX
        formatted_number = re.sub(r'(\+\d{2})(\d{3})(\d{3})(\d{3})', r'\1 \2 \3 \4', number)
    elif number.startswith('+1'):
        # US: +1 XXX XXX XXXX
        formatted_number = re.sub(r'(\+\d{1})(\d{3})(\d{3})(\d{4})', r'\1 \2 \3 \4', number)
    elif number.startswith('+44'):
        # UK: +44 XXXX XXXXXX
        formatted_number = re.sub(r'(\+\d{2})(\d{4})(\d{6})', r'\1 \2 \3', number)
    else:
        # Default fall-back to original number if no known country code is found
        formatted_number = number

    return formatted_number
     
def send_message_to_number(number, message):
    formatted_number = format_number(number)
    try:
        chat_contact = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//span[@title="{formatted_number}"]'))
        )
        chat_contact.click()
        time.sleep(random.uniform(1,5))
        message_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@aria-placeholder="Type a message"]'))
        )
        message_box.click()
        time.sleep(random.uniform(1,5))
        message_box.send_keys(message + Keys.ENTER)
        # for char in message:
        #     message_box.send_keys(char)
        #     time.sleep(random.uniform(0.05, 0.2))
        # message_box.send_keys(Keys.ENTER)
        
        print(f"Message sent to {formatted_number}")
    except Exception as e:
        print(f"Error sending message to {formatted_number}: {e}")


def click_cancel_search():
    try:
        cancel_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Cancel search"]'))
        )
        cancel_button.click()
    except Exception as e:
        print(f"Error clicking cancel search button")
        
def check_number(number):
    try:
        new_chat_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@title="New chat"]'))
        )
        new_chat_button.click()
        search_box = WebDriverWait(driver, 10).until(
             EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]'))
        )
        time.sleep(random.uniform(1,5))
        search_box.send_keys(number)
        # for char in number:
        #     search_box.send_keys(char)
        #     # Sleep a random short duration to simulate typing
        #     time.sleep(random.uniform(0.05, 0.2))
        time.sleep(random.uniform(1,5))

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, f'//span[contains(text(), "No results found for \'{number}\'")]'))
            )
            return False
        except:
            
            send_message_to_number(number, message)
        return True

    except Exception as e:
        print(f"Error checking number {number}")
        return False

with open('list.txt', 'r') as file:
    numbers_to_check = [line.strip() for line in file if line.strip()]

for number in numbers_to_check:
    results = check_number(number)
    if(results):
        print(f"{number}")
    else:
        click_cancel_search()
    # click_cancel_search()
    time.sleep(random.uniform(1,5))
