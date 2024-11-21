import streamlit as st
from PIL import Image
import hashlib
from dbconnect import init_connection
from Hospital import hospital_portal
import time

# ---------------- Initialize session state ----------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None
if "page" not in st.session_state:
    st.session_state["page"] = "login"

# ----------------------------Load the Logo------------------------------------
img = Image.open('C:/Users/Fatima/Desktop/Emro/kescare_logo.png')

# -----------------------------Page Title--------------------------------------
st.set_page_config(
    page_title='Christbay Consultants Hospital Registration System',
    page_icon=img,
    layout="wide",
)

# -------------------------------App Logo--------------------------------------
st.text('')
st.text('')
st.text('')
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    st.image(img, width=150)

with col2:
    st.markdown(
        """
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
        """,
        unsafe_allow_html=True,
    )
# -------------------------------App Logo--------------------------------------

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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

# Logout function
def logout():
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.session_state["page"] = "login"
    st.sidebar.success("You have been logged out!")

# Login function
def login():
    if not st.session_state["authenticated"]:
        # Add some spacing above the login form
        st.text("")
        st.text("")

        # Center the login UI using columns
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.markdown("<h3 style='text-align: center;'>Login</h3>", unsafe_allow_html=True)
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")

            # Center the Login button
            login_button = st.button("Login", key="login_button")

            if login_button:
                if authenticate_user(username, password):
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username  # Cache the username
                    st.session_state["page"] = "hospital_portal"
                    st.rerun()  # Redirect to the hospital portal page
                else:
                    st.error("Invalid username or password.")

# Main execution logic
if __name__ == "__main__":
    if st.session_state["authenticated"]:
        # Sidebar logout button
        with st.spinner('Loading...'):
            time.sleep(5)
        with st.sidebar:
            st.write(f"Welcome: **{st.session_state['username']}**")
            st.button("Logout", key="logout_button", on_click=logout)

        # Load the hospital portal
        hospital_portal()
    else:
        login()



#============================ Working properly=================================
# # -*- coding: utf-8 -*-
# """
# Created on Mon Nov 11 06:48:26 2024

# @author: KesBes
# """

# import streamlit as st
# from PIL import Image
# import hashlib
# from dbconnect import init_connection
# from Hospital import hospital_portal
# import time
# # ------------------------ Initialize session state ---------------------------
# if "authenticated" not in st.session_state:
#     st.session_state["authenticated"] = False
# if "page" not in st.session_state:
#     st.session_state["page"] = "login"
# # ------------------------ Initialize session state ---------------------------
# # ----------------------------Load the Logo------------------------------------
# img = Image.open('C:/Users/Fatima/Desktop/Emro/kescare_logo.png')

# # -----------------------------Page Title--------------------------------------
# st.set_page_config(
#     page_title='Christbay Consultants Hospital Registration System',
#     page_icon=img,
#     layout="wide",
# )

# # -------------------------------App Logo--------------------------------------
# st.text('')
# st.text('')
# st.text('')
# col1, col2, col3 = st.columns([1, 3, 1])

# with col1:
#     st.image(img, width=150)

# with col2:
#     st.markdown(
#         """
#         <style>
#         h5 {
#             text-align: center;
#             font-size: 14px;
#             margin-bottom: 3px;
#             font-weight: bold;
#         }
#         p {
#             text-align: justify;
#             font-size: 14px;
#             line-height: 1.6;
#             margin-bottom: 15px;
#         }
#         </style>
        
#         <h4>Quality healthcare services at your fingertips!</h4>
#         <p>ChristBay Hospital is dedicated to providing top-notch medical \
#             services. You can register 
#         patients using this application. Follow the steps to complete the patient \
#             registration process.</p>
#         """,
#         unsafe_allow_html=True,
#     )
# # -------------------------------App Logo--------------------------------------

# # Function to hash passwords
# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# # def login_clicked(Username, Password):
    
# # Function to authenticate user
# def authenticate_user(username, password):
#     hashed_password = hash_password(password)
#     conn = init_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT Password FROM staff WHERE username = ?", username)
#     record = cursor.fetchone()
#     conn.close()
#     if record and record[0] == hashed_password:
#         return True
#     return False

# # Logout function
# def logout():
#     st.session_state["authenticated"] = False
#     st.session_state["page"] = "login"
#     # with st.spinner('Logging Off...'):
#     #     time.sleep(5)
#     st.sidebar.success("You have been logged out!")

# # Login function
# def login():
#     if not st.session_state["authenticated"]:
#         # Login UI
#         username = st.text_input("Username", key="login_username")
#         password = st.text_input("Password", type="password", key="login_password")

#         if st.button("Login", key="login_button"):
#             if authenticate_user(username, password):
#                 st.session_state["authenticated"] = True
#                 st.session_state["page"] = "hospital_portal"
#                 # st.success("Login successful! Redirecting...")
                
#             else:
#                 st.error("Invalid username or password.")

# # Main execution logic
# if __name__ == "__main__":
#     if st.session_state["authenticated"]:
        
#         with st.spinner('Loading...'):
#              # st.snow()
#              time.sleep(5)
          
#         # Sidebar logout button
#         with st.sidebar:
            
#             st.button("Logout", key="logout_button", on_click=logout)
#         hospital_portal()  # Load the hospital portal       
#     else:
#         login() # Call login pass if authentication is unsuccessfu




