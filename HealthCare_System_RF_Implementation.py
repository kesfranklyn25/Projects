# Load required libraries

# import numpy as np
import streamlit as st
import pickle
from streamlit_option_menu import option_menu
from PIL import Image
img = Image.open('salford.png')
# st.beta


# Set the title page of the web app page
st.set_page_config(
    page_title= 'Healthcare System - Diabetes Prediction',
    page_icon= img
    
    )
# Display the logo at the top of the page
st.image(img, width=150)
# Title page ends here
# Load models
rf = pickle.load(open('rf.sav','rb'))
# Models loading ends here.



# Hidden the visibilty of the deploy/share and the settings menu on the top right 
# corner of the web app page
st.markdown("""
            <style>
                .eyeqlp51.st-emotion-cache-1pbsqtx.ex0cdmw0
                { visibility: hidden;
                    }
                .st-emotion-cache-1wbqy5l{
                    visibility: hidden;
                    position: None;}
            </style>
            
            """, unsafe_allow_html=True)

# deploy/share and settings ends here

# set the side menu background color
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #40e0d0;
        

    }
</style>
""", unsafe_allow_html=True)
# side menu background color ends here

# Create a sidebar menu for the models
with st.sidebar:
    selection = option_menu('Menu', 
                            ['RF Prediction'],
                            icons = ['tree-fill'],
                            default_index = 0)
    st.write('Welcome to the Healthcare System - Diabetes Prediction application! \
             This app is designed to provide a quick and efficient way to assess \
             the likelihood of diabetes based on readily available health parameters. \
                 Our goal is to leverage advanced machine learning techniques to offer \
                     accurate predictions, helping individuals make informed decisions \
                         about their health..')
   
# sidebar menu creation ends here

# Code the different  models
if selection == 'RF Prediction':
    # Give the page a title
    # st.image(img, width=150)
    html_temp = """
    <div style="background:#40e0d0 ;padding:10px">
    <h2 style="color:white;text-align:center;">Diabetes Test </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html = True)
    col1, col2 = st.columns(2)
    # Get user data for prediction
    with col1:
        Glucose = st.number_input('Glucose Level', min_value=0, key='Glucose')
        BloodPressure = st.number_input('Blood Pressure Level', min_value=0, key='BloodPressure')

    with col2:
        BMI = st.number_input('Body Mass Index', min_value=0.0, key='BMI')
        Age = st.number_input('Patient Age', min_value=12, key='Age')

    prediction = ''
    with col2:
        if st.button('Outcome'):
            outcome = rf.predict([[Glucose, BloodPressure, BMI, Age]])
            if outcome[0] == 1:
                prediction = 'DIABETIC'
            else:
                prediction = 'NOT DIABETIC'
            
    with col1:
        st.success(prediction)


#  disclaimer 
disclaimer_temp = """
<div style="background:#f9f9f9; padding:10px; margin-top:20px; border-top: 1px solid #ddd;">
<h4 style="color:#333;text-align:center;">Disclaimer</h4>
<p style="color:#555;text-align:center;">
This application provides an estimation for the likelihood of diabetes based on the given parameters.
However, it is not a substitute for professional medical advice, diagnosis, or treatment.
Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
Do not disregard professional medical advice or delay in seeking it because of something you have read on this application.
Visit your hospital today to confirm your results. Thank you!
</p>
</div>
"""
st.markdown(disclaimer_temp, unsafe_allow_html=True)
