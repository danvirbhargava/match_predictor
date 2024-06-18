from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
stats_url = 'https://www.uefa.com/european-qualifiers/statistics/teams/'
driver.get(stats_url)
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'ag-center-cols-container'))
    )
except:
    print("Elements not found within the given time")
soup = BeautifulSoup(driver.page_source, 'html.parser')
table_divs = soup.find_all('div', class_='ag-center-cols-container')
if table_divs:
    print(table_divs[0].prettify()[:20000])
team_links = []
for table_div in table_divs:
    for a_tag in table_div.find_all('a', href=True):
        team_links.append(a_tag['href'])
team_stats = pd.DataFrame(team_links, columns=['Links'])
##print(team_stats)

