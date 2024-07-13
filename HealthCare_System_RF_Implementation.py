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
img = Image.open('AIDScanner_Logo.png')

# Set the title page of the web app page
st.set_page_config(
    page_title='Healthcare System - Diabetes Diagnosis',
    page_icon=img
)

# Display the logo at the top of the page
st.image(img, width=150)
# Load models
rf = pickle.load(open('rf.sav', 'rb'))
gluco_dt = pickle.load(open('gluco_dt.sav', 'rb'))

# Set the side menu background color
st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: #13202c;
        }
    </style>
    """, unsafe_allow_html=True)
st.markdown("""
    <style>
        .eyeqlp51.st-emotion-cache-1pbsqtx.ex0cdmw0 {
            # visibility: hidden;
            visibility: hidden;
        }
        .st-emotion-cache-1wbqy5l {
            visibility: hidden;}
    #------------ Active menu colour change---------------
       .menu .nav-item .nav-link.active[data-v-5af006b8] {
    background-color: #199be7;
}     
    </style>
    """, unsafe_allow_html=True)
  #------------ Active menu colour change---------------
# Create a sidebar menu for the models
with st.sidebar:
    selection = option_menu('Menu',
                            ['How To Use','Get Glucose Level', 'BMI Calculation', 'Diabetes Diagnosis'],
                             default_index=0)
# Initialize bmi_value
bmi_value = 0
if selection == 'How To Use':
    st.write('Welcome to AIDScanner (Artificial Intelligence Diabetes Scanner) App.\
             This web application helps you understand your diabetes status \
            through various features. The app consists of four main sections, \
            accessible via the menu on the left side of the page:')
    lst = ['How to Use:\
           This guide explains how to navigate and utilize the app effectively.',
           'Get Glucose Level: Use this section to estimate your glucose level \
            if you do not know it. Input the required information, and\
            the app will compute it.', 'BMI Computation: \
            This tool calculates your Body Mass Index (BMI) if you do not know \
            it. Enter your height and weight, and the app will compute your BMI\
            for you.', 'Diabetes Diagnosis: This is the main feature of the app. \
            Here, you can get a diagnosis of your diabetes status based on the \
            information you provide. Follow the prompts to input your details \
            and receive an assessment.']

    for i in lst:
        st.markdown("- " + i)
           
# Glucose Computation
elif selection == 'Get Glucose Level':
    html_temp = """
    <div style="background:#13202c ;padding:10px">
    <h2 style="color:white;text-align:center;">Know Your Glucose Level</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    # Get user data for glucose estimation
    with col1:
        # Glucose = st.number_input('Glucose', min_value=0.0, key='Glucose')
        BloodPressure = st.number_input('Blood Pressure Level *', min_value=0.0, key='BloodPressure')

    with col2:
        BMI = st.number_input('Body Mass Index *', min_value=0.0, key='BMI')
        Age = st.number_input('Age *', min_value=16, key='Age')
    glucose_estimate = 0
    with col2:
        if st.button('Compute'):
            glucose_estimate = int(gluco_dt.predict([[BloodPressure, BMI, Age]]))
            # prediction = glucose

    with col1:
        st.success(glucose_estimate)


# BMI Computation
elif selection == 'BMI Calculation':
    # Give the page a title
    html_temp = """
    <div style="background:#13202c ;padding:10px">
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
    <div style="background:#13202c ;padding:10px">
    <h2 style="color:white;text-align:center;">Welcome to AIDScanner! </h2>
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
<div style="background:#13202c; padding:10px; margin-top:20px; border-top: 1px solid #ddd;">
<h4 style="color:#fff;text-align:center;">Disclaimer</h4>
<p style="color:#fff;text-align:center;">
This application predicts the likelihood of diabetes based on the given parameters.
However, it is not a substitute for professional medical advice, diagnosis, or treatment.
Always seek the advice of your physician or other qualified health providers with any questions you may have regarding diabetes.
</p>
</div>
"""
st.markdown(disclaimer_temp, unsafe_allow_html=True)
