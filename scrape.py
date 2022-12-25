from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


website = 'https://www.fifa.com/fifaplus/en/tournaments/mens/worldcup/qatar2022/scores-fixtures?country=UG&wtw-filter=ALL'
options = Options()
options.add_experimental_option("detach", True)
driver1 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver1.get(website)

def accept_cookies(driver_object):
    time.sleep(10)
    accept_cookies_button = driver_object.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')
    accept_cookies_button.click()

def animate_scroll(driver_object):
        for i in range(8):
            time.sleep(1)
            driver_object.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

def extract_data(driver_object):
    pass

accept_cookies(driver_object=driver1)
anchor_divs = driver1.find_elements(By.XPATH, '//div[@class="match-block_wtwOuterMatchBlock__3ZBGT"]/a')
all_h_links = []
for anchor_div in anchor_divs:
    hlink = anchor_div.get_attribute('href')
    all_h_links.append(hlink)
animate_scroll(driver1)
driver1.quit()

for hlink in all_h_links[:10]:
    print(f'''window.open("{hlink}","_blank");''')
    driver2 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver2.get(hlink)
    accept_cookies(driver_object=driver2)
    stats_tab_xpath = '//div[@class="rail_childContainer__UIJ1R match-details-new-tabs-component_tabsContainer__2MfUY"]/div[4]'
    stats_tab = driver2.find_element(By.XPATH, stats_tab_xpath)
    stats_tab.click()
    animate_scroll(driver2)
    driver2.quit()
