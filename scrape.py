from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

website = 'https://www.fifa.com/fifaplus/en/tournaments/mens/worldcup/qatar2022/scores-fixtures?country=UG&wtw-filter=ALL'
options = Options()
options.add_experimental_option("detach", True)
driver1 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver1.get(website)

def accept_cookies(driver_object):
    time.sleep(15)
    accept_cookies_button = driver_object.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')
    accept_cookies_button.click()

def animate_scroll(driver_object):
        for i in range(3):
            time.sleep(1)
            driver_object.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

def extract_data(driver_object):
    # General information
    match_kind = driver_object.find_element(By.XPATH, '//p[@class="ff-m-0 ff-p-0"]').text
    date_time = driver_object.find_element(By.XPATH, '//p[@class="ff-p-0"]').text.replace('•', '-')
    first_team = driver_object.find_element(By.XPATH, '//p[@class="match-score_TeamName__3Ua0B text-align-end justify-content-end ff-m-0 ff-mr-16 ff-my-8 text-lg ff-mr-md-16 ff-mr-lg-48"]').text
    second_team = driver_object.find_element(By.XPATH, '//p[@class="match-score_TeamName__3Ua0B ff-m-0 ff-ml-16 ff-my-8 text-lg ff-ml-md-16 ff-ml-lg-48"]').text
    scores = driver_object.find_element(By.XPATH, '//span[@class="show-match-score_BigFont__qRZ5P show-match-score_BiggerFont__2lUIG show-match-score_score__23vdC d-flex align-items-center justify-content-evenly"]')
    first_team_score = scores.text.split('-')[0].strip()
    second_team_score = scores.text.split('-')[1].strip()

    # Attacking information
    first_team_posession = driver_object.find_element(By.XPATH, '//div[@class="d-flex justify-content-center align-items-center flex-column ff-mb-24"]/div/p[1]').text
    second_team_possession = driver_object.find_element(By.XPATH, '//div[@class="d-flex justify-content-center align-items-center flex-column ff-mb-24"]/div/p[2]').text
    other_metrices_divs = driver_object.find_elements(By.XPATH, '//div[@class="d-flex justify-content-center align-items-center flex-column ff-mt-20"]')
    pk = f'{match_kind}{first_team}{second_team}'.replace(' ', '').replace('-', '').lower()
    print(f"fetching {match_kind} {first_team} vs {second_team}")
    general_info = [
        pk,
        match_kind,
        date_time,
        first_team,
        second_team,
        first_team_score,
        second_team_score,
        first_team_posession,
        second_team_possession
    ]

    match_stats = []
    for metric_div in other_metrices_divs:
        metric = metric_div.find_element(By.XPATH, './p[@class="ff-m-0 ff-mb-8"]').text
        first_team_metric_values = metric_div.find_element(By.XPATH, './div/div/p[@class="ff-m-0 ff-mr-20"]').text
        second_team_metric_values = metric_div.find_element(By.XPATH, './div/div/p[@class="ff-m-0 ff-ml-20"]').text
        mpk = f'{pk}{metric}'.replace(' ', '').replace('-', '').lower()
        match_stats.append([
            mpk,
            pk,
            metric,
            first_team_metric_values,
            second_team_metric_values
        ])
    return general_info, match_stats


accept_cookies(driver_object=driver1)
anchor_divs = driver1.find_elements(By.XPATH, '//div[@class="match-block_wtwOuterMatchBlock__3ZBGT"]/a')
all_h_links = []
for anchor_div in anchor_divs:
    hlink = anchor_div.get_attribute('href')
    all_h_links.append(hlink)
animate_scroll(driver1)
driver1.quit()

all_matches_general_info = []
all_matches_stats = []
for hlink in all_h_links[:5]:
    driver2 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver2.get(hlink)
    accept_cookies(driver_object=driver2)
    stats_tab_xpath = '//div[@class="rail_childContainer__UIJ1R match-details-new-tabs-component_tabsContainer__2MfUY"]/div[4]'
    stats_tab = driver2.find_element(By.XPATH, stats_tab_xpath)
    stats_tab.click()
    general_info, match_stats = extract_data(driver2)
    all_matches_general_info.append(general_info) 
    all_matches_stats = all_matches_stats + match_stats
    animate_scroll(driver2)
    driver2.quit()

matches_cols = [
        'id',
        'match_kind',
        'date_time',
        'first_team',
        'second_team',
        'first_team_score',
        'second_team_score',
        'first_team_posession',
        'second_team_possession'
    ]
stats_cols = [
    'id',
    'match_id',
    'metric',
    'first_team_metric_values',
    'second_team_metric_values'
]
matches = pd.DataFrame(all_matches_general_info, columns=matches_cols)
print(matches.head())
matches.to_csv('data/matches.csv', index=False)
stats = pd.DataFrame(all_matches_stats, columns=stats_cols)
stats.to_csv('data/stats.csv', index=False)
print(stats.head())