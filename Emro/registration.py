# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 19:14:25 2024

@author: KesBes
"""
import streamlit as st
from datetime import datetime
from dbconnect import init_connection, insert_data

# --------------------------Patient ID Generation------------------------------

def generate_patient_id(card_type):
    """
    Generates a unique patient ID based on the card type, ensuring the integer part increments across months.
    The ID format is {CardType}/{Integer}/{MM}/{YYYY}.
    """
    # from datetime import datetime
    
    # Validate card type
    if card_type not in ['FC', 'SC', 'NHIS']:
        raise ValueError("Invalid card type. Use 'FC', 'SC', or 'NHIS'.")

    # Get current month and year
    now = datetime.now()
    month = now.strftime("%m")
    year = now.strftime("%Y")

    # Database connection
    conn = init_connection()
    cursor = conn.cursor()

    # Fetch the last used integer for the given card type (ignoring month/year)
    cursor.execute(f"""
        SELECT MAX(CAST(SUBSTRING(PATID, CHARINDEX('/', PATID) + 1, 
        CHARINDEX('/', PATID, CHARINDEX('/', PATID) + 1) - CHARINDEX('/', PATID) - 1) AS INT)) 
        AS LastID 
        FROM tblPATIENT 
        WHERE PATID LIKE 'FC/%' OR PATID LIKE 'SC/%' OR PATID LIKE 'NHIS/%'
        AND SUBSTRING(PATID, CHARINDEX('/', PATID, CHARINDEX('/', PATID) + 1) + 1, 2) = '11' 
        AND SUBSTRING(PATID, CHARINDEX('/', PATID, CHARINDEX('/', PATID) + 1) + 4, 4) = '2024'
    """)
    result = cursor.fetchone()

    # Determine the new integer part
    if result and result[0]:
        new_integer = result[0] + 1
    else:
        new_integer = 1  # Start at 1 if no existing IDs

    # Construct the new PATID
    new_patid = f"{card_type}/{new_integer}/{month}/{year}"

    conn.close()
    return new_patid



# --------------------------Patient ID Generation------------------------------

# ========================Start of Registration Function=======================
def registration_module(patient_data=None):
# Create tabs for different registration sections
   tab1, tab2, tab3, tab4 = st.tabs(["Card Details", "Personal Details", \
                                     "Contact Details", "Next of Kin Details"])

# -------------------------------Card Details ---------------------------------
   with tab1:
       # st.header("Card Details")
       st.markdown("""
       <div style="background:#0f983c ;padding:10px">
       <h2 style="color:white;text-align:center;">Patient's Card Details</h2>
       </div>
       """, unsafe_allow_html=True)
   
       col1, col2 = st.columns(2)
       with col1:
           st.session_state.form_data['CardType'] = st.selectbox('Type of \
                                                    Card:', ['HMO', \
                                                    'Individual'], \
                                                    key='CardType')
           st.session_state.form_data['CardClass'] = st.selectbox('Class of \
                                                     Card:', ['FC', 'NHIS', \
                                                    'SC'], key='CardClass')
           st.session_state.form_data['HMOName'] = st.selectbox('HMO Name:\
           ', ["None", "Hygeia", "Reliance", "Leadway", "RedCare", \
               "Philips", "Springtide", "Clearline", "Dots", "Zuma", \
               "Healthcare International", "Songhai", "Integrated Health \
               Care", "Princeton", "Venus", "Wellnes", "Polic", \
               "LifeWorth", "Total Health Trust", "Sterling", "Axa mansard"\
               , "Nonsuch"], key='HMOName')               
       with col2:
          st.session_state.form_data['RegDate'] = st.date_input('Registration \
                                                  Date:', key='RegDate')
          st.session_state.form_data['ShelveNO'] = st.text_input\
                                                   ('ShelveNO:',key='ShelveNo')
          st.text('')
          st.text('')
          if st.button("Save Card Details"):
               RegID = generate_patient_id(st.session_state.form_data['CardClass'])
               st.session_state.form_data['RegID'] = RegID
               st.session_state.form_data['PATID'] = \
                           st.session_state.form_data['RegID'] 
               insert_data('Card Details',st.session_state.form_data['RegID'],\
                           st.session_state.form_data['RegDate'],\
                           st.session_state.form_data['CardClass'],\
                           st.session_state.form_data['CardType'],\
                           st.session_state.form_data['ShelveNO'],\
                           st.session_state.form_data['HMOName'])
               st.write('Card Details Saved Successfully')
# -------------------------------Card Details ---------------------------------
         
# ---------------------------------Personal Details ---------------------------
   with tab2:
        st.markdown("""
        <div style="background:#0f983c ;padding:10px">
        <h2 style="color:white;text-align:center;">Patient's Personal Details</h2>
        </div>
        """, unsafe_allow_html=True)
        # st.header("Patient Personal Information")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input('Registration ID:', \
                          value=st.session_state.form_data['RegID'], \
                          key='RegistrationID', disabled=True)
            st.session_state.form_data['FName'] = st.text_input\
                ('First Name:*', value=st.session_state.form_data['FName'])
            st.session_state.form_data['LName'] = st.text_input\
                ('Last Name:*', value=st.session_state.form_data['LName'])
            st.session_state.form_data['MName'] = st.text_input\
                ('Middle Name:', value=st.session_state.form_data['MName'])
            st.session_state.form_data['Gender'] = st.selectbox('Gender:', \
                ['Female', 'Male', 'Other'], key='Gender')
            
    
        with col2:
            st.session_state.form_data['MStatus'] = st.selectbox\
                ('Marital Status:', ['Divorced','Married', 'Single','Widow', \
                'Widower', 'Other'], key = 'MStatus')
            st.session_state.form_data['StateOfOrigin'] = st.selectbox\
            ('State of Origin:', \
             ["Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", \
              "Benue", "Borno", "Cross River", "Delta", "Ebonyi", "Edo", \
             "Ekiti", "Enugu", "FCT - Abuja", "Gombe", "Imo", "Jigawa", \
             "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", \
             "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun",\
             "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba","Yobe","Zamfara"],\
             key = 'StatOfOrigin')
            st.session_state.form_data['DateOfBirth'] = st.date_input\
            ('Date of Birth:*',value=st.session_state.form_data['DateOfBirth'])
            st.session_state.form_data['PhoneNo'] = st.text_input\
            ('Phone Number *:', value=st.session_state.form_data['PhoneNo'])
# Consult Emro on the below validation
            # if st.session_state.form_data['PhoneNo'] == '':
            #     st.warning('Please enter Phone Number!')
            #     st.stop()
            st.session_state.form_data['EmailAddress'] = \
            st.text_input('Email Address:', \
            value=st.session_state.form_data['EmailAddress'])
                          
    
            if st.button("Save Patient Details"):
                if not st.session_state.form_data['FName']:
                    st.warning('First Name is required!')
                elif not st.session_state.form_data['LName']:
                    st.warning('Last Name is required!')
                elif not st.session_state.form_data['PhoneNo']:
                    st.warning('Phone Number is required!')
                
                else:
           # Proceed with saving the details if all required fields are filled
                   st.session_state.form_data['PATID'] = st.session_state.form_data['RegID']
                   insert_data('Personal Details', st.session_state.form_data['PATID'],
                       st.session_state.form_data['RegID'],
                       st.session_state.form_data['FName'],
                       st.session_state.form_data['LName'],
                       st.session_state.form_data['MName'],
                       st.session_state.form_data['Gender'],
                       st.session_state.form_data['MStatus'],
                       st.session_state.form_data['StateOfOrigin'],
                       st.session_state.form_data['DateOfBirth'],
                       st.session_state.form_data['PhoneNo'],
                       st.session_state.form_data['EmailAddress'])
                   st.write('Details saved successfully. Enter Contact details.')

# ---------------------------------Personal Details ---------------------------
        
# ---------------------------------Contact Details-----------------------------            
   with tab3:
        st.markdown("""
        <div style="background:#0f983c ;padding:10px">
        <h2 style="color:white;text-align:center;">Patient's Contact Details</h2>
        </div>
        """, unsafe_allow_html=True)
        # st.header("Contact Details")
        
        col1, col2 = st.columns(2)
        with col1:          
            st.session_state.form_data['HouseNo'] = st.text_input\
            ('House Number:', value =st.session_state.form_data['HouseNo'])
            st.session_state.form_data['StreetName'] = st.text_input\
            ('Street Name:', value=st.session_state.form_data['StreetName'])
            st.session_state.form_data['City'] = st.text_input\
            ('City:', value=st.session_state.form_data['City'])
            
    
        with col2:
            st.session_state.form_data['State'] = st.selectbox\
            ('State:', \
             ["Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", \
              "Benue", "Borno", "Cross River", "Delta", "Ebonyi", "Edo", \
             "Ekiti", "Enugu", "FCT - Abuja", "Gombe", "Imo", "Jigawa", \
             "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", \
             "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun",\
             "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara"],\
             key = 'State')
            st.session_state.form_data['PostCode'] = st.text_input\
            ('Postal Code:*', value=st.session_state.form_data['PostCode'])
            st.session_state.form_data['Country'] = st.text_input\
            ('Country:*', value=st.session_state.form_data['Country'])

            if st.button("Save Next of Kin Details"):
                 insert_data('Contact Details', st.session_state.form_data\
                             ['PATID'],\
                             st.session_state.form_data['HouseNo'],\
                             st.session_state.form_data['StreetName'],\
                             st.session_state.form_data['City'],\
                             st.session_state.form_data['State'],\
                             st.session_state.form_data['PostCode'],\
                             st.session_state.form_data['Country'])
                 st.write('Contact saved successfully. \
                          Continue on the Next of Kin tab')
# ---------------------------------Contact Details-----------------------------
        
        
# --------------------------------Next of Kin's Details------------------------
   with tab4:
        st.markdown("""
        <div style="background:#0f983c ;padding:10px">
        <h2 style="color:white;text-align:center;">Patient's Next of Kin Details</h2>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            # st.session_state.form_data['PATID'] = st.session_state.form_data['FName'] 
            st.session_state.form_data['NxtFName'] = \
                st.text_input('Next of Kin First Name:', \
                value =st.session_state.form_data['NxtFName'])
            st.session_state.form_data['NxtLName'] = \
            st.text_input('Next of Kin Last Name:', \
            value =st.session_state.form_data['NxtLName'])
            st.session_state.form_data['NxtRelationship'] = \
            st.text_input('Relationship:', \
            value=st.session_state.form_data['NxtRelationship'])
            
        with col2:
            st.session_state.form_data['NxtEmailAddress'] = \
            st.text_input('Next of Kin Email ID:', \
            value=st.session_state.form_data['NxtEmailAddress'])
            st.session_state.form_data['NxtPhoneNo'] = st.text_input('Next of \
            Kin Phone No:*', value=st.session_state.form_data['NxtPhoneNo'])
            st.text('')
            st.text('')
            if st.button('Submit'):
                insert_data('Next of Kin Details', \
                            st.session_state.form_data['PATID'],\
                            st.session_state.form_data['NxtFName'],\
                            st.session_state.form_data['NxtLName'],\
                            st.session_state.form_data['NxtRelationship'],\
                            st.session_state.form_data['NxtEmailAddress'],\
                            st.session_state.form_data['NxtPhoneNo'])
                
                
                st.write('Contact saved successfully.')
                st.success(f"Patient Registration is complete. The generated \
                           Registration ID is: \
                               {st.session_state.form_data['PATID']}")
# --------------------------------Next of Kin's Details------------------------

# ========================End of Registration Function=========================
