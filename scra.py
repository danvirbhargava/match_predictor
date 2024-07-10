from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

def extract_stats(url):
    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'stats-module__single-stat'))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        team_name_tag = soup.find('span', class_='team-name pk-d--none pk-d-sm--block')
        team_name = team_name_tag.text.strip() if team_name_tag else 'Unknown'
        stats = {"team": team_name}
        stat_items = soup.find_all('pk-num-stat-item')
        for item in stat_items:
            stat_value = item.find('div', slot='stat-value').text.strip() if item.find('div', slot='stat-value') else None
            stat_label = item.find('div', slot='stat-label').text.strip() if item.find('div', slot='stat-label') else None
            stat_second_label = item.find('div', slot='stat-second-label').text.strip() if item.find('div', slot='stat-second-label') else None
            if stat_label:
                stats[stat_label] = {
                    "value": stat_value,
                    "second-label": stat_second_label
                }
        return stats
    except TimeoutException:
        print(f"Timeout while loading {url}")
        return None
        

# setting up web driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

stats_url = 'https://www.uefa.com/european-qualifiers/statistics/teams/?order=desc&sortBy=matches_win'
driver.get(stats_url)

WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.TAG_NAME, 'body'))
)
soup = BeautifulSoup(driver.page_source, 'html.parser')
all_links = soup.find_all('a', href=True)

base_url = 'https://www.uefa.com'

team_stats_links = [
    base_url + a_tag['href'] for a_tag in all_links 
    if a_tag['href'].startswith('/api/v1/linkrules/team/') and 'statistics' in a_tag['href']
]

all_stats = []
for link in team_stats_links:
    stats = extract_stats(link)
    if stats:
        all_stats.append(stats)
driver.quit()

flattened_stats = []
for stat in all_stats:
    flattened_stat = {"team": stat["team"]}
    for key, value in stat.items():
        if key != "team":
            flattened_stat[f"{key}"] = value["value"]
    flattened_stats.append(flattened_stat)

team_stats_df = pd.DataFrame(flattened_stats)

print(team_stats_df)
team_stats_df.to_csv('team_stats.csv', index=False)