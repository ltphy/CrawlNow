def read_user_information(filename):
    user_info = {}
    with open(filename, "r") as file:
        user_name = file.readline().replace("\n","")
        password = file.readline().replace("\n","")
        user_info = {"username": user_name, "password":password}
    return user_info
def read_file(filename):
    website_name = ""
    with open(filename, "r") as file:
        website_name = file.readline().replace("\n","")
    return website_name
