import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.image('perth-house-price-prediction/app/house.png')
st.title('Perth House Price Prediction')
st.subheader('Acknowledgements')
st.write("""This data was scraped from http://house.speakingsame.com/ and includes data from 322 Perth suburbs, 
         resulting in an average of about 100 rows per suburb.""")
st.subheader('Content')
st.write("""I believe the columns chosen to represent this dataset are the most crucial in predicting house prices. 
         Some preliminary analysis I conducted showed a significant correlation between each of these columns and 
         the response variable (i.e. price).""")
st.subheader('Data obtained from other than scrape source')
st.write("""Longitude and Latitude data was obtained from [data.gov.au](https://data.gov.au/data/dataset/geocoded-national-address-file-g-naf).
                
School ranking data was obtained from [bettereducation](https://bettereducation.com.au/Default.aspx).

The nearest schools to each address selected in this dataset are schools which are defined to be 'ATAR-applicable'. 
         In the Australian secondary school education system, ATAR is a scoring system used to assess a student's 
         culminative academic results and is used for entry into Australian universities. As such, schools which 
         do not have an ATAR program such as primary schools, vocational schools, special needs schools etc. 
         are not considered in determining the nearest school.
         
Do also note that under the "NEAREST_SCH_RANK" column, there are some missing rows as some schools are unranked according to 
         [this criteria](https://bettereducation.com.au/Results/WA/wace.aspx) by bettereducation.""")

df=pd.read_csv('perth-house-price-prediction/data/perth_house_price.csv')
df_prepared=pd.read_csv('perth-house-price-prediction/data/perth_house_prepared.csv',index_col=0)
st.subheader('Data')
st.dataframe(df)
st.subheader('Cleaned and Feature Engineering used data')
st.dataframe(df_prepared)
options_model={'XGB':'perth-house-price-prediction/models/XGB_model.jbl','Random Forest':'perth-house-price-prediction/models/RF_model.jbl',
               'Decision Tree':'perth-house-price-prediction/models/Tree_model.jbl'}
options={'XGB':'perth-house-price-prediction/predicted_data/XGB_prediction.csv','Random Forest':'perth-house-price-prediction/predicted_data/RF_prediction.csv',
         'Decision Tree':'perth-house-price-prediction/predicted_data/Tree_prediction.csv'}
model_name=st.selectbox('Input model type',options=options.keys())
index=st.number_input('Input index number',0,len(df_prepared))
def model_choose(options,model_name):   
    for option in options.keys():
        if model_name==option:
            df_pred=pd.read_csv(options[option],index_col=0)
            result=st.success(f"Predicted Price: {df_pred.iloc[index][0]}")
            st.info(f"Original Price: {df.iloc[index]['PRICE']}")
            #with open(options[option],'rb') as file:
            #model=joblib.load(file)
model_choose(options,model_name)
#page = st.sidebar.radio("Go to:", ("Home", "About", "Contact"))  

def filedownload(data):
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown("""[Original Data](filedownload(df),unsafe_allow_html=True)""")
st.markdown("""[Prepared Data](filedownload(df_prepared),unsafe_allow_html=True)""")

  
     
