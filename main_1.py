import streamlit as st
import base64
st.set_page_config(layout="wide", initial_sidebar_state='expanded')

query = '''
select
    *
from
    `jp-gs-379412.sevenrooms_covent_garden.reservation_feedback`
union all
select
    *
from
    `jp-gs-379412.sevenrooms_shoreditch.reservation_feedback`
union all
select
    *
from
    `jp-gs-379412.sevenrooms_kensington.reservation_feedback`
union all
select
    *
from
    `jp-gs-379412.sevenrooms_kings_cross.reservation_feedback`
union all
select
    *
from
    `jp-gs-379412.sevenrooms_edinburgh.reservation_feedback`
union all
select
    *
from
    `jp-gs-379412.sevenrooms_manchester.reservation_feedback`
union all
select
    *
from
    `jp-gs-379412.sevenrooms_birmingham.reservation_feedback`
union all
select
    *
from
    `jp-gs-379412.sevenrooms_canary_wharf.reservation_feedback`
union all
select
    *
from
    `jp-gs-379412.sevenrooms_permit_room_brighton.reservation_feedback`
'''
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

class GoogleBigQuery:
    def __init__(self):
        self.credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])

    def connect(self):
        self.client = bigquery.Client(credentials=self.credentials, project=self.credentials.project_id)
        return self.client
    
    def query(self, query = str, as_dataframe = True):
        with self.connect() as client:
            query_job = self.client.query(query)
            results = query_job.result()
            if as_dataframe:
                results = results.to_dataframe()
            return results

data = GoogleBigQuery().query(query)


st.sidebar.title('Reservation Feedbacks')
# transform data
data['received_date'] = pd.to_datetime(data['received_date'], dayfirst=True, format = 'mixed')
# filter data by date
start_date = st.sidebar.date_input('Start date', value=data['received_date'].min())
end_date = st.sidebar.date_input('End date', value=data['received_date'].max())
# get unique venues
venues =  data['venue'].unique().tolist() + ['All']
venue = st.sidebar.selectbox('Select venue', venues, index=len(venues)-1)

if venue != 'All':
    data = data[data['venue'] == venue]


st.subheader(f'**{venue}** - {start_date} {end_date}')
# transform data
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

data = data[(data['received_date'] >= start_date) & (data['received_date'] <= end_date)]

st.write(data)
st.write(f'{len(data)} reviews')


# create a download button
c1,c2 = st.columns(2)
st.sidebar.text_input('Rename your file', value=f'{venue} - {start_date.date()} {end_date.date()}', key='filename')
st.sidebar.download_button(
    label="Download data as CSV",
    data=data.to_csv().encode("utf-8"),
    file_name='data.csv',
    mime='text/csv',
    use_container_width=True
)
