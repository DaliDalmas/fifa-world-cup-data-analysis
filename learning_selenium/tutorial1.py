# Note: Major changes has happened to this code that may be different from the original video
# Original videohttps://www.youtube.com/watch?v=UOsRrxMKJYk
# you can also checkout my youtube channel here https://www.youtube.com/@dalicodes/videos

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

website = 'https://www.adamchoi.co.uk/teamgoals/detailed'

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(website)
all_matches_button = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
all_matches_button.click()


country_dropdown = Select(driver.find_element(By.ID, 'country'))
league_dropdown = Select(driver.find_element(By.ID, 'league'))
season_dropdown = Select(driver.find_element(By.ID, 'season'))
matches_list = []

countries = driver.find_element(By.XPATH, '//select[@id="country"]').find_elements(By.TAG_NAME, 'option')
for country in countries:
    print(country.text)
    country_dropdown.select_by_visible_text(country.text)
    time.sleep(5)
    leagues = driver.find_element(By.XPATH, '//select[@id="league"]').find_elements(By.TAG_NAME, 'option')
    for league in leagues:
        print(league.text)
        league_dropdown.select_by_visible_text(league.text)
        time.sleep(5)
        seasons = driver.find_element(By.XPATH, '//select[@id="season"]').find_elements(By.TAG_NAME, 'option')
        for season in seasons:
            print(season.text)
            season_dropdown.select_by_visible_text(season.text)
            time.sleep(5)
            matches = driver.find_elements(By.TAG_NAME, 'tr')
            for match in matches:
                matches_list.append([
                    country,
                    league,
                    season,
                    match.find_element(By.XPATH, './td[1]').text,
                    match.find_element(By.XPATH, './td[2]').text,
                    match.find_element(By.XPATH, './td[3]').text.split('-')[0].strip(),
                    match.find_element(By.XPATH, './td[3]').text.split('-')[0].strip(),
                    match.find_element(By.XPATH, './td[4]').text,
                ])
df = pd.DataFrame(matches_list, columns=['date', 'home_team', 'home_score', 'away_score', 'away_team'])
df.to_csv('learning_selenium/data/football_data.csv', index=False)
driver.quit()