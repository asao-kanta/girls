import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date, timedelta, datetime
import numpy as np

import streamlit as st
from streamlit_modal import Modal
from streamlit import session_state as state

headers = {"User-Agent":
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
urls = pd.read_csv('url.csv', index_col=0, header=None)
print(urls)
if "urls" not in state:
    state.urls = [url for url in [urls.index][0]]
if "index" not in state:
    state.index = 0

names = []
df = pd.DataFrame()

today = datetime.today()
year, month, day = today.year, today.month, today.day
shukkin_day = [date(year, month, day)]

for j in range(1, 7):
    # 翌日を求める timedelta
    td = timedelta(days=j)
    # 基準日を 2020年2月28日とする
    d = date(year, month, day)
    shukkin_day.append(d+td)

for i, url in enumerate(state.urls):
    print(type(url))
    if url == "" or url is None or type(url) != str or url == "nan":
        continue
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
st.dataframe(df)

modal = Modal(key="Demo Key", title="test")
if modal.is_open():
    with modal.container():
        # st.text_input(label="urls", key=1)
        for i in range(len(state.urls)):
            state.urls[i] = st.text_input(
                label="url", value=state.urls[i], key=i)
            if st.button("delete", key=f"delete{i}"):
                state.urls.pop(i)
        if st.button("add"):
            state.urls.append("")
        if st.button("close"):
            pd.DataFrame(state.urls).to_csv(
                'url.csv', header=False, index=False)
            modal.close()


open_modal = st.button("Open")
if open_modal:
    modal.open()

print(state.urls)
