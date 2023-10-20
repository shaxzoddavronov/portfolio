import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import plotly.express as px
st.set_page_config(page_title='Visualization',layout='wide')

df=pd.read_csv('/home/shaxzod/Data Science App/Customer Segmentation app/Application/bank_transactions.csv')    
df.TransactionDate=pd.to_datetime(df['TransactionDate'],format="%d/%m/%y")
val_1=st.sidebar.slider('Customer Balance',df.CustAccountBalance.min(),df.CustAccountBalance.max(),value=df.CustAccountBalance.max())
val_2=st.sidebar.slider('Transaction Time',df.TransactionTime.min(),df.TransactionTime.max(),value=df.TransactionTime.max())
val_3=st.sidebar.slider('Transaction Amount (INR)',df['TransactionAmount (INR)'].min(),df['TransactionAmount (INR)'].max(),value=df['TransactionAmount (INR)'].max())
location=df.CustLocation.value_counts()
val_4=st.sidebar.multiselect('Locations',location[location>10000].index.values,location[location>10000].index.values)
df=df[(df.CustAccountBalance<=val_1)&(df.TransactionTime<=val_2)&(df['TransactionAmount (INR)']<=val_3)&(df.CustLocation.isin(val_4))]

def data_by_gender(gender):
       data=df[df.CustGender==gender].iloc[:,5:].groupby('TransactionDate').mean().reset_index().sort_values(by='TransactionDate')
       data.columns=data.columns+'_'+gender
       return data
df_male=data_by_gender('M')
df_female=data_by_gender('F')
df_gender=pd.concat([df_male,df_female],axis=1)

left_column,right_column=st.columns(2)
left_column.subheader('Daily Transaction Time')
right_column.subheader('Customer Balance Amount')
with left_column:
       st.line_chart(df_gender,x='TransactionDate_M',y=['TransactionTime_M','TransactionTime_F'],color=['#202CFF','#F70D1A'],
              width=600,height=400)
with right_column:
       st.line_chart(df_gender,x='TransactionDate_M',y=['CustAccountBalance_M','CustAccountBalance_F'],color=['#202CFF','#F70D1A'],
              width=600,height=400)
st.subheader('Daily Transaction Amount (INR)')
st.line_chart(df_gender,x='TransactionDate_M',y=['TransactionAmount (INR)_M','TransactionAmount (INR)_F'],color=['#202CFF','#F70D1A'],
              width=500,height=350)
df_bar_gender=pd.DataFrame(df[df['CustGender']!='T'].CustGender.value_counts())
df_bar_gender.rename(index={'F':'Female','M':'Male'},inplace=True)
#fig=px.bar(df_bar_gender)
#st.plotly_chart(fig, theme="streamlit", use_container_width=True)
left_column,right_column=st.columns(2)
with left_column:
       st.subheader('Male-Female Count',divider='orange')
       st.bar_chart(data=df_bar_gender,y='count',color=['#F4FA58'],height=370)
cust_location=df.CustLocation.value_counts()
cust_location=cust_location[cust_location>10000]
with right_column:
       st.subheader('Here is a location plot with more than 10,000 customers',divider='orange')
       st.bar_chart(cust_location,height=400)

