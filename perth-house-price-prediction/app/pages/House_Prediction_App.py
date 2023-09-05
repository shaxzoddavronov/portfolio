import streamlit as st
import pandas as pd
import numpy as np
from About import model_choose
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import joblib
st.title(' House Price Prediction App')
pipeline=joblib.load('perth-house-price-prediction/app/pipeline.jbl')
st.write('You should enter some information about house')
X_data=pd.read_csv('perth-house-price-prediction/app/pages/data_X.csv',index_col=0)
#replace_values={7:'SENIOR HIGH SCHOOL',6:'SCHOOl',1:'ALTA-1',3:'COLLEGE',5:'HIGH SCHOOL',2:'CAMPUS',4:'GRAMMAR'}
#X_data.School_type=X_data.School_type.map(replace_values)
title_names=['Suburb', 'Bedrooms', 'Bathrooms', 'Garage', 'Land Area','Floor Area', 'Year Built', 
             'Cbd Distance', 'Nearest Station','Nearest Stn Distance', 'Date Sold', 'Latitude', 'Longitude',
             'Nearest School', 'Nearest School Distance', 'School type', 'Government Area','Remain Area', 
             'Price per Area', 'Home Age', 'Rooms']
columns=X_data.columns.tolist()
house_data=[]
for column in columns:
    if X_data[column].dtype=='object':
        data=st.selectbox(title_names[columns.index(column)],options=X_data[column].unique())
    else:
        data=st.number_input(title_names[columns.index(column)],X_data[column].min(),X_data[column].max())        
    house_data.append(data)
house_table=pd.DataFrame(np.array([house_data]),columns=columns)    

st.write('Check your data')
st.dataframe(house_table)

#house_table=house_table[]

options_model={'XGB':'perth-house-price-prediction/models/XGB_model.jbl','Random Forest':'perth-house-price-prediction/models/RF_model.jbl',
               'Decision Tree':'perth-house-price-prediction/models/Tree_model.jbl'}
model_chosen=st.selectbox('Choose model',options=['XGB','Random Forest','Decision Tree'])
st.button('Reset',type='primary')
if st.button('Show result'):
    model=joblib.load(options_model[model_chosen])
    prepared_data=pipeline.transform(house_table[columns])
    st.success(model.predict(prepared_data))
