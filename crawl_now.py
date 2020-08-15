from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pickle
class HandleNow:
    def __init__(self, signin_url, user_info):
        options = webdriver.ChromeOptions()
        #enable full screen 
        options.add_argument('--kiosk')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        #user-data-dir=> to create selenium folder. 
        options.add_argument('--user-data-dir=selenium')
        # options.add_argument("user-data-dir=C:/Users/phyli/AppData/Local/Google/Chrome/User Data")
        #using a new profile data
        # options.add_argument("profile-directory=Profile 1")

        self.driver = webdriver.Chrome('C:\driver\chromedriver.exe', options=options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.handle_signin(signin_url, user_info)

    def handle_signin(self, signin_url, user_info):
        
        self.driver.get(signin_url)
        cookie = self.driver.get_cookies()
        print("COOKIE", cookie)
        try: 
            login_element = wait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "form-login-input"))
            )
        except:
            return
        
        username = login_element.find_element_by_xpath("//div[@class='field-group']/div[@class='input-group'][1]/input[@type='text']")
        if(username):
            print(username.get_attribute('placeholder'))
            username.send_keys(user_info['username'])
        else: 
            print("CANNOT GET ELEMENT")
            return
        password = login_element.find_element_by_xpath("//div[@class='field-group']/div[@class='input-group'][2]/input[@type='password']")
        if(password):
            password.send_keys(user_info['password'])
        else:
            print("CANNOT GET ELEMENT")
            return
        login_element.find_element_by_css_selector("button.btn-submit").click()
        print("SUCCESSFULLY LOGIN!")
        self.save_cookie('cookie.pkl')

    def save_cookie(self, path):
        with open(path, 'wb') as filehandler:
            pickle.dump(self.driver.get_cookies(), filehandler)

    def load_cookie(self, path):
        with open(path, 'rb') as cookiefile:
            cookies = pickle.load(cookiefile)
            for cookie in cookies:
                print("COOKIE", cookie)
                self.driver.add_cookie(cookie)

    def handle_crawl(self, url):
        self.load_cookie('cookie.pkl')
        self.driver.get(url)
        #get category menu list
        # category_list = driver.find_element_by_class_name('menu-restaurant-category')
        category_list = wait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "menu-restaurant-category"))
        )
        category_values = category_list.find_elements_by_css_selector('span.item-link')
        # print(category_list.text)
        #get all the ite
        #a dict with menu {menu: {food:price}}
        menu_list = []
        check_list = []
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
                            food_name = food_element.find_element_by_class_name('item-restaurant-name')
                            current_price = food_element.find_element_by_class_name('current-price')
                            print("{}: {}".format(food_name.text, current_price.text))
                            food_item = {'food_name': food_name.text, 'current_price': current_price.text}
                            food_list.append(food_item)
                except:
                    print("NONE")
            check_list.append(category_name)
            category_dict.update({'food_list':food_list})
            menu_list.append(category_dict)
            print("MENU DICT", menu_list)
                                
        self.driver.quit()

def read_user_information(filename):
    user_info = {}
    with open(filename, "r") as file:
        user_name = file.readline().replace("\n","")
        password = file.readline().replace("\n","")
        user_info = {"username": user_name, "password":password}
    return user_info

URL="https://www.now.vn/ho-chi-minh/larva-mi-cay-an-vat"
signin_URL="https://www.now.vn/account/login"
user_info_file = "user_information.txt"
user_info = read_user_information(user_info_file)
handleNow = HandleNow(signin_URL, user_info)
print("USER", user_info)
handleNow.handle_crawl(URL)
