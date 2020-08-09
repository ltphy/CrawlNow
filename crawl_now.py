from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait as wait

def handle_crawl(url):
    print("CRAWL URL", url)
    options = webdriver.ChromeOptions()
    #enable full screen 
    options.add_argument('--kiosk')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')

    
    driver = webdriver.Chrome('C:\driver\chromedriver.exe', options=options)
    driver.maximize_window()
    driver.set_page_load_timeout(20)

    driver.get(url)
    #get category menu list
    category_list = driver.find_element_by_class_name('menu-restaurant-category')
    category_values = category_list.find_elements_by_css_selector('span.item-link')
    # print(category_list.text)
    #get all the ite
    
    for value in category_values:
        value.click()
        print("value: ", value.text)
        try:
            #//*[@id="restaurant-item"]/div/div/div
            food_elements = driver.find_elements_by_xpath('//div[@class="ReactVirtualized__Grid__innerScrollContainer"]/div')

            for food_element in food_elements:
                if(food_element.get_attribute('class')=="menu-group"):
                    print("CONTENT", food_element.text)
                else:
                            

        except:
            print("NON")
    driver.quit()
URL="https://www.now.vn/ho-chi-minh/du-du-s-bakery-banh-tuoi-dai-loan"
handle_crawl(URL)
