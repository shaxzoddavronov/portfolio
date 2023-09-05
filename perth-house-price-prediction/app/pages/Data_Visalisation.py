import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

df=pd.read_csv('perth-house-price-prediction/data/perth_house_prepared.csv',index_col=0)
st.header('Price Trending')
options=['min','max','mean']
color_codes=['b','r','o']
def build_year_graph(option,data=df):
    st.subheader(f"{option.title()} in Years")
    if option=='min':        
        build_year_data=df.groupby('Build_Year').Price.min()
        st.line_chart(build_year_data)
        
    elif option=='max':   
        build_year_data=df.groupby('Build_Year').Price.max()
        st.line_chart(build_year_data)
    else:
        build_year_data=df.groupby('Build_Year').Price.mean()
        st.line_chart(build_year_data) 
 
for option in options:
    build_year_graph(option)      

st.subheader('Interactive Statistics')    
st.write('Here you can see which government area the houses sold in different years belong to')
alt.data_transformers.enable('default', max_rows=40000) 
scale=alt.Scale(domain=df.Govern_Area.unique().tolist(),
                range=['#641e16','#512e5f','#154360','#0e6251','#145a32','#7d6608',
                       '#784212','#7b7d7d','#4d5656','#212f3c','#c0392b','#9b59b6',
                       '#2980b9','#5dade2','#1abc9c','#27ae60','#f4d03f','#f5b041',
                       '#f0b27a','#34495e','#4649ff','#f394e6','#ff4141','#cb41ff',
                       '#0df411','ffaa4f','9f76ff','#fffb71','#44e66e',' #23edcb'
                      ])
color=alt.Color('Govern_Area:O',scale=scale)

brush=alt.selection_interval(encodings=['x'])
click=alt.selection_point(encodings=['color'])

points=alt.Chart().mark_point().encode(
    alt.X('Date_Sold:N',title='Date'),
    alt.Y('Price:Q',title='House Price',
          scale=alt.Scale(domain=[50000,2500000])),
    color=alt.condition(brush,color,alt.value('lightgray')),
    size=alt.Size('Home_Age:Q',scale=alt.Scale(domain=[5,154]))    
).properties(
width=500,height=300
).add_params(
    brush
).transform_filter(
    click
)

bars=alt.Chart().mark_bar().encode(
    x='count()',
    y='Govern_Area:N',
    color=alt.condition(click,color,alt.value('lightgray'))
).transform_filter(
brush
).properties(
width=450).add_params(
click
)

chart=alt.vconcat(points,bars,data=df,title=' Interactive Statistics')

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Altair native theme"])

with tab1:
    st.altair_chart(chart, theme="streamlit", use_container_width=True)
with tab2:
    st.altair_chart(chart, theme=None, use_container_width=True)
