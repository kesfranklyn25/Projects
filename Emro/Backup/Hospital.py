def hospital_portal():
    import streamlit as st
    from streamlit_option_menu import option_menu
    from datetime import datetime
    from PIL import Image
    import pandas as pd
    # import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    # import pandas.io.sql as psql
    import plotly.express as px
    from dbconnect import init_connection
    from registration import registration_module, generate_patient_id
    from staffCreation import newstaff
    import hashlib
    # from login import login
    # import streamlit_authenticator as stauth
    
    # # ----------------------------Load the Logo------------------------------------
    
    # img = Image.open('C:/Users/Fatima/Desktop/Emro/kescare_logo.png')
    
    # # ----------------------------Load the Logo------------------------------------
    
    
    # # -----------------------------Page Title--------------------------------------
    # st.set_page_config(
    #     page_title='Christbay Consultants Hospital Registration System',
    #     page_icon=img,
    #     layout="wide")
    
    # # # -----------------------------Page Title--------------------------------------
    
    # #==================================Authentication==============================
    
    # # ===================================Authentication============================
    #     # login()
    # # -------------------------------App Logo--------------------------------------
    # # Display the logo at the top of the page
    # st.text('')
    # st.text('')
    # st.text('')
    # col1, col2, col3 = st.columns([1, 3, 1])
    
    # with col1:
    #     st.image(img, width=150)
    
    # with col2:
    #     st.markdown("""
    #     <style>
    #     h5 {
    #         text-align: center;
    #         font-size: 14px;
    #         margin-bottom: 3px;
    #         font-weight: bold;
    #     }
    #     p {
    #         text-align: justify;
    #         font-size: 14px;
    #         line-height: 1.6;
    #         margin-bottom: 15px;
    #     }
    #     </style>
        
    #     <h4>Quality healthcare services at your fingertips!</h4>
    #     <p>ChristBay Hospital is dedicated to providing top-notch medical \
    #         services. You can register 
    #     patients using this application. Follow the steps to complete the patient \
    #         registration process.</p>
    #     """, unsafe_allow_html=True)   
    # # -------------------------------App Logo--------------------------------------
    
    # # -------------------------Database Connetion----------------------------------
    
    conn = init_connection()
    # # --------------------------Database Connection Ends---------------------------
    
    
    # Initialize session state for form data
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
            'CardClass':'',
            'HMO':'',
            'ShelveNo':'',
            'PATID': '',
            'RegID': '',
            'SFname': '',
            'SLname': '',
            'SRegDate': '',
            "SPassword":'',
            'SModifiedDate':'',
            'DeptID': ''
        }
    
    
    # -----------------------------Sidebar Colour----------------------------------
    st.markdown("""
        <style>
            [data-testid=stSidebar] {
                background-color: #0f983c;
                primaryColor: #0a07d0
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
    
    
    # ------------------------Next and Previous Function---------------------------
    def load_previous_record():
        if st.session_state.current_record > 0:
            st.session_state.current_record -= 1
    
    def load_next_record():
        if st.session_state.current_record <len(st.session_state.search_results)-1:
            st.session_state.current_record += 1
    
    # ------------------------Next and Previous Function---------------------------
    
    # =========================Sidebar Menu for Navigation=========================
    with st.sidebar:
        menu = option_menu(
            'Patient Registration',
            ['ChristBay', 'Registration', 'Search', 'Update', 'New Staff'],
            default_index=0
        )
    st.markdown("""
            <style> +
            .element-container button.step-up { display: none; } +
            .element-container button.step-down  { display: none; } +
            .element-container div[data-baseweb] { border-radius: 4px; }
            </style>
    """, unsafe_allow_html=True)
    
    # =========================Sidebar Menu for Navigation=========================
    # ===============================Home Page=====================================
    
    if menu == 'ChristBay':
        
        cursor = conn.cursor()
        
        query = "SELECT p.patid, p.Gender, c.CardClass, c.CardType FROM\
                tblPATIENT p join tblCard c on p.PATID = c.RegID "
        df = pd.read_sql_query(query, conn)
        
        col1, col2 = st.columns(2)
    
        with col1:
            Total_Pat = df.shape[0]  # Use the dataframe from the database
            st.write("Total Number of Patients:", Total_Pat)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write('Analysis: Classes of Cards')
            # Ensure no NaN values in 'CardClass' column and that it has data
            if not df['CardClass'].dropna().empty:
                sns.countplot(x='CardClass', data=df, palette=['#0f983c', '#0a07d0', '#ff00bb'])
                st.pyplot(plt)  
                plt.close()
            else:
                st.write("No data available for CardClass.")
        
        with col2:
            st.write('Analysis: Card Type')
            # Ensure no NaN values in 'CardType' column and that it has data
            if not df['CardType'].dropna().empty:
                sns.countplot(x='CardType', data=df, palette=['#0f983c', '#0a07d0'])
                st.pyplot(plt)
                plt.close()
            else:
                st.write("No data available for CardType.")
        
        with col3:
            st.write('Analysis By Gender')
            # Ensure no NaN values in 'Gender' column and that it has data
            if not df['Gender'].dropna().empty:
                pie = px.pie(df, names='Gender', \
                              color_discrete_sequence=['#0f983c', '#0a07d0'], \
                              width=320, height=320)
                pie.update_layout(margin=dict(t=10, b=100))  # Adjust the margins
                st.plotly_chart(pie)
            else:
                st.write("No data available for Gender.")
    
    # ===============================Home Page=====================================  
    # =============================Registration Page===============================
    elif menu == 'Registration':
        registration_module() # Calls Registration function fron registration module
        
    # =============================Registration Page===============================
    
    # ================================Search Module================================
    
    elif menu == 'Search':
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
    
    
    # ================================Search Module================================
    # ==============================Update Module==================================
    elif menu == 'Update':
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
    
    # ==============================New Staff Creation=============================
    
    elif menu == 'New Staff':
        newstaff()
    # ==============================New Staff Creation=============================
    # else:
    #     login()
    #     # newstaff()
    #     # pass
    # =================================Footer======================================
    st.markdown("""
        <div style="display: flex; background:#0f983c; color:#fff; \
            padding:10px; margin-top:20px; border-top: \
            1px solid #ddd; justify-content: space-between; width: 100%;">
            <div>© 2024 KesBes Technology. All Rights Reserved.</div>
            <div style="text-align: right; background:#0f983c; color:#fff;">\
                Phone: +2347032332980 or +2347035221702</div>
        </div>
        """, unsafe_allow_html=True)


# =================================Footer======================================