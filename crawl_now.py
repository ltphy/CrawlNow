import requests
from tools.handle_now import HandleNow
def read_user_information(filename):
    user_info = {}
    with open(filename, "r") as file:
        user_name = file.readline().replace("\n","")
        password = file.readline().replace("\n","")
        user_info = {"username": user_name, "password":password}
    return user_info

URL="https://www.now.vn/ho-chi-minh/patis-story-coffee"
signin_URL="https://www.now.vn/account/login"
user_info_file = "user_information.txt"
user_info = read_user_information(user_info_file)
handleNow = HandleNow(signin_URL, user_info)
print("USER", user_info)
menu_list, topping_list =  handleNow.handle_crawl(URL)
handleNow.save_values_to_xml_file("food.xlsx", menu_list, topping_list)
