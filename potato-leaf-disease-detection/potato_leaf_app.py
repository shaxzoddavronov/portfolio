import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image
model=tf.keras.models.load_model('potato-leaf-disease-detection/model.h5')
classes=['Potato Early blight', 'Potato Late blight', 'Potato healthy']
st.title('Potato Leaf Disease Prediction')



def get_result(image):
    if image:
        st.image(uploaded_img)
        img=Image.open(image).resize((224,224))
        img_arr=np.array(img).reshape(1,224,224,3)

        prediction=model.predict(img_arr)
        st.write('Result')
        st.success(classes[np.argmax(prediction)])
        st.write('Accuracy')
        st.info(f"{round(prediction.max(),2)*100}%")


selection=st.selectbox('Select Option',options=['Uploading Image','Using Camera'])
if selection=='Uploading Image':
    st.write('You should upload image ')
    uploaded_img=st.file_uploader('Upload Here',type=['png','jpg','jpeg'])
    get_result(uploaded_img)
else:
    st.write('You should take a leaf picture')    
    camera_img=st.camera_input('Take picture')
    get_result(camera_img)
