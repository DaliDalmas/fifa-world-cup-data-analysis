# link to the video
# https://www.youtube.com/watch?v=UOsRrxMKJYk
# you can also checkout my youtube channel here https://www.youtube.com/@dalicodes/videos

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

website = 'https://www.adamchoi.co.uk/teamgoals/detailed'

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(website)
all_matches_button = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
all_matches_button.click()

matches = driver.find_elements(By.TAG_NAME, 'tr')
matches_list = []
for match in matches:
    matches_list.append([
        match.find_element(By.XPATH, './td[1]').text,
        match.find_element(By.XPATH, './td[2]').text,
        match.find_element(By.XPATH, './td[3]').text.split('-')[0].strip(),
        match.find_element(By.XPATH, './td[3]').text.split('-')[0].strip(),
        match.find_element(By.XPATH, './td[4]').text,
    ])
df = pd.DataFrame(matches_list, columns=['date', 'home_team', 'home_score', 'away_score', 'away_team'])
df.to_csv('learning_selenium/data/premier_league.csv', index=False)
driver.quit()