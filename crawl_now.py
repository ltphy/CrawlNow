from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def handle_crawl(url):
    print("CRAWL URL", url)
    options = webdriver.ChromeOptions()
    #enable full screen 
    options.add_argument('--kiosk')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')

    
    driver = webdriver.Chrome('C:\driver\chromedriver.exe', options=options)
    driver.maximize_window()
    driver.implicitly_wait(5)

    driver.get(url)
    #get category menu list
    # category_list = driver.find_element_by_class_name('menu-restaurant-category')
    category_list = wait(driver, 10).until(
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
        food_elements = driver.find_elements_by_xpath('//div[@class="ReactVirtualized__Grid__innerScrollContainer"]/div')
        
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
                            

    driver.quit()
URL="https://www.now.vn/ho-chi-minh/lotteria-nguyen-van-nghi"
handle_crawl(URL)
