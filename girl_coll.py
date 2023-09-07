import requests
from bs4 import BeautifulSoup
import pandas as pd

from datetime import date, timedelta, datetime
headers = {"User-Agent":
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

try:
    names = []
    df = pd.DataFrame()
    urls = pd.read_csv('url.csv', index_col=0)

    today = datetime.today()
    year, month, day = today.year, today.month, today.day
    shukkin_day = [date(year, month, day)]

    for j in range(1, 7):
        # 翌日を求める timedelta
        td = timedelta(days=j)
        # 基準日を 2020年2月28日とする
        d = date(year, month, day)
        shukkin_day.append(d+td)

    for i, url in enumerate([urls.index][0]):

        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.content, 'html.parser')

        names.append(soup.find(id='p_data').find('td').text)

        chapter = soup.find(id='girlprofile_sukkin')
        shukkin_time = []
        try:
            for item in chapter.find_all('li'):

                try:
                    shukkin_time.append(
                        ' '.join(item.text.strip().split()).split(' ', 1)[1])
                except:
                    shukkin_time.append(" ")
        except:

            shukkin_time = ['出', '勤', 'な', 'し', '', '', '']

        if df.columns.size == 0:
            df = pd.DataFrame(columns=shukkin_day)
        df.loc[i] = (shukkin_time)

    df.index = names
    df.to_csv('girl_collection.csv', encoding="shift-jis")
except:
    df = pd.DataFrame(columns=['error'])
    df.loc[0] = '作成者に問い合わせてください'
    df.to_csv('girl_collection.csv', encoding="shift-jis")
