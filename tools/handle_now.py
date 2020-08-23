from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pickle
import pandas as pd
import time
class HandleNow:
    def __init__(self, chrome_driver_path):
        options = webdriver.ChromeOptions()
        #enable full screen 
        options.add_argument('--kiosk')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        #user-data-dir=> to create selenium folder. 
        options.add_argument('--user-data-dir=selenium') 
        #using a new profile data
        options.add_argument("--profile-directory=Profile 1")
      
        try:    
            self.driver = webdriver.Chrome(chrome_driver_path, options=options)
        except:
            print("Please check your chrome driver path!")
            exit()
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        

    def handle_signin(self, signin_url, user_info):
        
        self.driver.get(signin_url)

        # if(self.driver.get_cookies()):
        #     return True
        try: 
            login_element = wait(self.driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "form-login-input"))
            )
        except:
            #if redirect to main page mean already logged in
            current_website = self.driver.current_url
            if "account/login" not in current_website:
                print ("USE COOKIE")
                return True
            return False
        
        username = login_element.find_element_by_xpath("//div[@class='field-group']/div[@class='input-group'][1]/input[@type='text']")
        if(username):
            print(username.get_attribute('placeholder'))
            username.send_keys(user_info['username'])
        else: 
            print("CANNOT GET ELEMENT")
            return False
        password = login_element.find_element_by_xpath("//div[@class='field-group']/div[@class='input-group'][2]/input[@type='password']")
        if(password):
            password.send_keys(user_info['password'])
        else:
            print("CANNOT GET ELEMENT")
            return False
        login_element.find_element_by_css_selector("button.btn-submit").click()
        time.sleep(5)
        #check wheter it redirect to home page 
        current_website = self.driver.current_url
        #redirect to homepage mean login successfully
        if "account/login" in current_website:
            print ("LOGIN FAILED")
            self.driver.quit()
            return False
        print("SUCCESSFULLY LOGIN!")
        # self.save_cookie('cookie.pkl')
        return True
        # self.driver.quit()
    def save_cookie(self, path):
        with open(path, 'wb') as filehandler:
            pickle.dump(self.driver.get_cookies(), filehandler)

    def load_cookie(self, path):
        with open(path, 'rb') as cookiefile:
            cookies = pickle.load(cookiefile)
            for cookie in cookies:
                print("COOKIE", cookie)
                self.driver.add_cookie(cookie)
    def crawl_topping_content(self, topping_element):
        topping_content = []
        topping_list = topping_element.find_elements_by_class_name('topping-category-item')
        for topping_item_element in topping_list:
            topping_category_item = {}
            topping_name = topping_item_element.find_element_by_class_name('topping-name')
            topping_check_boxes = topping_item_element.find_elements_by_class_name('custom-checkbox')
            topping_category_item.update({'topping_title':topping_name.text})
            print("TOPPING NAME", topping_name.text)
            topping_items = []
            #loop through each topping check box and push to list
            for topping_check_box in topping_check_boxes:
                topping_check_box_item = {}
                #get input name
                # print("TOPPING CHECK BOX", topping_check_box.text)
                price = topping_check_box.find_element_by_css_selector('span.topping-item-price')
                price_text = price.text
                name_text = (topping_check_box.text).replace(price_text,"")
                topping_check_box_item = {'topping_name': name_text}
                # print("NAME: ", name_text)
                # print("PRICE: ", price_text)
                if(price_text):
                    topping_check_box_item.update({'topping_price': (price_text).replace("đ","")})
                topping_items.append(topping_check_box_item)
            topping_category_item.update({'topping_items': topping_items})    
            topping_content.append(topping_category_item)
        return topping_content
    def save_values_to_xml_file(self,file_name,food_items, topping_items):
        excel_file_name = file_name
        items = []
        column_keys = ['food name','current price', 'description', 'category title','topping category']
        for category_list in food_items:
            category_name = category_list['category_name']
            food_list = category_list['food_list']
            for food in food_list:
                item = [food.get('food_name',''),int(food.get('current_price','').replace(",","")),food.get('description',''), category_name, food.get('topping_category','')]
                items.append(item)
        df_food = pd.DataFrame(items, columns = column_keys)
        column_keys = ['topping name', 'topping price', 'topping title']
        df_topping_list = []
        for topping_type in topping_items:
            #each topping type have many category topping title
            topping_items = []
            for topping_category in topping_type:
                category = topping_category['topping_title']
                topping_list_items = topping_category['topping_items']
                for item in topping_list_items:
                    topping_price = item.get('topping_price','').replace(",","")
                    if(topping_price != ""):
                        topping_price = int(topping_price)
                    topping_item = [item.get('topping_name',''), topping_price , category]
                    topping_items.append(topping_item)
            df1 = pd.DataFrame(topping_items, columns = column_keys)
            df_topping_list.append(df1)
        with pd.ExcelWriter(excel_file_name) as writer:
            df_food.to_excel(writer,sheet_name="food")
            for i, df_topping in enumerate(df_topping_list):
                df_topping.to_excel(writer, sheet_name="category_"+str(i))

        category_dict = food_items[0].keys()
        
    def handle_crawl(self, url):
        # self.load_cookie('cookie.pkl')
        self.driver.get(url)
        #check this url exist 
        #get category menu list
        # category_list = driver.find_element_by_class_name('menu-restaurant-category')
        try:
            
            # popup_modal = find_elements_by_xpath('//*[@id="modal"]')
            #https://stackoverflow.com/questions/59130200/selenium-wait-until-element-is-present-visible-and-interactable
            #visibitity located on the page (got height and width)
            popup_modal = wait(self.driver, 3).until(
            EC.visibility_of_element_located((By.ID, "modal"))
            )
            active_modal = popup_modal.find_element_by_css_selector("div.is-active")
            
            #find button ok to turn off.
            #//*[contains(text(), 'Ok')]
            # btn_ok = active_modal.find_element_by_css_selector('button.btn-red')
            btn_ok = active_modal.find_element_by_xpath('div[1]/div/div[3]/button')
            btn_ok.click()
        except:
            print("No pop up modal")
        try:
            category_list = wait(self.driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "menu-restaurant-category"))
            )
        except:
            print("Invalid URL")
            self.driver.quit()
            exit()
        category_values = category_list.find_elements_by_css_selector('span.item-link')
        # print(category_list.text)
        #get all the ite
        #a dict with menu {menu: {food:price}}
        menu_list = []
        check_list = []
        #store the topping string list. 
        topping_list = []
        topping_list_text = []
        #reset value before crawl data.
        reset_value = self.driver.find_element_by_css_selector("button.btn-reset")
        reset_value.click()
        for value in category_values:
            value.click()
            print("value: ", value.text)
            category_name = value.text
            category_dict = {'category_name':category_name}
            food_list = []
            #//*[@id="restaurant-item"]/div/div/div
            food_elements = self.driver.find_elements_by_xpath('//div[@class="ReactVirtualized__Grid__innerScrollContainer"]/div')
            
            new_menu_flag = False
            for food_element in food_elements:
                try:
                    print("FOOD ELEMENT", food_element.text)
                    #meet cateogy first
                    if(food_element.get_attribute('class')=="menu-group"):
                        category_content = food_element.text
                        #currently in the menu_dict list and we want it is empty => so that can assign
                        if category_content == category_name:
                            new_menu_flag = True
                        else: #not in the check list
                            if(category_content not in check_list):
                                break
                    #meet food
                    else:
                        if new_menu_flag:
                            
                            #update food to the current menu content
                            food_name = wait(food_element, 3).until(
                                    EC.visibility_of_element_located((By.CLASS_NAME, "item-restaurant-name"))
                                )
                            current_price =  wait(food_element, 3).until(
                                    EC.visibility_of_element_located((By.CLASS_NAME, "current-price"))
                                )
                            description_text = ""
                            try:
                                description = wait(food_element, 3).until(
                                    EC.visibility_of_element_located((By.CLASS_NAME, "item-restaurant-desc"))
                                )
                                description_text = description.text

                            except:
                                print("no description")
                            #wait until food element containing bt-adding can be clickable
                            plus_element = wait(food_element, 3).until(
                                EC.element_to_be_clickable((By.CLASS_NAME, "btn-adding"))
                            )
                            actions = ActionChains(self.driver)
                            food_name_text = food_name.text
               
                            food_item = {'food_name': food_name_text, 'current_price': (current_price.text).replace("đ",""), 'description': description_text}
                            #show topping modal
                            print("PLUS ELEMENT: ", plus_element.text)
                            #dont know why this one cant click for those first item? 1
                            #because the first element, it cannot click it will skip this item
                            actions.move_to_element(plus_element).click().perform()

                            print("CAN CLICK")
                            topping_content = {}
                            #find topping category #should wait it present and appear?
                            try:
                                print("START TO GET TOPPING")
                                modal_element = wait(self.driver, 5).until(
                                    EC.visibility_of_element_located((By.ID, "modal-topping"))
                                )
                                topping_category = modal_element.find_element_by_class_name('topping-category')
                                topping_category_text = topping_category.text
                                #dont have any topping
                                if(not topping_category_text):
                                    print("Dont have topping")
                                #new item
                                elif(topping_category_text not in topping_list_text):
                                    #update the text
                                    print("not in topping list")
                                    topping_list_text.append(topping_category_text)
                                    food_item.update({'topping_category': len(topping_list_text)-1})
                                    print("TOPPING list _ text", topping_list_text)
                                    #crawl topping elements
                                    topping_content = self.crawl_topping_content(topping_category)
                                    topping_list.append(topping_content)
                                    #find Ok to click
                                    #div/div/div[3]/div/div[2]/button
                                    ok_button = modal_element.find_element_by_xpath('//div/div/div[3]/div/div[2]/button')
                                    # modal_element.click()
                                    ok_button.click()
                                    #update the 
                                else:
                                    print("in topping list")
                                    ok_button = modal_element.find_element_by_xpath('//div/div/div[3]/div/div[2]/button')
                                    topping_idx = topping_list_text.index(topping_category_text)
                                    food_item.update({'topping_category': topping_idx})
                                    ok_button.click()
                            except:
                                #modal is not visible => item has no topping
                                print("ITEM HAS NO TOPPING")
                            food_list.append(food_item)
                except:
                    print("NONE")
            
            check_list.append(category_name)
            category_dict.update({'food_list':food_list})
            menu_list.append(category_dict)
            # print("FINAL MENU DICT", menu_list)
            # print("FINAL TOPPING LIST", topping_list)              
        reset_value = self.driver.find_element_by_css_selector("button.btn-reset")
        reset_value.click()
        self.driver.quit()
        print("FINAL MENU DICT", menu_list)
        print("FINAL TOPPING LIST", topping_list)                    
        return menu_list, topping_list
