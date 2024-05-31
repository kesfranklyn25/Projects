# Load required libraries

# import numpy as np
import streamlit as st
import pickle
from streamlit_option_menu import option_menu

# Load models

dt = pickle.load(open('Healthcare/dt.sav','rb'))
rf = pickle.load(open('Healthcare/rf.sav','rb'))
svm = pickle.load(open('Healthcare/svm.sav','rb'))

# Models loading ends here.

# Set the title page of the web app page
st.set_page_config(
    page_title= 'Healthcare System - Diabetes Prediction',
    page_icon='tree-fill'
    
    )
# Title page ends here

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
        .menu .nav-item .nav-link.active[data-v-5af006b8]
        background-color: #40e0d0;
        }
            

    }
</style>
""", unsafe_allow_html=True)
# side menu background color ends here

# Create a sidebar menu for the models
with st.sidebar:
    selection = option_menu('Menu', 
                            ['DT Prediction',
                            'RF Prediction',
                            'SVM Prediction'],
                            icons = ['tree', 'tree-fill', 'activity'],
                            default_index = 0)
    st.write('This app was developed for the prediction of diabetes given the relevant \
             parameters. Machine learning algorithms used in the implementation of this\
            app are Decision tree, Random forest and Support vector machine')
# sidebar menu creation ends here

# Code the different  models
if selection == 'DT Prediction':
    # Give the page a title
    # st.title('ML- Prediction Using Decision Tree')
    html_temp = """
    <div style="background:#40e0d0 ;padding:10px">
    <h2 style="color:white;text-align:center;">Decision Tree Prediction </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html = True)
    col1, col2 = st.columns(2)
    # Get user data for prediction
    with col1:
        
        Pregnancies = st.text_input('No of Pregnacies', placeholder = 'Enter an interger value', key ='Pregnancies')
        Glucose = st.text_input('Glucose Level', placeholder = 'Enter glucose level', key = 'Glucose')
        BloodPressure = st.text_input('Blood Pressure Level', placeholder = 'Enter blood pressure reading', key = 'BloodPressure')
        SkinThickness = st.text_input('SkinThickness', placeholder = 'Skin Thickness', key = 'SkinThickness')
    with col2:
        

        Insulin = st.text_input('Insulin',placeholder = 'Enter Insulin Level', key = 'Insulin')
        BMI = st.text_input('Body Mass Index',placeholder = 'BMI value', key = 'BMI')
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function',placeholder = 'DPF', key = 'DiabetesPedigreeFunction')
        Age = st.text_input('Patient Age',placeholder = "Patient\'s age", key = 'Age')

    prediction = ''
    with col2:
        if st.button('Diabetes Test Result'):
            outcome = dt.predict([[Pregnancies,Glucose,BloodPressure,SkinThickness,
                          Insulin,BMI,DiabetesPedigreeFunction,
                          Age]])
            if outcome[0] == 1:
                prediction = 'DIABETIC'
            else:
                prediction = 'NOT DIABETIC'
            
    with col1:
        st.success(prediction)

elif selection == 'RF Prediction':
    # Give the page a title
    html_temp = """
    <div style="background:#40e0d0 ;padding:10px">
    <h2 style="color:white;text-align:center;">Random Forest Prediction </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html = True)
    col1, col2 = st.columns(2)
    # Get user data for prediction
    with col1:
        
        Pregnancies = st.text_input('No of Pregnacies', placeholder = 'Enter an interger value', key ='Pregnancies')
        Glucose = st.text_input('Glucose Level', placeholder = 'Enter glucose level', key = 'Glucose')
        BloodPressure = st.text_input('Blood Pressure Level', placeholder = 'Enter blood pressure reading', key = 'BloodPressure')
        SkinThickness = st.text_input('SkinThickness', placeholder = 'Skin Thickness', key = 'SkinThickness')
    with col2:
        

        Insulin = st.text_input('Insulin',placeholder = 'Enter Insulin Level', key = 'Insulin')
        BMI = st.text_input('Body Mass Index',placeholder = 'BMI value', key = 'BMI')
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function',placeholder = 'DPF', key = 'DiabetesPedigreeFunction')
        Age = st.text_input('Patient Age',placeholder = "Patient\'s age", key = 'Age')

    prediction = ''
    with col2:
        if st.button('Diabetes Test Result'):
            outcome = rf.predict([[Pregnancies,Glucose,BloodPressure,SkinThickness,
                          Insulin,BMI,DiabetesPedigreeFunction,
                          Age]])
            if outcome[0] == 1:
                prediction = 'DIABETIC'
            else:
                prediction = 'NOT DIABETIC'
            
    with col1:
        st.success(prediction)

else:
    # Give the page a title
    html_temp = """
    <div style="background:#40e0d0 ;padding:10px">
    <h2 style="color:white;text-align:center;">Support Vector Machine Prediction </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html = True)
    col1, col2 = st.columns(2)
    # Get user data for prediction
    with col1:
        
        Pregnancies = st.text_input('No of Pregnacies', placeholder = 'Enter an interger value', key ='Pregnancies')
        Glucose = st.text_input('Glucose Level', placeholder = 'Enter glucose level', key = 'Glucose')
        BloodPressure = st.text_input('Blood Pressure Level', placeholder = 'Enter blood pressure reading', key = 'BloodPressure')
        SkinThickness = st.text_input('SkinThickness', placeholder = 'Skin Thickness', key = 'SkinThickness')
    with col2:
        

        Insulin = st.text_input('Insulin',placeholder = 'Enter Insulin Level', key = 'Insulin')
        BMI = st.text_input('Body Mass Index',placeholder = 'BMI value', key = 'BMI')
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function',placeholder = 'DPF', key = 'DiabetesPedigreeFunction')
        Age = st.text_input('Patient Age',placeholder = "Patient\'s age", key = 'Age')

    prediction = ''
    with col2:
        if st.button('Diabetes Test Result'):
            outcome = svm.predict([[Pregnancies,Glucose,BloodPressure,SkinThickness,
                          Insulin,BMI,DiabetesPedigreeFunction,
                          Age]])
            if outcome[0] == 1:
                prediction = 'DIABETIC'
            else:
                prediction = 'NOT DIABETIC'
            
    with col1:
        st.success(prediction)
# the different  models coding ends here
