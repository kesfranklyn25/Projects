# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 06:49:26 2024

@author: KesBes
"""

import streamlit as st
from streamlit_option_menu import option_menu
import pyodbc
# from datetime import datetime
from dbconnect import init_connection, insert_data

# -------------------------Database Connetion----------------------------------
    
conn = init_connection()
    
# --------------------------Database Connection Ends---------------------------
# -----------------------------Sidebar Colour----------------------------------
# st.markdown("""
#     <style>
#         [data-testid=stSidebar] {
#             background-color: #0f983c;
#             primaryColor: #0a07d0
#         }
#         .st-emotion-cache-1wbqy5l {
#             visibility: hidden;
#         }
#         .block-container {
#             padding-top: 1rem;
#             padding-right: 1rem;
#             padding-left: 1rem;
#             padding-bottom: 1rem;
#         }
#     </style>
#     """, unsafe_allow_html=True)
    
# -----------------------------Sidebar Colour----------------------------------

# with st.sidebar:
#     menu = option_menu(
#         'Staff Portal',
#         ['New Staff', 'Login'],
#         default_index=0
#     )
# st.markdown("""
#        <style> +
#         .element-container button.step-up { display: none; } +
#         .element-container button.step-down  { display: none; } +
#         .element-container div[data-baseweb] { border-radius: 4px; }
#        </style>
# """, unsafe_allow_html=True)

# =========================Sidebar Menu for Navigation=========================
import hashlib
def newstaff():

    # if menu == 'New Staff':
    # Display title and form
    st.markdown("""
    <div style="background-color:#0f983c;padding:10px">
    <h2 style="color:white;text-align:center;">CBCH Staff Creation</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Form fields
    col1, col2 = st.columns(2)
    
    with col1:
        SFname = st.text_input('First Name:', key='SFname')
        SLname = st.text_input('Last Name:', key='SLname')
        SRegdate = st.date_input('Registration Date:', key='SRegdate')
    
    with col2:
        SUsername = st.text_input('Username:', key='SUsername')
        SPassword = st.text_input('Password:', type='password', key='SPassword')
        SModifiedDate = st.date_input('Modified Date:', key='SModifiedDate')
        DeptID = st.text_input('Department:', key='DeptID')

    # Submit button
    if st.button('Submit', key='login_button'):
        # Check for None or empty values in required fields
        if not SUsername or not SFname or not SLname:
            st.error("Username, First Name, and Last Name cannot be empty.")
        else:
            # Hash the password
            hashed_password = hashlib.sha256(SPassword.encode()).hexdigest()

            try:
                # Insert data
                insert_data(
                    'New Staff',
                    SUsername,
                    SRegdate,
                    SFname,
                    SLname,
                    hashed_password,
                    SModifiedDate,
                    DeptID
                )
                st.success('User created successfully')
            except pyodbc.IntegrityError:
                st.error('Username already exists. Please choose a different username.')
            except Exception as e:
            
                st.error(f"An unexpected error occurred: {e}")