from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from random import randint
from os.path import exists

import random
import pandas as pd
import time

columns_names=['Brand Name', 'Product Name', 'Category', 'VPN', 'UPC', 'Price', 'Qty', 'Description', 'Specification', 'Video URL', 'Image URL', 'Related Product URL']
df = pd.DataFrame(columns=columns_names)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(executable_path='chromedriver91.0.4472.101_win32.exe', options=chrome_options)
driver.get("https://usa.ingrammicro.com/Site/Search#category%3aComputer%20Systems")
current_window = driver.current_window_handle

time.sleep(5)
driver.find_element_by_id('product-activate').click()
driver.find_element_by_xpath("//a[@class='cc_btn cc_btn_accept_all']").click()

categories_index = 4
categories_url = []
categories_name = []
categories_li = WebDriverWait(driver, 25).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@id='product-list']/ul/li")))
for index in range(len(categories_li)):
    if index < 9:
        element = categories_li[index].find_element_by_xpath('./a')
        categories_url.append(element.get_attribute('href'))
        categories_name.append(element.text)

time.sleep(2)
driver.find_element_by_id('itemPerPageDropdown').click()
driver.find_element_by_xpath('//select[@id="itemPerPageDropdown"]/option[5]').click()
time.sleep(3)

count = 0
index = 0
while True:
    try:
        body_elements = WebDriverWait(driver, 25).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='grid-column js-favorite-lines-container  show']/div")))
    except:
        print('No product')
        pass
    number_of_products = len(body_elements)
    if body_elements[index].get_attribute('data-rank'):
        current_window = driver.current_window_handle
        try:
            time.sleep(5)
            switch_url = driver.find_elements_by_xpath("//div[@class='grid-column js-favorite-lines-container  show']/div["+str(index+1)+"]//a")[0].get_attribute('href')
            driver.execute_script('window.open(arguments[0]);', switch_url)
            new_window = [window for window in driver.window_handles if window != current_window][0]
            driver.switch_to.window(new_window)
        except:
            print('The link is not correct.')
            pass

        if categories_index == 1:
            title = 'Audio video Devices.csv'
        else: title = categories_name[categories_index]+'.csv'

        if exists(title):
            df = pd.read_csv(title)
            count = df.shape[0]
            
        count += 1
        print('--------------------> ' + categories_name[categories_index] +' Product ' + str(count) + ' <----------------------')
        
        try:
            brand = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="Top-Sku-VPN-UPC"]/div/span/a'))).text
            df.at[count - 1, 'Brand Name'] = brand
            print('Brand Name: ' + brand)
        except:
            # df.at[count - 1, 'Brand Name'] = "No brand"
            print('No written brand')
            pass
        
        try:
            tables = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="collapseOne"]/div/div/div[1]/table')))
            productname = ''
            for table in tables:
                trs = table.find_elements_by_xpath('./tbody/tr')
                for tr in trs:
                    tds = tr.find_elements_by_xpath('./td')
                    for td in tds:
                        if td.text == 'Product Name':
                            productname = tds[1].text
                            break
            if productname == '':
                product_description = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="font-20 bold margin-top-lg  clsProductFullDesc"]'))).text
                product_description.strip()
                productname = product_description[(product_description.find(brand)+len(brand)+1):product_description.find(' -')]
            df.at[count - 1, 'Product Name'] = productname
            print('Product Name: ' + productname)
        except:
            # df.at[count - 1, 'Product Name'] = "No product"
            print('No written productname')
            pass

        try:
            category = ''
            category = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//section/main/div/div/div[1]/div[2]/div[1]/span[6]/a'))).text
            df.at[count - 1, 'Category'] = category
            print('Category: ' + category)
        except:
            # df.at[count - 1, 'Category'] = "No category"
            print('No written category')
            pass

        try:
            vpn = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="Top-Sku-VPN-UPC"]/span[1]'))).text
            df.at[count - 1, 'VPN'] = vpn[5:]
            print('VPN: ' + vpn[5:])
        except:
            # df.at[count - 1, 'VPN'] = "No VPN"
            print('No written vpn')
            pass
        
        try:
            upc = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="Top-Sku-VPN-UPC"]/span[3]'))).text
            df.at[count - 1, 'UPC'] = upc[5:]
            print('UPC: ' + upc[5:])
        except:
            # df.at[count - 1, 'UPC'] = "No UPC"
            print('No written upc')
            pass
        
        try:
            price = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@id="priceSection"]/div[1]/div[1]/span[1]'))).text
            product_price = float(price[7:-9].replace(',', ''))
            df.at[count - 1, 'Price'] = product_price
            print('Price: ' + str(product_price))
        except Exception as e:
            # df.at[count - 1, 'Price'] = "No Price"
            print('No written price')
            pass

        try:
            qty = randint(1, 20)
            df.at[count - 1, 'Qty'] = qty
            print('Qty: ' + str(qty))
        except Exception as e:
            # df.at[count - 1, 'Qty'] = "No Qty"
            print('No written qty')
            pass

        try:
            description = ''
            description_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="collapseZero"]/div/div[1]/div/div[1]/div')))
            if len(description_element.find_elements_by_xpath('./p')) > 0:
                descriptions = description_element.find_elements_by_xpath('./p')
                for each_description in descriptions:
                    description += each_description.text + '\n'
            else:
                description = description_element.text
            df.at[count - 1, 'Description'] = description
            print('Description: ' + description)
        except:
            # df.at[count - 1, 'Description'] = "No Description"
            print('No written description')
            pass
        
        try:
            specification = ''
            specification = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="collapseOne"]/div/div'))).text
            df.at[count - 1, 'Specification'] = specification
            print('Specification: ' + specification)
        except:
            # df.at[count - 1, 'Specification'] = "No Specification"
            print('No written specification')
            pass
        
        try:
            video_url = ''
            videos = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="spexWidget_videos"]/div/div[2]/div')))
            for each_video in videos:
                video_url += each_video.find_element_by_xpath('./div/div[1]/iframe').get_attribute('src') + '\n'
            df.at[count - 1, 'Video URL'] = video_url
            print('Videos URL: \n' + video_url)
        except:
            # df.at[count - 1, 'Video URL'] = "No Video"
            print('No videos')
            pass

        try:
            image_url = ''
            images = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="spexWidget_thumbnails"]/div/div')))
            for each_image in images:
                if each_image.get_attribute('class') == 'col-xs-4 padB10':
                    image_url += each_image.find_element_by_xpath('./img').get_attribute('src') + '\n'
            df.at[count - 1, 'Image URL'] = image_url
            print('Images URL: \n' + image_url)
        except:
            # df.at[count - 1, 'Image URL'] = "No Image"
            print('No images')
            pass
        
        try:
            related_products_url = ''
            related_products = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="flexbox-carousel-list js-flexbox-carousel-list"]/div')))
            for each_product in related_products:
                related_products_url += each_product.find_element_by_xpath('./div/div/a[1]').get_attribute('href') + '\n'
            df.at[count - 1, 'Related Product URL'] = related_products_url
            print('Related Products URL: \n' + related_products_url)
        except:
            # df.at[count - 1, 'Related Product URL'] = "No Related Products"
            print('No related products')
            pass
        
        for window in driver.window_handles:
            if current_window != window:
                driver.switch_to.window(window)
                driver.close()
        driver.switch_to.window(current_window)
        
        df.to_csv(title, index = False)
        
    index += 1
    if index == number_of_products:
        index = 0
        try:
            time.sleep(5)
            driver.find_element_by_xpath("//ul[@id='search-paging-container']//a[@id='nextPage']").click()
        except NoSuchElementException:
            if categories_index < 8:
                categories_index += 1
                count = 0
                driver.get(categories_url[categories_index])
            elif categories_index == 8:
                break
        except: pass
        time.sleep(10)

driver.close()