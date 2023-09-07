import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date, timedelta, datetime
import numpy as np
import boto3
import os
from io import StringIO

import streamlit as st
from streamlit_modal import Modal
from streamlit import session_state as state
from logging import getLogger
logger = getLogger(__name__)
logger.info('message')

access_key = os.environ["AWS_ACCESS_KEY"]
secret_key = os.environ["AWS_SECRET_ACCESS_KEY"]

client = boto3.client('s3')

Filename = 'url.csv'
Bucket = 'arabum-girls'
client = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name='ap-northeast-1'
)

csv = client.get_object(Bucket=Bucket, Key=Filename)
csv_buf = StringIO()
# logger.info(csv)

csv_file = client.get_object(Bucket=Bucket, Key=Filename)
st.write(csv_file)
csv_file_body = csv_file["Body"].read().decode("utf-8")
st.write(csv_file_body)
st.write(csv_file_body.split())
# print(type(csv_file_body))

# urls = pd.read_csv(csv, index_col=0, header=None)
# urls = pd.read_csv(StringIO(csv_file_body), index_col=0, header=None)
# st.write(urls)
headers = {"User-Agent":
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

if "urls" not in state:
    state.urls = [url for url in csv_file_body.split()]
if "index" not in state:
    state.index = 0
logger.info(state.urls)
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
    if url == "" or url is None or type(url) != str or url == "nan" or url == "NoneType" or type(url) == "NoneType":
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
                csv_buf, header=False, index=False)
            client.put_object(Bucket=Bucket,
                              Body=csv_buf.getvalue(), Key=Filename)
            modal.close()


open_modal = st.button("Open")
if open_modal:
    modal.open()

print(state.urls)
