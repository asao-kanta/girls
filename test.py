import requests
from bs4 import BeautifulSoup
import pandas as pd

from datetime import date, timedelta, datetime

# try:
names = []
df = pd.DataFrame()
url = "https://www.cityheaven.net/akita/A0503/A050301/loveandlove/girlid-41485255/"
headers = {"User-Agent":
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

html = requests.get(url, headers=headers)
print(html)
