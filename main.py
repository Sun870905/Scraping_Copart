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
options = uc.ChromeOptions()
# setting profile
options.user_data_dir = "C:\\Users\\Sun\\AppData\\Local\\Google\\Chrome\\User Data"
# another way to set profile is the below (which takes precedence if both variants are used
options.add_argument('--user-data-dir=c:\\temp\\profile2')
# just some options passing in to skip annoying popups
options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
driver = uc.Chrome(options=options)

email = "588291"
password = "Parol@12"
sign_in_btn_xpath = "//a[@data-uname='homePageSignIn']"
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
link_for_search_list_xpath = "//table[@id='clientSideDataTable']/tbody/tr[1]/td[6]/a"
search_btn_xpath = "//div[@class='row vehicle-finder-search']/div/button"
search_list_xpath = "//div[@id='serverSideDataTable_wrapper']/table/tbody/tr"
waiting_time_xpath = "//span[@data-uname='lotdetailSaleinformationtimeleftvalue']"
waiting_time_in_iframe_xpath = "//table[@class='arAuctiontable']/tbody[2]/tr[4]/td/later-auction-row/div/div/div[3]/div/div[2]/strong"
join_bid_btn_xpath = "//table[@class='arAuctiontable']/tbody[2]/tr[2]//button"
join_now_btn_xpath = "//div[@class='button-div ng-star-inserted']/button"
price_xpath = "//div[@class='contentscrolldiv-MACRO']"
vin_xpath = "//a[@class='titlelbl ellipsis']"
auction_ended_xpath = '/html/body/div[2]/root/app-root/div/widget-area/div[2]/div[3]/div/gridster/gridster-item/widget/div/div/div/div[1]'

auction_result = []

def copart():
    while True:
        driver.get("https://www.copart.com/login/")
        print('-------------->>> Start :)')
        if sign_in_check():
            sign_in()
    
        try:
            time.sleep(15)
            auctions = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, auctions_xpath)))
            auctions.click()
            print("-------------->>> Auctions pass")
        except:
            print("-------------->>> Can't find Auctions")
            pass
        
        try:
            time.sleep(4)
            join_auctions = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, join_auctions_xpath)))
            join_auctions.click()
            print("-------------->>> Join Auctions pass")
        except:
            print("-------------->>> Join Auctions Option isn't selected")
            pass
        
        try:
            time.sleep(5)
            join_bid_iframe = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, join_bid_iframe_xpath)))
            driver.switch_to.frame(join_bid_iframe)
            print("-------------->>> iframe pass")
        except:
            print("-------------->>> Can't find iframe for join bid")
            pass
        
        try:
            time.sleep(3)
            no_live_auctions = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, no_live_auctions_xpath))).text
            if "No Live Auctions" in no_live_auctions:
                no_upcoming_auctions = ''
                try:
                    no_upcoming_auctions = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, no_upcoming_auctions_xpath))).text
                except:
                    print("-------------->>> Can't find 'No Upcoming Actions' Text")
                    pass
                
                if "No Upcoming Auctions" in no_upcoming_auctions:
                    no_upcoming()
                    continue
                else:
                    upcoming()
                    if sign_in_check():
                        continue
        except:
            print("-------------->>> Can't find 'No Live Auctions' text")
            pass

        try:
            time.sleep(3)
            join_bid_btn = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, join_bid_btn_xpath)))
            driver.execute_script("arguments[0].click();", join_bid_btn)
            print("-------------->>> Join Bid Button pass")
        except NoSuchElementException:
            print("-------------->>> Join bid button doesn't exist")
            pass
        
        try:
            time.sleep(2)
            join_now_btn = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, join_now_btn_xpath)))
            driver.execute_script("arguments[0].click();", join_now_btn)
            print("-------------->>> Join now button pass")
        except NoSuchElementException:
            print("-------------->>> Join now button doesn't exist")
            pass
        
        auctions_record()
        end = False
        if end: break
    print('-------------->>> Closing <<<--------------')
    time.sleep(10)
    driver.close()

def sign_in_check():
    try:
        time.sleep(2)
        sign_in_btn = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, sign_in_btn_xpath)))
        if "Sign In" in sign_in_btn.text:
            print('-------------->>> You have to sign in')
            return True
    except:
        print("-------------->>> Can't find Sign In button")
        pass
    print("-------------->>> You don't need to sign in")
    return False

def sign_in():
    try:
        time.sleep(10)
        email_field = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, email_field_xpath)))
        email_field.clear()
        email_field.send_keys(email)
        print("-------------->>> Email pass")
    except:
        print("-------------->>> Email field doesn't exist")
        pass
    
    try:
        time.sleep(5)
        pwd_field = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, pwd_field_xpath)))
        pwd_field.clear()
        pwd_field.send_keys(password)
        print("-------------->>> Password pass")
    except:
        print("-------------->>> Password field doesn't exist")
        pass
    
    try:
        time.sleep(6)
        sign_in_into_account_btn = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, sign_in_into_account_btn_xpath)))
        sign_in_into_account_btn.click()
        print("-------------->>> Sign in pass")
    except:
        print("-------------->>> Account Login button doesn't exist")
        pass

