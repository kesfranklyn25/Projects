# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 18:30:52 2024

@author: KesBes
"""

import streamlit as st
from streamlit_option_menu import option_menu
import pyodbc
from datetime import datetime
from PIL import Image

# -------------------------Load the Logo----------------------------------

img = Image.open('C:/Users/Fatima/Desktop/Emro/kescare_logo.png')

# -------------------------Load the Logo----------------------------------


# ------------------------Page Title--------------------------------------
st.set_page_config(
    page_title='Hospital Registration System',
    page_icon=img,
    layout="wide"  # for better responsiveness layout
)

# ------------------------Page Title--------------------------------------

# --------------------------App Logo--------------------------------------
# Display the logo at the top of the page
st.text('')
st.text('')
st.text('')
st.image(img, width=150)

# --------------------------App Logo--------------------------------------
# -------------------------Database Connetion----------------------------------


# @st.cache_resource
def init_connection():
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={st.secrets['database']['server']};"
        f"DATABASE={st.secrets['database']['database']};"
        f"UID={st.secrets['database']['username']};"
        f"PWD={st.secrets['database']['password']}"
    )
    return pyodbc.connect(connection_string)

conn = init_connection()

# Function to insert data into the database
def insert_data(action, *args):
    cursor = conn.cursor()
    if action == 'Registration':
        cursor.execute("""
            INSERT INTO tblPATIENT(PATID,FName, LName, MName, Gender, MStatus,\
            StateOfOrigin, DateOfBirth, PhoneNo, EmailAddress) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?)
        """, args)
    elif action == 'Contact Details':
        cursor.execute("""
            INSERT INTO tblAddress (PATID, HouseNo, StreetName, City, State, PostCode, Country) 
            VALUES (?, ?, ?,?, ?, ?, ?)
        """, args)
        
    elif action == 'Next of Kin Details':
        cursor.execute("""
            INSERT INTO tblNEXTOFKIN ('Next of Kin Details',PATID,nxtFName, nxtLName, nxtRelationship, nxtEmailAddress, nxtPhoneNo) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, args)
        
        # cursor.execute("""
        #     INSERT INTO tblREGISTRATION (PATID,RegDate, CardClass, CardType) 
        #     VALUES (?, ?, ?, ?)
        # """, args)
        # PATID						
    conn.commit()
    cursor.close()
    # conn.close()
    
# --------------------------Database Connection Ends--------------------------------
# ----------------------------Patient Registration-----------------------------
# # --------------------------Default Page Patient's Details------------------------------
# ----------------------------Generate Patient's ID----------------------------
# Function to generate custom PATID
# def generate_patient_id():
#     now = datetime.now()
#     month = now.strftime("%m")
#     year = now.strftime("%Y")
    
#     # Get the last inserted integer from the database for today
#     cursor = conn.cursor()
#     cursor.execute(f"SELECT MAX(PATID) FROM tblPATIENT WHERE PATID LIKE 'SC/{month}/{year}/%'")
#     last_id = cursor.fetchone()[0]
    
#     # Extract the last integer from the PATID if available
#     if last_id is None:
#         new_integer = 1  # Start at 1 if no records found
#     else:
#         # Split to get the last part of the PATID and increment it
#         new_integer = int(last_id.split('/')[-1]) + 1
    
#     # Construct the new PATID
#     new_patid = f"CBH/{month}/{year}/{new_integer}"
    
#     return new_patid

# Function to generate custom PATID
def generate_patient_id(card_type):
    """
    Generates a patient ID based on the card type.
    For Family Card: FC/integer/mm/yyyy
    For Single Card: SC/integer/mm/yyyy
    
    Parameters:
    card_type (str): Either 'FC' for Family Card or 'SC' for Single Card.
    
    Returns:
    str: The generated patient ID.
    """
    now = datetime.now()
    month = now.strftime("%m")
    year = now.strftime("%Y")

    # Ensure the card_type is valid
    if card_type not in ['FC', 'SC']:
        raise ValueError("Invalid card type. Use 'FC' for Family Card or 'SC' for Single Card.")
    
    # Get the last inserted integer for the given card type
    cursor = conn.cursor()
    cursor.execute(f"SELECT MAX(PATID) FROM tblPATIENT WHERE PATID LIKE '{card_type}/%/{month}/{year}'")
    last_id = cursor.fetchone()[0]
    
    # Extract the last integer from the PATID if available
    if last_id is None:
        new_integer = 1  # Start at 1 if no records found
    else:
        # Split to get the last part of the PATID and increment it
        new_integer = int(last_id.split('/')[1]) + 1  # Extract integer part and increment
    
    # Construct the new PATID based on the card type
    new_patid = f"{card_type}/{new_integer}/{month}/{year}"
    
    return new_patid

