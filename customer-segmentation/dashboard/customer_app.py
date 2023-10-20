import streamlit as st
import numpy as np
import pandas as pd
import requests
from streamlit_lottie import st_lottie
st.set_page_config(page_title='HomePage',page_icon='&#9883',layout='wide')

def get_lottie(url):
       lot_r=requests.get(url)
       if lot_r.status_code!=200:
              return None
       return lot_r.json()
lottie_code=get_lottie('https://lottie.host/e1369326-c49d-4221-8d74-917f436dc90f/sHVqNSIb7s.json')

with st.container(): 
       st.title('Bank Customer Segmentation (1M+ Transactions)')
       st.write('##')
       st.write('--- ')
       left_col,right_col=st.columns(2)
       with left_col:
              st.subheader('About Dataset')
              st.write('#')
              st.write("""
                     Bank Customer Segmentation:
                     - Most banks have a large customer base - with different characteristics in terms of age, 
                     income, values, lifestyle, and more. \n 
                     Customer segmentation is the process of dividing 
                     a customer dataset into specific groups based on shared traits.
                     - According to a report from Ernst & Young, “A more granular understanding of consumers is 
                     no longer a nice-to-have item, \n 
                     but a strategic and competitive imperative for banking providers.
                     Customer understanding should be a living, breathing \n
                     part of everyday business, with insights 
                     underpinning the full range of banking operations.
                    
                            """)
              st.write('#')
              st.write("""
                     About this Dataset:
                     - This dataset consists of 1 Million+ transaction by over 800K customers for a bank in India. 
                     The data contains information \n 
                     such as - customer age (DOB), location, gender, account balance at 
                     the time of the transaction, transaction details, transaction amount, etc. 
                     
                     """)

       with right_col:
              st_lottie(lottie_code,height=600,key='coding')

st.write('---')
data=pd.read_csv('/home/shaxzod/Data Science App/Customer Segmentation app/Application/bank_transactions.csv')
st.dataframe(data,use_container_width=True)