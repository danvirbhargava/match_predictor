import requests
from bs4 import BeautifulSoup

stats_url = "https://www.uefa.com/european-qualifiers/statistics/teams/"
headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}
data = requests.get(stats_url, headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
standings_table = soup.find('div', class_='ag-center-cols-viewport')
print(standings_table)