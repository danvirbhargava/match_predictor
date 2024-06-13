import requests
from bs4 import BeautifulSoup

stats_url = "https://www.uefa.com/european-qualifiers/statistics/teams/"
##headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}
##data = requests.get(stats_url, headers=headers)
##soup = BeautifulSoup(data.content, 'html.parser')
##standings_table = soup.find_all("div",{"class" : "ag-center-cols-container"})
##print(standings_table)
from requests_html import HTMLSession

session = HTMLSession()
data = session.get(stats_url)
print(data)
