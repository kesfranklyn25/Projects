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
# st.logo(image:img)

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
    if action == 'Card Details':
        cursor.execute("""
            INSERT INTO tblCard(RegID, RegDate, CardClass, CardType, ShelveNo,HMO)
            VALUES (?, ?, ?, ?, ?, ?)
        """, args)
    elif action == 'Personal Details':
        cursor.execute("""
            INSERT INTO tblPATIENT(PATID,RegID,FName, LName, MName, Gender, MStatus,\
            StateOfOrigin, DateOfBirth, PhoneNo, EmailAddress) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, args)
    elif action == 'Contact Details':
        cursor.execute("""
            INSERT INTO tblAddress (PATID, HouseNo, StreetName, City, State, PostCode, Country) 
            VALUES (?, ?, ?,?, ?, ?, ?)
        """, args)
        
    elif action == 'Next of Kin Details':
        cursor.execute("""
            INSERT INTO tblNEXTOFKIN (PATID,nxtFName, nxtLName, nxtRelationship, nxtEmailAddress, nxtPhoneNo) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, args)
        
        # cursor.execute("""
        #     INSERT INTO tblREGISTRATION (PATID,RegDate, CardClass, CardType) 
        #     VALUES (?, ?, ?, ?)
        # """, args[6:])
        # PATID						
    conn.commit()
    cursor.close()
    # conn.close()
    
# --------------------------Database Connection Ends--------------------------------

# Function to generate custom PATID
def generate_patient_id(card_type):
    """
    Generates a patient ID based on the card type.
    For Family Card: FC/integer/mm/yyyy
    For Single Card: SC/integer/mm/yyyy
    For NHIS Card: NHIS/integer/mm/yyyy
    
    Parameters:
    card_type (str): Either 'FC' for Family Card or 'SC' for Single Card.
    
    Returns:
    str: The generated patient ID.
    """
    now = datetime.now()
    month = now.strftime("%m")
    year = now.strftime("%Y")

    # Ensure the card_type is valid
    if card_type not in ['FC', 'NHIS', 'SC']:
        raise ValueError("Invalid card type. Use 'FC' for Family Card or 'SC' \
                         for Single Card and NHIS for National Health Insurance Scheme card.")
    
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

# -------------------------Database Connetion----------------------------------

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
        'RegID': ''
        
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
        'Patient Registration',
        ['ChristBay', 'Registration', 'Search', 'Update'],
        default_index=0
    )
st.markdown("""
       <style> +
        .element-container button.step-up { display: none; } +
        .element-container button.step-down  { display: none; } +
        .element-container div[data-baseweb] { border-radius: 4px; }
       </style>
""", unsafe_allow_html=True)
# ------------------------ PAGE 1: Welcome Page -------------------------------
if menu == 'ChristBay':
    st.markdown("""
    <div style="background:#000080 ;padding:10px">
    <h2 style="color:white;text-align:center;">Welcome to ChristBay Hospital</h2>
    </div>
    """, unsafe_allow_html=True)
    # st.header("Welcome to ChristBay Hospital")
    
    st.write("""
    **ChristBay Hospital** is dedicated to providing top-notch medical services.
    You can register patients using this application. Follow the steps to complete the patient registration process.
    """)

# ----------- PAGE 2: Registration Page -----------
elif menu == 'Registration':
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = 0

    # Create tabs for the registration sub-pages
    tab1, tab2, tab3, tab4 = st.tabs(
    ["Card Details", "Personal Details", "Contact Details", "Next of Kin Details"])

