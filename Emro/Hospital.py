def hospital_portal():
    import streamlit as st
    from streamlit_option_menu import option_menu
    from datetime import datetime
    from pat_dashboard import patDashboard
    from pat_search import search_patient_record
    from pat_update import patupdate
    from registration import registration_module
    from staffCreation import newstaff

# -------------------------Database Connetion----------------------------------
    
    # conn = init_connection()
# --------------------------Database Connection Ends---------------------------
    
    
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

# =========================Sidebar Menu for Navigation=========================
    with st.sidebar:
        menu = option_menu(
            'Patient Registration',
            ['ChristBay', 'Registration', 'Search', 'Update', 'Staff'],
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
# This module displays the dashboard for patients
    if menu == 'ChristBay':
        patDashboard()
       
# ===============================Home Page=====================================  
# =============================Registration Page===============================
# This module is used for patient registration
    elif menu == 'Registration':
        registration_module() # Calls Registration function fron registration module
        
# =============================Registration Page===============================
    
# ================================Search Module================================
# This module handles searches (patients)
    elif menu == 'Search':
       
        search_patient_record()
# ================================Search Module================================
# # ==============================Update Module==================================
    elif menu == 'Update':
        patupdate()  

# # ==============================Update Module==================================
    
# ==============================New Staff Creation=============================
    else:
    # elif menu == 'New Staff':
        newstaff()
# ==============================New Staff Creation=============================
 
# ================================Footer======================================
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