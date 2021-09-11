from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver.v2 as uc
from random import randint
from os.path import exists
from colorama import Fore
from datetime import datetime
import pandas as pd
import time
import re

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
    auctions_xpath = "//header[@id='top']/div[2]/div/div/nav/div/ul/li[5]/a"
    join_auctions_xpath = "//header[@id='top']/div[2]/div/div/nav/div/ul/li[5]/ul/li[3]/a"
    join_bid_iframe_xpath = "//iframe[@id='iAuction5']"
    no_live_auctions_xpath = "//table[@class='arAuctiontable']/tbody[2]/tr[2]"
    no_upcoming_auctions_xpath = "//table[@class='arAuctiontable']/tbody[2]/tr[4]/td/div"
    inventory_xpath = "//header[@id='top']/div[2]/div/div/nav/div/ul/li[4]/a"
    sales_list_xpath = "//header[@id='top']/div[2]/div/div/nav/div/ul/li[4]/ul/li[2]/a"
    list_xpath = "//table[@id='clientSideDataTable']/tbody/tr"
    waiting_time_xpath = "//table[@class='arAuctiontable']/tbody[2]/tr[4]/td/later-auction-row/div/div/div[3]/div/div[2]/strong"
    join_bid_btn_xpath = "//table[@class='arAuctiontable']/tbody[2]/tr[2]//button"
    search_btn_xpath = "//div[@class='row vehicle-finder-search']/div/button"
    search_list_xpath = "//div[@id='serverSideDataTable_wrapper']/table/tbody/tr"
    join_now_btn_xpath = "//div[@class='button-div ng-star-inserted']/button"
    price_xpath = "//div[@class='contentscrolldiv-MACRO']"
    vin_xpath = "//a[@class='titlelbl ellipsis']"
    auction_ended_xpath = '/html/body/div[2]/root/app-root/div/widget-area/div[2]/div[3]/div/gridster/gridster-item/widget/div/div/div/div[1]'
    
    auction = False
    auction_result = []
    
    try:
        time.sleep(10)
        email_field = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, email_field_xpath)))
        email_field.clear()
        email_field.send_keys(email)
    except:
        print("-------------->>> Email field doesn't exist")
        pass
    print("-------------->>> Email pass")
    
    try:
        time.sleep(5)
        pwd_field = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, pwd_field_xpath)))
        pwd_field.clear()
        pwd_field.send_keys(password)
    except:
        print("-------------->>> Password field doesn't exist")
        pass
    print("-------------->>> Password pass")
    
    try:
        time.sleep(6)
        sign_in_into_account_btn = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, sign_in_into_account_btn_xpath)))
        sign_in_into_account_btn.click()
    except:
        print("-------------->>> Account Login button doesn't exist")
        pass
    print("-------------->>> Sign in pass")
    
    time.sleep(20)
    while True:
        try:
            auctions = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, auctions_xpath)))
            auctions.click()
        except:
            pass
        print("-------------->>> Auctions pass")
        
        try:
            time.sleep(4)
            join_auctions = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, join_auctions_xpath)))
            join_auctions.click()
        except:
            print("-------------->>> Join Auctions Option isn't selected")
            pass
        print("-------------->>> Join Auctions pass")
        
        try:
            join_bid_iframe = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, join_bid_iframe_xpath)))
            driver.switch_to.frame(join_bid_iframe)
        except:
            print("-------------->>> Can't find iframe for join bid")
            pass
        print("-------------->>> iframe pass")
        
        try:
            time.sleep(15)
            no_live_auctions = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, no_live_auctions_xpath))).text
            if "No Live Auctions" in no_live_auctions:
                no_upcoming_auctions = ''
                try:
                    no_upcoming_auctions = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, no_upcoming_auctions_xpath))).text
                except:
                    print("Can't find 'No Upcoming Actions' Text")
                    pass
                
                if "No Upcoming Auctions" in no_upcoming_auctions:
                    print("-------------->>> 'No Upcoming Auctions' exists")
                    driver.switch_to.default_content()
                    try:
                        time.sleep(3)
                        inventory = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, inventory_xpath)))
                        inventory.click()
                    except:
                        print("-------------->>> Inventory isn't selected")
                        pass
                    print("-------------->>> Inventory pass")
                    
                    try:
                        time.sleep(2)
                        sales_list = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, sales_list_xpath)))
                        sales_list.click()
                    except:
                        print("-------------->>> Sales List isn't selected")
                        pass
                    print("-------------->>> Sales List pass")
                    
                    datetime_list = []
                    try:
                        time.sleep(4)
                        print('-------------->>> Datetime list')
                        list = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, list_xpath)))
                        for idx in range(len(list)):
                            date_str = list[idx].find_element_by_xpath('./td[6]').text
                            time_str = list[idx].find_element_by_xpath('./td[1]').text
                            datetime_str = date_str + " " + time_str
                            print(datetime_str)
                            if date_str != '' and (idx == 0 or (idx > 0 and datetime_list[-1] != datetime_str)):
                                datetime_list.append(datetime_str)
                    except:
                        print("-------------->>> Can't find List")
                        pass
                    print('-------------->>> Main Datetime List\n', datetime_list)
                    
                    time.sleep(60)
                    break
                else:
                    print("-------------->>> 'No Upcoming Auctions' doesn't exist")
                    try:
                        waiting_time = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, waiting_time_xpath))).text
                        nums = [int(s) for s in re.findall(r'\b\d+\b', waiting_time)]
                        seconds = nums[0] * 3600 + nums[1] * 60
                        print(f"-------------->>> Auction hasn't started yet. Sleeping for {seconds}seconds")
                        time.sleep(seconds)
                    except:
                        print("-------------->>> Can't find waiting time text")
                        pass                
        except:
            print("-------------->>> Can't find join bid text")
            pass

        try:
            time.sleep(3)
            join_bid_btn = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, join_bid_btn_xpath)))
            driver.execute_script("arguments[0].click();", join_bid_btn)
        except NoSuchElementException:
            print("-------------->>> Join bid button doesn't exist")
            pass
        print("-------------->>> Join Bid Button pass")
        
        try:
            time.sleep(2)
            join_now_btn = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, join_now_btn_xpath)))
            driver.execute_script("arguments[0].click();", join_now_btn)
        except NoSuchElementException:
            print("-------------->>> Join now button doesn't exist")
            pass
        print("-------------->>> Join now button pass")

        data = ''
        vin_change = []
        while 1:
            try:
                print('svg start')
                price = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'svg')))
                price_txt = [price[idx].text for idx in range(len(price))]
                print('svg ok')
                print(len(price))
                print(price_txt)
            except NoSuchElementException:
                print("-------------->>> Can't find svg")
                try:
                    print('Div start instead of svg')
                    price = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, price_xpath)))
                    price_txt = [price[idx].text for idx in range(len(price))]
                    print('Div ok instead of svg')
                    print(len(price))
                    print(price_txt)
                except:
                    print("-------------->>> Can't price description")
                    pass
            except:
                print("-------------->>> svg exception")
                pass
            print('Price End')
            
            try:
                print('vin start')
                vin = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, vin_xpath)))
                vin_txt = [vin[idx].text for idx in range(len(vin))]
                print('vin ok')
                print(len(vin))
                print(vin_txt)
            except NoSuchElementException:
                print("Can't find vin")
                pass
            print('vin End')
            
            time.sleep(60)
            break
            # if not price or vin:
            #     print('No price or vin')
            #     break
            # if vin_change == []:
            #     print('vin change is no')
            #     vin_change = 
            # elif vin_change == vin_txt1:
            #     print('vin change is the same')
            #     data = svg_txt1
            # elif vin_change != vin_txt1:
            #     print('vin change is not the same')
            #     auction_result.append({'vin': vin_change, 'auction': data})
            #     vin_change = vin_txt1
            #     print(auction_result)
        print('auction is end')
        time.sleep(3)
        break
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