# -------------------------Tab 1 Card Details ---------------------------------
   
    with tab1:
           # st.header("Card Details")
           st.markdown("""
           <div style="background:#000080 ;padding:10px">
           <h2 style="color:white;text-align:center;">Patient's Card Details</h2>
           </div>
           """, unsafe_allow_html=True)
       
           col1, col2 = st.columns(2)
           with col1:
               # st.session_state.form_data['RegID'] = st.session_state.form_data['FName'] 
               st.session_state.form_data['CardType'] = st.selectbox('Type of Card:', ['HMO', 'Individual'], key='CardType')
               st.session_state.form_data['CardClass'] = st.selectbox('Class of Card:', ['FC', 'NHIS', 'SC'], key='CardClass')
               st.session_state.form_data['HMOName'] = st.selectbox('HMO Name:\
               ', ["None", "Hygeia", "Reliance", "Leadway", "RedCare", \
                   "Philips", "Springtide", "Clearline", "Dots", "Zuma", \
                   "Healthcare International", "Songhai", "Integrated Health \
                   Care", "Princeton", "Venus", "Wellnes", "Polic", \
                   "LifeWorth", "Total Health Trust", "Sterling", "Axa mansard"\
                   , "Nonsuch"], key='HMOName')               
           with col2:
              st.session_state.form_data['RegDate'] = st.date_input('Registration Date:', key='RegDate')
              st.session_state.form_data['ShelveNO'] = st.text_input('ShelveNO:',key='ShelveNo')
               if st.button('Save Details'):
                   RegID = generate_patient_id(st.session_state.form_data['CardClass'])
                   st.session_state.form_data['RegID'] = RegID
                   st.session_state.form_data['PATID'] = st.session_state.form_data['RegID'] 
                   insert_data('Card Details',st.session_state.form_data['RegID'],\
                               st.session_state.form_data['RegDate'],\
                               st.session_state.form_data['CardClass'],\
                               st.session_state.form_data['CardType'],\
                               st.session_state.form_data['ShelveNO'],\
                               st.session_state.form_data['HMOName'])
                   st.write('Card Details Saved Successfully')
# -------------------------Tab 1 Card Details ---------------------------------
             
