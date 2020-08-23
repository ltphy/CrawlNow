from tools.handle_now import HandleNow
from tools import helper
if __name__ == "__main__":    
    signin_URL="https://www.now.vn/account/login"
    user_info_file = "user_information.txt"
    url_file = "url.txt"
    chrome_file = "chrome_driver.txt"
    website_name = helper.read_file(url_file)
    chrome_driver = helper.read_file(chrome_file)
    user_info = helper.read_user_information(user_info_file)
    handleNow = HandleNow(chrome_driver)
    
    handleNow.handle_signin(signin_URL, user_info)
    # handleNow = HandleNow()
    menu_list, topping_list =  handleNow.handle_crawl(website_name)
    handleNow.save_values_to_xml_file("food.xlsx", menu_list, topping_list)
