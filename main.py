from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from random import randint
from os.path import exists
from colorama import Fore
import random
import pandas as pd
import time
import undetected_chromedriver.v2 as uc

# columns_names=['Brand Name', 'Product Name', 'Category', 'VPN', 'UPC', 'Price', 'Qty', 'Description', 'Specification', 'Video URL', 'Image URL', 'Related Product URL']
# df = pd.DataFrame(columns=columns_names)
def copart():
    draw_banner()
    
    options = uc.ChromeOptions()

    # setting profile
    options.user_data_dir = "C:\\Users\\Sun\\AppData\\Local\\Google\\Chrome\\User Data"

    # another way to set profile is the below (which takes precedence if both variants are used
    options.add_argument('--user-data-dir=c:\\temp\\profile2')

    # just some options passing in to skip annoying popups
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')

    driver = uc.Chrome(options=options)
    driver.get("https://www.copart.com/login/")

    email = "588291"
    password = "Parol@12"
    email_field_xpath = "//div[@id='show']/div[1]/div[1]/input"
    pwd_field_xpath = "//div[@id='show']/div[2]/div[1]/input"
    remember_checkbox_xpath = "//div[@id='show']/div[3]/div[1]/input"
    sign_in_into_account_btn_xpath = "//div[@id='show']/div[4]/button"
    inventory_xpath = "//header[@id='top']/div[2]/div/div/nav/div/ul/li[4]/a"
    sales_list_xpath = "//header[@id='top']/div[2]/div/div/nav/div/ul/li[4]/ul/li[2]/a"
    auctions_xpath = "//header[@id='top']/div[2]/div/div/nav/div/ul/li[5]/a"
    join_auctions_xpath = "//header[@id='top']/div[2]/div/div/nav/div/ul/li[5]/ul/li[3]/a"
    join_bid_iframe_xpath = "//iframe[@id='iAuction5']"
    join_bid_btn_xpath = "//table[@class='arAuctiontable']/tbody[2]/tr[2]//button"

    auction = False
    
    try:
        time.sleep(10)
        email_field = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, email_field_xpath)))
        email_field.clear()
        email_field.send_keys(email)
        print("-------------->>> Email pass")
        
        time.sleep(5)
        pwd_field = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, pwd_field_xpath)))
        pwd_field.clear()
        pwd_field.send_keys(password)
        print("-------------->>> Password pass")
        
        time.sleep(6)
        sign_in_into_account_btn = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, sign_in_into_account_btn_xpath)))
        sign_in_into_account_btn.click()
        print("-------------->>> Sign in pass")
        
        time.sleep(20)
        sales_list = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, inventory_xpath)))
        sales_list.click()
        print("-------------->>> Inventory pass")
        
        time.sleep(5)
        sales_list = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, sales_list_xpath)))
        sales_list.click()
        print("-------------->>> Sales List pass")
        
        time.sleep(5)
        datetime_array = []
        rows = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//table[@id='clientSideDataTable']/tbody/tr")))
        print("-------------->>> Auctions Datetime")
        for idx, row in enumerate(rows):
            try:
                date_str = row.find_element_by_xpath("./td[6]/a").text
            except NoSuchElementException:
                continue
            time_str = row.find_element_by_xpath("./td[1]").text
            datetime_str = date_str + " " + time_str
            print(datetime_str)
            
            if date_str == "LIVE NOW":
                auction = True
            elif len(datetime_array) == 0:
                datetime_array.append(datetime_str)
            elif datetime_str != datetime_array[len(datetime_array) - 1]:
                datetime_array.append(datetime_str)
        print("-------------->>> Main Auctions Datetime")
        print(datetime_array)
        
        if auction:
            time.sleep(5)
            auctions = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, auctions_xpath)))
            auctions.click()
            print("-------------->>> Auctions pass")
            
            time.sleep(4)
            join_auctions = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, join_auctions_xpath)))
            join_auctions.click()
            print("-------------->>> Join Auctions pass")
            
            join_bid_iframe = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, join_bid_iframe_xpath)))
            driver.switch_to.frame(join_bid_iframe)
            
            time.sleep(10)
            join_bid_btn = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, join_bid_btn_xpath)))
            driver.execute_script("arguments[0].click();", join_bid_btn)
            print("-------------->>> Join Bid Button pass")
        
        else:
            print()
            
        time.sleep(40)
        print("==================== Waiting for the next stage ===================")

    except Exception as e:
        print("===================== Exception ====================")
        print(e)

    print("===================== Waiting for closing ====================")
    time.sleep(10)
    driver.close()

def draw_banner():
    print(
        Fore.LIGHTGREEN_EX
        + """
                      ____                       _
                     / ___|___  _ __   __ _ _ __| |_
                    | |   / _ \| '_ \ / _` | '__| __|
                    | |__| (_) | |_) | (_| | |  | |_
                     \____\___/| .__/ \__,_|_|   \__|
                               |_|

                        https://copart.com/career
        """
        + Fore.RESET
    )

if __name__ == "__main__":

    copart()
