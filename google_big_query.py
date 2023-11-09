from google.cloud import bigquery
from google.oauth2 import service_account
import streamlit as st
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