# ------------------------- Tab 2: Personal Details ---------------------------
    with tab2:
        st.markdown("""
        <div style="background:#000080 ;padding:10px">
        <h2 style="color:white;text-align:center;">Patient's Personal Details</h2>
        </div>
        """, unsafe_allow_html=True)
        # st.header("Patient Personal Information")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input('Registration ID:', value=st.session_state.form_data['RegID'], key='RegistrationID', disabled=True)
            st.session_state.form_data['FName'] = st.text_input\
                ('First Name:*', value=st.session_state.form_data['FName'])
            st.session_state.form_data['LName'] = st.text_input\
                ('Last Name:*', value=st.session_state.form_data['LName'])
            st.session_state.form_data['MName'] = st.text_input\
                ('Middle Name:', value=st.session_state.form_data['MName'])
            st.session_state.form_data['Gender'] = st.selectbox('Gender:', \
                ['Female', 'Male', 'Other'], key='Gender')
            st.session_state.form_data['MStatus'] = st.selectbox\
                ('Marital Status:', ['Divorced','Married', 'Single','Widow', \
                'Widower', 'Other'], key = 'MStatus')

        with col2:
            st.session_state.form_data['StateOfOrigin'] = st.selectbox\
            ('State of Origin:', \
             ["Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", \
              "Benue", "Borno", "Cross River", "Delta", "Ebonyi", "Edo", \
             "Ekiti", "Enugu", "FCT - Abuja", "Gombe", "Imo", "Jigawa", \
             "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", \
             "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun",\
             "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara"],\
             key = 'StatOfOrigin')
            st.session_state.form_data['DateOfBirth'] = st.date_input\
            ('Date of Birth:*', value=st.session_state.form_data['DateOfBirth'])
            st.session_state.form_data['PhoneNo'] = st.text_input\
            ('Phone Number:', value=st.session_state.form_data['PhoneNo'])
            st.session_state.form_data['EmailAddress'] = \
            st.text_input('Email Address:', \
            value=st.session_state.form_data['EmailAddress'])
                          

             if st.button('Next'):
                 st.session_state.form_data['PATID'] = st.session_state.form_data['RegID']
                 insert_data('Personal Details', st.session_state.form_data\
                             ['PATID'],\
                             st.session_state.form_data['RegID'],\
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
                
# ------------------------- Tab 2: Personal Details ---------------------------

# ----------------------------- Tab 3 Contact Details--------------------------


        with tab3:
            st.markdown("""
            <div style="background:#000080 ;padding:10px">
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

                 if st.button('Save Contact'):
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
# ----------------------------- Tab 3 Contact Details--------------------------
        with tab4:
            st.markdown("""
            <div style="background:#000080 ;padding:10px">
            <h2 style="color:white;text-align:center;">Patient's Next of Kin Details</h2>
            </div>
            """, unsafe_allow_html=True)
            # st.header("Next of Kin Information")
            
            col1, col2 = st.columns(2)
            with col1:
                # st.session_state.form_data['PATID'] = st.session_state.form_data['FName'] 
                st.session_state.form_data['NxtFName'] = st.text_input('Next of Kin First Name:', value =st.session_state.form_data['NxtFName'])
                st.session_state.form_data['NxtLName'] = st.text_input('Next of Kin Last Name:', value =st.session_state.form_data['NxtLName'])
                st.session_state.form_data['NxtRelationship'] = st.text_input('Relationship:', value=st.session_state.form_data['NxtRelationship'])
                
                

            with col2:
                st.session_state.form_data['NxtEmailAddress'] = st.text_input('Next of Kin Email ID:', value=st.session_state.form_data['NxtEmailAddress'])
                st.session_state.form_data['NxtPhoneNo'] = st.text_input('Next of Kin Phone No:*', value=st.session_state.form_data['NxtPhoneNo'])
                if st.button('Submit'):
                    insert_data('Next of Kin Details', \
                                st.session_state.form_data['PATID'],\
                                st.session_state.form_data['NxtFName'],\
                                st.session_state.form_data['NxtLName'],\
                                st.session_state.form_data['NxtRelationship'],\
                                st.session_state.form_data['NxtEmailAddress'],\
                                st.session_state.form_data['NxtPhoneNo'])
                    
                    
                    st.write('Contact saved successfully.')
                    st.success(f"Patient Registration is complete. The generated Registration ID is: {st.session_state.form_data['PATID']}")

# --------------------------Next of Kin's Details------------------------------
# --------------------------------Search Module--------------------------------

if menu == 'Search':
    st.markdown("""
    <div style="background:#000080 ;padding:10px">
    <h2 style="color:white;text-align:center;">Search Patient's Details</h2>
    </div>
    """, unsafe_allow_html=True)

    # Text input for searching by patient details
    PatientID = st.text_input('Enter Patient ID:', key='PatientID')
    PatientFirstName = st.text_input('Enter Patient\'s First Name:', key='PatientFirstName')
    PatientLastName = st.text_input('Enter Patient\'s Last Name:', key='PatientLastName')

    if st.button('Search'):
        if PatientID or PatientFirstName or PatientLastName:  # Proceed if any field is filled
            try:
                # Create a cursor object to execute queries
                cursor = conn.cursor()

                # Query to search for the matching details in the database
                query = "SELECT * FROM tblPATIENT WHERE PATID = ? OR FName = ? OR LName = ?"

                # Execute the SQL query using the cursor and parameterized query to prevent SQL injection
                cursor.execute(query, (PatientID, PatientFirstName, PatientLastName))

                # Fetch the first matching record (assuming one match is enough)
                result = cursor.fetchone()

                # Check if a result was found
                if result:
                    # Populate the form with the patient details
                    PatID = result[0]
                    FName = result[2]
                    LName = result[3]
                    Gender = result[5]
                    MaritalStatus = result[6]
                    StateOfOrigin = result[7]
                    DOB = result[8]
                    PhoneNo = result[9]
                    Email = result[10]

                    # Close the cursor
                    cursor.close()

                    # Display form with populated values
                    st.markdown("### Patient Details")
                    col1, col2 = st.columns(2)

                    with col1:
                        st.text_input('Patient ID', value=PatID, key='PatID')
                        st.text_input('First Name', value=FName, key='FName')
                        st.text_input('Last Name', value=LName, key='LName')
                        st.text_input('Gender', value=Gender, key='Gender')

                    with col2:
                        st.text_input('Marital Status', value=MaritalStatus, key='MaritalStatus')
                        st.text_input('State of Origin', value=StateOfOrigin, key='StateOfOrigin')
                        st.date_input('Date of Birth', value=DOB, key='DOB')
                        st.text_input('Phone Number', value=PhoneNo, key='PhoneNo')
                        st.text_input('Email Address', value=Email, key='Email')

                else:
                    st.warning('No records found for the given details.')

            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning('Please enter at least one field to search.')



# --------------------------------Search Module--------------------------------
# ---------------------------Update Module-------------------------------------
else: # menu == 'Update':
    # st.markdown("""
    # <div style="background:#000080 ;padding:10px">
    # <h2 style="color:white;text-align:center;">Update Patient's Details</h2>
    # </div>
    # """, unsafe_allow_html=True)
    # st.header("Welcome to ChristBay Hospital")
    pass

# ---------------------------Update Module-------------------------------------