def no_upcoming():
    print("-------------->>> 'No Upcoming Auctions' exists")
    driver.switch_to.default_content()
    try:
        time.sleep(3)
        inventory = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, inventory_xpath)))
        inventory.click()
        print("-------------->>> Inventory pass")
    except:
        print("-------------->>> Can't find Inventory")
        pass
    
    try:
        time.sleep(2)
        sales_list = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, sales_list_xpath)))
        sales_list.click()
        print("-------------->>> Sales List pass")
    except:
        print("-------------->>> Can't find Sales List")
        pass
    
    datetime_list = []
    seconds_list = []
    try:
        time.sleep(4)
        print('-------------->>> Datetime list')
        list = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, list_xpath)))
        for idx in range(len(list)):
            date_str = list[idx].find_element_by_xpath('./td[6]').text
            time_str = list[idx].find_element_by_xpath('./td[1]').text
            datetime_str = date_str + " " + time_str
            
            if date_str != '':
                format_date = datetime_str[0:datetime_str.index('M')+1]
                date_object = datetime.strptime(format_date, "%m/%d/%Y %I:%M %p")
                now = datetime.now()
                total_seconds = (date_object - now).total_seconds()
                print('Extract-->', datetime_str, 'Convert-->', date_object, 'Now-->', now, 'Waiting_seconds-->', total_seconds)
                if idx == 0 or (idx > 0 and datetime_list[-1] != date_object and total_seconds >= 0):
                    datetime_list.append(date_object)
                    seconds_list.append(total_seconds)
    except:
        print("-------------->>> Can't find Sales List")
        pass
    print('-------------->>> Main Auctions Datetime List:\n', datetime_list)
    print('-------------->>> Main Waiting Seconds List:\n', seconds_list)
    
    try:
        time.sleep(2)
        link_for_search_list = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, link_for_search_list_xpath)))
        link_for_search_list.click()
        print("-------------->>> Link For Search List pass")
        
        try:
            time.sleep(4)
            search_btn = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, search_btn_xpath)))
            search_btn.click()
            print("-------------->>> Search Button pass")
            
            try:
                time.sleep(5)
                index = -1
                print('-------------->>> Sale Date:')
                for idx in range(20):
                    sale_date = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, f"{search_list_xpath}[{(idx+1)}]/td[9]/span"))).text
                    sale_date = sale_date.split('\n')[0]+" "+sale_date.split('\n')[1]
                    print(sale_date)
                    
                    sale_date = sale_date[:sale_date.index('m')+1]
                    convert_sale_date = datetime.strptime(sale_date, "%m/%d/%Y %I:%M %p")
                    now = datetime.now()
                    total_seconds = (convert_sale_date - now).total_seconds()
                    if total_seconds >= 0:
                        print('-------------->>> Total seconds:', total_seconds)
                        index = idx
                        break
                print("-------------->>> Search Sales List pass")
                if index != -1:
                    try:
                        time.sleep(4)
                        bid_now_btn = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, search_list_xpath+f"[{(index+1)}]/td[14]/ul/li/ul/li[2]/a")))
                        bid_now_btn.click()
                        print("-------------->>> Bid Now Button pass")

                        sleeping('no_upcoming')
                    except:
                        print("-------------->>> Can't find Bid Now Button")
                        pass
            except:
                print("-------------->>> Can't find Search List")
                pass
        except:
            print("-------------->>> Can't find Search Button")
            pass
    except:
        print("-------------->>> Can't find Link For Search List")
        pass

def upcoming():
    print("-------------->>> 'No Upcoming Auctions' doesn't exist")
    sleeping('upcoming')

def sleeping(str):
    time_str = []
    sleeping_time_xpath = ''
    if str == 'no_upcoming':
        time_str = ['D', 'H', 'min']
        sleeping_time_xpath = waiting_time_xpath
    else:
        time_str = ['d', 'h', 'm']
        sleeping_time_xpath = waiting_time_in_iframe_xpath
    
    try:
        time.sleep(3)
        waiting_time = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, sleeping_time_xpath))).text
        print(f'-------------->>> Time Left: {waiting_time}')
        sleeping_time = 0
        if waiting_time.find('d') != -1:
            day = re.findall(r'\d+', waiting_time[:waiting_time.find(time_str[0])])[-1]
            sleeping_time = int(day)*24*3600
        if waiting_time.find('h') != -1:
            hour = re.findall(r'\d+', waiting_time[:waiting_time.find(time_str[1])])[-1]
            sleeping_time += int(hour)*3600
        if waiting_time.find('m') != -1:
            min = re.findall(r'\d+', waiting_time[:waiting_time.find(time_str[2])])[-1]
            sleeping_time += int(min)*60
        print(f"-------------->>> Auction hasn't started yet. Sleeping for {sleeping_time}seconds")
        time.sleep(sleeping_time)
    except:
        print("-------------->>> Can't find Time Left")
        pass

def auctions_record():
    vin_list = []
    price_list = []
    count = 0
    while True:
        price_change = []
        try:
            print('-------------->>> svg')
            price = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'svg')))
            price_change = [price[idx].text for idx in range(len(price))]
            print(price_change)
        except NoSuchElementException:
            print("-------------->>> Can't find svg")
            try:
                print('-------------->>> div')
                price = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, price_xpath)))
                price_change = [price[idx].text for idx in range(len(price))]
                print(price_change)
            except:
                print("-------------->>> Can't price description")
                pass
        except Exception as e:
            print(e)
            pass
        
        vin_change = []
        try:
            print('-------------->>> vin')
            vin = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, vin_xpath)))
            vin_change = [vin[idx].text for idx in range(len(vin))]
            print(vin_change)
        except NoSuchElementException:
            print("Can't find vin")
            pass

        for idx, vin_value in enumerate(vin_change):
            if vin_list[idx] == []:
                vin_list = vin_change
                price_list = price_change
                break
            elif vin_list[idx] == vin_value:
                price_list[idx] = price_change[idx]
            elif vin_list[idx] != vin_value:
                auction_result.append({'vin': vin_list[idx], 'price': price_list[idx]})
                vin_list[idx] = vin_change[idx]
                price_list[idx] = price_change[idx]
        print('-------------->>> ', auction_result)
        count += 1
        if count == 100: break
        if vin_change == []: break
    print('-------------->>> The auction is over.')

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
    draw_banner()
    copart()