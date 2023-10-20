import streamlit as st
import joblib
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA 
st.set_page_config('Models')
st.title('Applying Model')
st.write('##')
#model_chosen=st.selectbox('Models',['KMeans','DBSCAN','MeanShift'])
model_path=f"/home/shaxzod/Downloads/KMeans.jbl"
pipe_path=f"/home/shaxzod/Downloads/pipeline.jbl"
#with open(model_path,'rb') as file:
model=joblib.load(model_path)
pipeline=joblib.load(pipe_path)

gender=st.selectbox('Input Gender (M-male,F-female)',['F','M'])
location=st.number_input('Location',0,9329)
balance=st.number_input('Account Balance',0.0,120000000.0)
transactionTime=st.number_input('Transaction Time',0)
transactionAmount=st.number_input('Transactiom Amount (INR)',0.0)
day_birth=st.number_input('Day Birth',0,31)
month_birth=st.number_input('Month Birth',1,12)
year_birth=st.number_input('Year Birth',1910,2000)
transactionDay=st.number_input('Transaction Day')
transactionMonth=st.selectbox('Transaction Month',['August','September','October'])
age=2016-year_birth
year_birth=[year_birth-1900 if year_birth<2000 else 0]

customer_data={'Gender':gender, 'Location':location, 'AccountBalance':balance, 'TransactionTime':transactionTime,
         'TransactionAmount (INR)':transactionAmount, 'Day_Birth':day_birth, 'Month_Birth':month_birth,
         'Year_Birth':year_birth, 'TransactionDay':transactionDay, 'TransactionMonth':transactionMonth, 'Age':age}
df_customer=pd.DataFrame(customer_data)
X=pipeline.transform(df_customer)
st.text(X)
pca=joblib.load('/home/shaxzod/Downloads/pca.jbl')
#n_components = min(X.shape[0], X.shape[1]-6)
X_prepared=pca.transform(X)
st.text(X_prepared)
result=model.predict(X_prepared)
st.success(result)
#st.text(customer_data)