# Example Usage:
# For Family Card
# family_card_id = generate_patient_id('FC')
# print(f"Family Card ID: {family_card_id}")

# # For Single Card
# single_card_id = generate_patient_id('SC')
# print(f"Single Card ID: {single_card_id}")


# -------------------------Database Connetion----------------------------------

# Initialize session state for form data if not already initialized
if 'form_data' not in st.session_state:
    st.session_state.form_data = {
        'FName': '',
        'LName': '',
        'MName': '',
        'Gender': '',
        'MStatus': '',
        'StateOfOrigin': '',
        'DateOfBirth': datetime.today(),
        'PhoneNo': '',
        'EmailAddress': '',
        'NxtFName': '',
        'NxtLName': '',
        'NxtPhoneNo': '',
        'NxtRelationship': '',
        'NxtEmailAddress': '',
        'HouseNo': '',
        'StreetName':'',
        'City': '',
        'State': '',
        'PostCode':'',
        'Country': '',
        'CardType':'',
        'CardClass':''
        
    }


# --------------------------Sidebar Colour--------------------------------
st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: #000080;
        }
        .st-emotion-cache-1wbqy5l {
            visibility: hidden;
        }
        .block-container {
            padding-top: 1rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
# -----------------------------Sidebar Colour----------------------------------

# Sidebar Menu for Navigation
with st.sidebar:
    menu = option_menu(
        'Registration Menu',
        ['ChristBay', 'Registration'],
        default_index=0
    )
# ----------- PAGE 1: Welcome Page -----------
if menu == 'ChristBay':
    st.header("Welcome to ChristBay Hospital")
    
    st.write("""
    **ChristBay Hospital** is dedicated to providing top-notch medical services.
    You can register patients using this application. Follow the steps to complete the patient registration process.
    """)

# ----------- PAGE 2: Registration Page -----------
elif menu == 'Registration':
    # Create tabs for the registration sub-pages
    tab1, tab2, tab3 = st.tabs(["Personal Details", "Contact Details", "Next of Kin Details"])

    # ----------- Tab 1: Personal Details -----------
    with tab1:
        st.header("Patient Personal Information")
        
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.form_data['FName'] = st.text_input('First Name:*', value=st.session_state.form_data['FName'])
            st.session_state.form_data['LName'] = st.text_input('Last Name:*', value=st.session_state.form_data['LName'])
            st.session_state.form_data['MName'] = st.text_input('Middle Name:', value=st.session_state.form_data['MName'])
            st.session_state.form_data['Gender'] = st.text_input('Gender:', value=st.session_state.form_data['Gender'])
            st.session_state.form_data['MStatus'] = st.text_input('Marital Status:', value=st.session_state.form_data['MStatus'])

        with col2:
            st.session_state.form_data['StateOfOrigin'] = st.text_input('State of Origin:*', value=st.session_state.form_data['StateOfOrigin'])
            st.session_state.form_data['DateOfBirth'] = st.date_input('Date of Birth:*', value=st.session_state.form_data['DateOfBirth'])
            st.session_state.form_data['PhoneNo'] = st.text_input('Phone Number:', value=st.session_state.form_data['PhoneNo'])
            st.session_state.form_data['EmailAddress'] = st.text_input('Email Address:', value=st.session_state.form_data['EmailAddress'])
            st.session_state.form_data['CardClass'] = st.selectbox('Class of Card:*', ['SC', 'FC'], key='CardClass')
            if st.button('Next'):
                PATID = generate_patient_id(st.session_state.form_data['CardClass'])
                st.session_state.form_data['PATID'] = PATID
                insert_data('Registration', st.session_state.form_data['PATID'],\
                            st.session_state.form_data['FName']\
                            , st.session_state.form_data['LName'], \
                            st.session_state.form_data['MName'], \
                            st.session_state.form_data['Gender'],\
                            st.session_state.form_data['MStatus'],\
                            st.session_state.form_data['StateOfOrigin'],\
                            st.session_state.form_data['DateOfBirth'],\
                            st.session_state.form_data['PhoneNo'],\
                            st.session_state.form_data['EmailAddress'])
                st.write('Details saved successfully. Enter Contact details')
# --------------------------------Contact Details------------------------------

# --------------------------Next of Kin's Details------------------------------
        with tab2:
            st.header("Patient Contact Details")
            
            col1, col2 = st.columns(2)
            with col1:          
                st.session_state.form_data['HouseNo'] = st.text_input('House Number:', value =st.session_state.form_data['HouseNo'])
                st.session_state.form_data['StreetName'] = st.text_input('Street Name:', value=st.session_state.form_data['StreetName'])
                st.session_state.form_data['City'] = st.text_input('City:', value=st.session_state.form_data['City'])
                
        
            with col2:
                st.session_state.form_data['State'] = st.text_input('State:', value=st.session_state.form_data['State'])
                st.session_state.form_data['PostCode'] = st.text_input('Postal Code:*', value=st.session_state.form_data['PostCode'])
                st.session_state.form_data['Country'] = st.text_input('Country:*', value=st.session_state.form_data['Country'])
                if st.button('Save Contact'):
                    insert_data('Contact Details', st.session_state.form_data['PATID'],\
                                st.session_state.form_data['HouseNo'],\
                                st.session_state.form_data['StreetName'],\
                                st.session_state.form_data['City'],\
                                st.session_state.form_data['State'],\
                                st.session_state.form_data['PostCode'],\
                                st.session_state.form_data['Country'])
                    st.write('Contact saved successfully. Continue on the Next of Kin tab')
# --------------------------------Contact Details------------------------------
        with tab3:
            st.header("Patient Next of Kin Information")
            
            col1, col2 = st.columns(2)
            with col1:
                # st.session_state.form_data['PATID'] = st.session_state.form_data['FName'] 
                st.session_state.form_data['NxtFName'] = st.text_input('Next of Kin First Name:', value =st.session_state.form_data['NxtFName'])
                st.session_state.form_data['NxtLName'] = st.text_input('Next of Kin Last Name:', value =st.session_state.form_data['NxtLName'])
                st.session_state.form_data['NxtRelationship'] = st.text_input('Relationship:', value=st.session_state.form_data['NxtRelationship'])
                
                

            with col2:
                st.session_state.form_data['NxtEmailAddress'] = st.text_input('Next of Kin Email ID:', value=st.session_state.form_data['NxtEmailAddress'])
                st.session_state.form_data['NxtPhoneNo'] = st.text_input('Next of Kin Phone No:*', value=st.session_state.form_data['NxtPhoneNo'])
                st.session_state.form_data['CardType'] = st.selectbox('Type of Card:*', ['HMO', 'Individual'], key='CardType')
                if st.button('Submit'):
                    # PATID = generate_patient_id(st.session_state.form_data['CardClass'])
                    insert_data('Next of Kin Details', st.session_state.form_data['PATID'],\
                                st.session_state.form_data['NxtFName'],\
                                st.session_state.form_data['NxtLName'],\
                                st.session_state.form_data['NxtRelationship'],\
                                st.session_state.form_data['NxtEmailAddress'],\
                                st.session_state.form_data['NxtPhoneNo'])
                    
                    # insert_data('Next of Kin Details', st.session_state.form_data['PATID'],\
                    #             datetime.today(),st.session_state.form_data['CardClass'],\
                    #             st.session_state.form_data['CardType'])    
                    print(f'Contact saved successfully. Patient Registration number is {st.session_state.form_data["PATID"]}')

                # st.session_state.form_data['Country'] = st.text_input('Country:*', value=st.session_state.form_data['Country'])
# --------------------------Next of Kin's Details------------------------------               