URL="https://www.now.vn/ho-chi-minh/ngon-24h-an-vat-mien-que"
from selenium import webdriver

options = webdriver.ChromeOptions()
#enable full screen 
options.add_argument('--kiosk')

driver = webdriver.Chrome()
A
