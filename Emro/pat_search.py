# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 19:28:08 2024

@author: KesBes
"""
import streamlit as st
from dbconnect import init_connection


conn = init_connection()

    
# ------------------------Next and Previous Function---------------------------
def load_previous_record():
    if st.session_state.current_record > 0:
        st.session_state.current_record -= 1

def load_next_record():
    if st.session_state.current_record <len(st.session_state.search_results)-1:
        st.session_state.current_record += 1

# ------------------------Next and Previous Function---------------------------

def search_patient_record():
    st.markdown("""
    <div style="background:#0f983c ;padding:10px">
    <h2 style="color:white;text-align:center;">Search Patient's Details</h2>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
       
        # Text input for searching by patient details
        PatientID = st.text_input('Enter Patient ID:', key='PatientID')
        PatientFirstName = st.text_input('Enter Patient\'s First Name:', key='PatientFirstName')
    with col2:
        PatientLastName = st.text_input('Enter Patient\'s Last Name:', key='PatientLastName')
        PatientPhoneNo = st.text_input('Enter Patient\'s Phone No:', key='PatientPhoneNo')
       
    # Initialize session state for pagination
    if 'search_results' not in st.session_state:
        st.session_state.search_results = []
    if 'current_record' not in st.session_state:
        st.session_state.current_record = 0
    with col2:
        if st.button('Search'):
            if PatientID or PatientFirstName or PatientLastName or \
                PatientPhoneNo:  # Proceed if any field is filled
                # populate_Patient_record()
                try:
                    # Create a cursor object to execute queries
                    cursor = conn.cursor()
    
                    # Query to search for the matching details in the database
                    query = "SELECT * FROM tblPATIENT WHERE PATID = ? OR \
                        FName = ? OR LName = ? OR PhoneNo =?"
                    cursor.execute(query, (PatientID, PatientFirstName, \
                                            PatientLastName, PatientPhoneNo))
    
                    # Fetch all matching records
                    st.session_state.search_results = cursor.fetchall()
    
                    # Check if any results were found
                    if st.session_state.search_results:
                        # Reset the current record index to the first record
                        st.session_state.current_record = 0
                        with col1:
    
                            st.success(f"{len(st.session_state.search_results)}\
                                        record(s) found.")
    
                    else:
                        st.warning('No records found for the given details.')
                        st.session_state.search_results = []  # Clear results
    
                    cursor.close()
    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.warning('Please enter at least one field to search.')
    
        # Display results with navigation if there are results
    if st.session_state.search_results:
          record = st.session_state.search_results\
              [st.session_state.current_record]
    
            # Display form with populated values
          st.markdown("### Patient Details")
          col1, col2 = st.columns(2)
        
          with col1:
              st.text_input('Patient ID', value=record[0], key='PatID',\
                            disabled=True)
              st.text_input('First Name', value=record[2], key='FName', \
                            disabled=True)
              st.text_input('Last Name', value=record[3], key='LName', \
                            disabled=True)
              st.text_input('Gender', value=record[5], key='Gender',\
                            disabled=True)
             
          with col2:
            st.text_input('Marital Status', value=record[6], \
                          key='MaritalStatus', disabled=True)
            st.text_input('State of Origin', value=record[7], \
                          key='StateOfOrigin', disabled=True)
            st.date_input('Date of Birth', value=record[8], \
                          key='DOB', disabled=True)
            st.text_input('Phone Number', value=record[9], \
                          key='PhoneNo', disabled=True)
            st.text_input('Email Address', value=record[10], \
                          key='Email', disabled=True)
        
        # Navigation buttons with actions that update session state immediately
        # populate_Patient_record()
          col1, col2, col3 = st.columns([1, 2, 1])
        
          with col1:
              st.button("Previous", on_click=load_previous_record)
        
          with col3:
              st.button("Next", on_click=load_next_record)
        
        # Display a record count for clarity
          st.markdown(f"Record {st.session_state.current_record + 1} of \
                      {len(st.session_state.search_results)}")
