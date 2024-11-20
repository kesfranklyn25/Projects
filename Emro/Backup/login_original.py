# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 06:48:26 2024

@author: KesBes
"""

import streamlit as st
# import pyodbc
from PIL import Image
import hashlib
from dbconnect import init_connection
from Hospital import hospital_portal


# ----------------------------Load the Logo------------------------------------

img = Image.open('C:/Users/Fatima/Desktop/Emro/kescare_logo.png')

# ----------------------------Load the Logo------------------------------------


# -----------------------------Page Title--------------------------------------
st.set_page_config(
    page_title='Christbay Consultants Hospital Registration System',
    page_icon=img,
    layout="wide")

# # -----------------------------Page Title--------------------------------------

#==================================Authentication==============================

# ===================================Authentication============================
    # login()
# -------------------------------App Logo--------------------------------------
# Display the logo at the top of the page
st.text('')
st.text('')
st.text('')
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    st.image(img, width=150)

with col2:
    st.markdown("""
    <style>
    h5 {
        text-align: center;
        font-size: 14px;
        margin-bottom: 3px;
        font-weight: bold;
    }
    p {
        text-align: justify;
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 15px;
    }
    </style>
    
    <h4>Quality healthcare services at your fingertips!</h4>
    <p>ChristBay Hospital is dedicated to providing top-notch medical \
        services. You can register 
    patients using this application. Follow the steps to complete the patient \
        registration process.</p>
    """, unsafe_allow_html=True)   
# -------------------------------App Logo--------------------------------------

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to connect to the database

# Function to authenticate user
def authenticate_user(username, password):
    hashed_password = hash_password(password)
    conn = init_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Password FROM staff WHERE username = ?", username)
    record = cursor.fetchone()
    conn.close()
    if record and record[0] == hashed_password:
        return True
    return False

# Login function
def login():
    # st.title("Login Page")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state.authenticated = True
            st.success("Login successful! Redirecting...")
            st.experimental_rerun()
            # hospital_portal()
        else:
            st.error("Invalid username or password.")

login()
# ==============================Authentication Module==========================

if __name__ == "__main__":
    if st.session_state.get("authenticated", False):
        hospital_portal()
    else:
        login()