import streamlit as st
import sklearn
import spacy
import joblib

nlp=spacy.load('en_core_web_md')
def preprocess_vectorize(text):
    doc=nlp(text)
    non_stopped=[token.lemma_ for token in doc if  not token.is_stop and not 
                 token.is_punct and not token.like_num]
    non_stop_text=' '.join(non_stopped)
    doc_non_stop=nlp(non_stop_text)
    not_oov_text=[token.lemma_ for token in doc_non_stop if not token.is_oov]
    prep_text=' '.join(not_oov_text)
    vectorizer=joblib.load('Tf_Idf_vectorizer.jbl')
    return vectorizer.transform([prep_text]) 

st.image('sentiment.png')
st.title('Financial News Sentiment Analysis')
st.write('In the app, you can get prediction of financial news sentiment with different Machine Learning models')
#model_types=['Random Forest','Random Forest (gensim)','Logistic Regression','XGBoost',
             #'XGBoost (gensim)','Support Vector Machine','Support Vector Machine (gensim)']
model_files={'Random Forest':'RandomForest.jbl','Logistic Regression':'Logistic.jbl','XGBoost':'XGboost.jbl'}
chosen_model=st.selectbox('Select model',model_files.keys())
model=joblib.load(model_files[chosen_model])
text=st.text_area('Enter financial news related text')
text_vector=preprocess_vectorize(text)
#predicted=model.predict()
if st.button('Get Result'):
    result=model.predict(text_vector)
    if result==0: st.success('Negative')
    elif result==1: st.success('Normal')
    else: st.success('Positive')
