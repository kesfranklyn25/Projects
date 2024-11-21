# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 19:51:05 2024

@author: KesBes
"""
import streamlit as st
from dbconnect import init_connection


conn = init_connection()

# ==============================Update Module==================================
def patupdate():
        st.markdown("""
        <div style="background:#0f983c ;padding:10px">
        <h2 style="color:white;text-align:center;">Update Patient's Details</h2>
        </div>
        """, unsafe_allow_html=True)
        
        Patient_ID = st.text_input('Registration ID:', key='Patient_ID')
        
        if st.button('Edit'):
            if Patient_ID:
                try:
                    # Create a cursor object to execute queries
                    cursor = conn.cursor()
    
                    # Optimized query to fetch from multiple tables
                    query = """
                    SELECT p.PATID, p.RegID, p.FName, p.LName, p.MName, p.Gender, \
                        p.MStatus, p.StateOfOrigin, p.DateOfBirth, p.PhoneNo, \
                            p.EmailAddress, 
                            c.RegID, c.RegDate, c.CardClass, c.CardType, \
                                c.ShelveNo, c.HMO, 
                            a.AddID, a.PATID, a.HouseNo, a.StreetName, a.City, \
                                a.State, a.PostCode, a.Country, 
                            n.NOKID, n.PATID, n.nxtFName, n.nxtLName, \
                                n.nxtRelationship, n.nxtEmailAddress, n.nxtPhoneNo
                    FROM tblPATIENT p
                    LEFT JOIN tblCard c ON p.RegID = c.RegID
                    LEFT JOIN tblAddress a ON p.PATID = a.PATID
                    LEFT JOIN tblNextOfKin n ON p.PATID = n.PATID
                    WHERE p.PATID = ?
                    """
                    cursor.execute(query, (Patient_ID,))
                    result = cursor.fetchone()
    
                    if result:
                        # Store the result in session state for different sections
                        st.session_state['patient'] = result[:11]# First 11 columns are from tblPATIENT
                        st.session_state['card'] = result[11:17] # Next 6 columns are from tblCard
                        st.session_state['address'] = result[17:25] # Next 8 columns are from tblAddress
                        st.session_state['next_of_kin'] = result[25:]# Last 6 columns are from tblNextOfKin
    
                        st.success(f"Patient record for ID {Patient_ID} \
                                    loaded successfully.")
                    else:
                        st.warning(f"No record found for Patient ID {Patient_ID}.")
                        st.session_state['result'] = None
    
                    cursor.close()
    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    
        # Display form for updating patient, card, address, and next of kin details
        if 'patient' in st.session_state:
            record_patient = st.session_state['patient']
            record_card = st.session_state['card']
            record_address = st.session_state['address']
            record_next_of_kin = st.session_state['next_of_kin']
    
            # Patient Details (First 11 columns)
            st.markdown("### Patient Details")
            col1, col2 = st.columns(2)
            with col1:
                st.text_input('Patient ID', value=record_patient[0], key='PatID', \
                              disabled=True)
                st.text_input('First Name', value=record_patient[2], key='FName')
                st.text_input('Last Name', value=record_patient[3], key='LName')
                st.text_input('Middle Name', value=record_patient[4], key='MName')
                st.text_input('Gender', value=record_patient[5], key='Gender')
            with col2:
                st.text_input('Marital Status', value=record_patient[6], \
                              key='MaritalStatus')
                st.text_input('State of Origin', value=record_patient[7], \
                              key='StateOfOrigin')
                st.date_input('Date of Birth', value=record_patient[8], \
                              key='DateOfBirth')
                st.text_input('Phone Number', value=record_patient[9], \
                              key='PhoneNo')
                st.text_input('Email Address', value=record_patient[10], \
                              key='Email')
    
            # Card Details (Next 6 columns)
            st.markdown("### Card Details")
            col3, col4 = st.columns(2)
            with col3:
                st.text_input('Card Type', value=record_card[3], key='CardType')
                st.text_input('Card Class', value=record_card[2], key='CardClass')
            with col4:
                st.text_input('Shelve Number', value=record_card[4], key='ShelveNo')
                st.text_input('HMO', value=record_card[5], key='HMO')
    
            # Address Details (Next 8 columns)
            st.markdown("### Address Details")
            col5, col6 = st.columns(2)
            with col5:
                st.text_input('House Number', value=record_address[2], \
                              key='HouseNo')
                st.text_input('Street Name', value=record_address[3], \
                              key='StreetName')
                st.text_input('City', value=record_address[4], key='City')
            with col6:
                
                st.text_input('State', value=record_address[5], \
                              key='AddressState')
                st.text_input('Postal Code', value=record_address[6], \
                              key='PostCode')
                st.text_input('Country', value=record_address[7], key='Country')
    
            # Next of Kin Details (Last 6 columns)
            st.markdown("### Next of Kin Details")
            col7, col8 = st.columns(2)
            with col7:
                st.text_input('Next of Kin First Name', \
                              value=record_next_of_kin[2], key='nxtFName')
                st.text_input('Next of Kin Last Name', \
                              value=record_next_of_kin[3], key='nxtLName')
            with col8:
                st.text_input('Relationship', value=record_next_of_kin[4], \
                              key='nxtRelationship')
                st.text_input('Next of Kin Email', value=record_next_of_kin[5], \
                              key='nxtEmail')
                st.text_input('Next of Kin Phone', value=record_next_of_kin[6], \
                              key='nxtPhone')
    
            # Update Changes Button
            if st.button('Update Changes'):
                try:
                    cursor = conn.cursor()
    
                    # Update tblPATIENT
                    update_patient_query = """
                    UPDATE tblPATIENT
                    SET FName = ?, LName = ?, MName = ?, Gender = ?, MStatus = ?, \
                        StateOfOrigin = ?, DateOfBirth = ?, PhoneNo = ?, \
                            EmailAddress = ?
                    WHERE PATID = ?
                    """
                    cursor.execute(update_patient_query, \
                                    (st.session_state['FName'], \
                                    st.session_state['LName'], \
                                    st.session_state['MName'],
                                    st.session_state['Gender'], \
                                    st.session_state['MaritalStatus'], \
                                    st.session_state['StateOfOrigin'],
                                    st.session_state['DateOfBirth'], \
                                    st.session_state['PhoneNo'], \
                                    st.session_state['Email'], \
                                    st.session_state['PatID']))
    
                    # Update tblCard
                    update_card_query = """
                    UPDATE tblCard
                    SET CardType = ?, CardClass = ?, ShelveNo = ?, HMO = ?
                    WHERE RegID = ?
                    """
                    cursor.execute(update_card_query, \
                                    (st.session_state['CardType'], \
                                    st.session_state['CardClass'], \
                                    st.session_state['ShelveNo'], \
                                    st.session_state['HMO'], \
                                    st.session_state['PatID']))
    
                    # Update tblAddress
                    update_address_query = """
                    UPDATE tblAddress
                    SET HouseNo = ?, StreetName = ?, City = ?, State = ?, \
                        PostCode = ?, Country = ?
                    WHERE PATID = ?
                    """
                    cursor.execute(update_address_query, \
                                    (st.session_state['HouseNo'], \
                                    st.session_state['StreetName'], \
                                    st.session_state['City'],
                                    st.session_state['AddressState'], \
                                    st.session_state['PostCode'], \
                                    st.session_state['Country'], \
                                    st.session_state['PatID']))
    
                    # Update tblNextOfKin
                    update_next_of_kin_query = """
                    UPDATE tblNextOfKin
                    SET nxtFName = ?, nxtLName = ?, nxtRelationship = ?, \
                        nxtEmailAddress = ?, nxtPhoneNo = ?
                    WHERE PATID = ?
                    """
                    cursor.execute(update_next_of_kin_query, \
                                    (st.session_state['nxtFName'], \
                                    st.session_state['nxtLName'], \
                                    st.session_state['nxtRelationship'],
                                    st.session_state['nxtEmail'], \
                                    st.session_state['nxtPhone'], \
                                    st.session_state['PatID']))
    
                    conn.commit()  # Commit the changes
                    with col7:
    
                        st.success('Details updated successfully.')
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    
    
    
# ==============================Update Module==================================