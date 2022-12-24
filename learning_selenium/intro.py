# chrome driver site https://sites.google.com/chromium.org/driver/?pli=1
# xattr -d com.apple.quarantine chromedriver 
# code source https://scrapfly.io/blog/web-scraping-with-selenium-and-python/
# onetrust-accept-btn-handler
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
# from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_experimental_option("detach", True) # allow the window to remain open
options.headless = False
options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
options.add_argument("start-maximized")  # ensure window is full-screen

# configure chrome browser to not load images and javascript
options.add_experimental_option(
    # this will disable image loading
    "prefs", {"profile.managed_default_content_settings.images": 2}
)

PATH = '/Users/dalmas.otieno/Documents/youtube/fifa-world-cup-data-analysis/cromedriver'
driver = webdriver.Chrome(PATH, options=options)

URL = 'https://www.fifa.com/fifaplus/en/tournaments/mens/worldcup/qatar2022/scores-fixtures?country=UG&wtw-filter=ALL'
print(driver.title)
driver.get(URL)

print(1)
# wait for page to load
element = WebDriverWait(driver=driver, timeout=60)
# .until(
#     EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-target=directory-first-item]'))
# )
print(2)
ACCEPT_COOKIES_BUTTON_XPATH = '//button[@id="onetrust-accept-btn-handler"]'
button = driver.find_element_by_xpath(ACCEPT_COOKIES_BUTTON_XPATH)
print(3)
button.click()
print(4)
print(driver.page_source)