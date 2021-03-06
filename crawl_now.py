from tools.handle_now import HandleNow
from tools import helper
import os
if __name__ == "__main__":    
    signin_URL="https://www.now.vn/account/login"
    user_info_file = "user_information.txt"
    url_file = "url.txt"
    chrome_file = "chrome_driver.txt"
    website_name = helper.read_file(url_file)
    chrome_driver = helper.read_file(chrome_file)
    user_info = helper.read_user_information(user_info_file)
    #check this path exist
    if(not os.path.exists(chrome_driver)):
        print("WRONG CHROME PATH")
        exit()
    handleNow = HandleNow(chrome_driver)
    
    is_login = handleNow.handle_signin(signin_URL, user_info)
    if(not is_login):
        print("Please check your username and password")
        exit()
    # handleNow = HandleNow()
    menu_list, topping_list =  handleNow.handle_crawl(website_name)
    handleNow.save_values_to_xml_file("food.xlsx", menu_list, topping_list)
