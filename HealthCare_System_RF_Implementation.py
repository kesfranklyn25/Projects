# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 16:47:02 2024

@author: KesBes
"""

# Load required libraries
import streamlit as st
import pickle
from streamlit_option_menu import option_menu
from PIL import Image

# Load the image
img = Image.open('salford.png')

# Set the title page of the web app page
st.set_page_config(
    page_title='Healthcare System - Diabetes Diagnosis',
    page_icon=img
)

# Display the logo at the top of the page
st.image(img, width=150)

# Load models
rf = pickle.load(open('rf.sav', 'rb'))

# Hide the visibility of the deploy/share and the settings menu on the top right
# corner of the web app page
st.markdown("""
    <style>
        .eyeqlp51.st-emotion-cache-1pbsqtx.ex0cdmw0 {
            visibility: hidden;
        }
        .st-emotion-cache-1wbqy5l {
            visibility: hidden;
            position: None;
        }
    </style>
    """, unsafe_allow_html=True)

# Set the side menu background color
st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: #40e0d0;
        }
    </style>
    """, unsafe_allow_html=True)

# Create a sidebar menu for the models
with st.sidebar:
    selection = option_menu('Menu',
                            ['BMI Computation', 'Diabetes Diagnosis'],
                            icons=['tree-fill'],
                            default_index=1)
    st.write('Welcome to the Healthcare System - Diabetes Prediction application! \
             This app is designed to provide a quick and efficient way to assess \
             the likelihood of diabetes based on readily available health parameters. \
             Our goal is to leverage advanced machine learning techniques to offer \
             accurate predictions, helping individuals make informed decisions \
             about their health.')

# Initialize bmi_value
bmi_value = 0

# BMI Computation
if selection == 'BMI Computation':
    # Give the page a title
    html_temp = """
    <div style="background:#40e0d0 ;padding:10px">
    <h2 style="color:white;text-align:center;">Body Mass Index Computation</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    # Get user data for prediction
    with col1:
        weight = st.number_input('Weight(kg)', min_value=0.0, key='weight')
    with col2:
        height = st.number_input('Height(m)', min_value=1.0, key='height')
    with col2:
        if st.button('Compute'):
            bmi_value = round(weight / (height * height), 2)
    with col1:
        st.success(bmi_value)
# Code the different models

else:
    # Give the page a title
    html_temp = """
    <div style="background:#40e0d0 ;padding:10px">
    <h2 style="color:white;text-align:center;">Diabetes Test </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    # Get user data for prediction
    with col1:
        Glucose = st.number_input('Glucose', min_value=0.0, key='Glucose')
        BloodPressure = st.number_input('Blood Pressure Level *', min_value=0.0, key='BloodPressure')

    with col2:
        BMI = st.number_input('Body Mass Index *', min_value=0.0, key='BMI')
        Age = st.number_input('Age *', min_value=16, key='Age')

        if BMI == 0:
            BMI = bmi_value

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

# Disclaimer
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
