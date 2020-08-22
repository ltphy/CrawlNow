import requests
from tools.handle_now import HandleNow
import helper
signin_URL="https://www.now.vn/account/login"
user_info_file = "user_information.txt"
url = "url.txt"
website_name = helper.read_now_web(url)
user_info = helper.sread_user_information(user_info_file)
handleNow = HandleNow(signin_URL, user_info)
print("USER", user_info)
menu_list, topping_list =  handleNow.handle_crawl(URL)
handleNow.save_values_to_xml_file("food.xlsx", menu_list, topping_list)
