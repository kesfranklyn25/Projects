# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 15:37:49 2024

@author: KesBes
"""

import pyodbc
import streamlit as st

# connection = pyodbc.connect(
#         'DRIVER={ODBC Driver 17 for SQL Server};'
#         'SERVER=hostname;'
#         'DATABASE=databasename;'
#         'UID=username;'
#         'PWD=password'
#     )
# cursor = connection.cursor()
# cursor.execute("SELECT @@version;")
# db_version = cursor.fetchone()
# print(f"Connected to SQL Server. Version: {db_version}")


# -------------------------Database Connetion----------------------------------


# # @st.cache_resource
# def init_connection():
#     connection_string = (
#         f"DRIVER={{ODBC Driver 17 for SQL Server}};"
#         f"SERVER={st.secrets['database']['server']};"
#         f"DATABASE={st.secrets['database']['database']};"
#         f"UID={st.secrets['database']['username']};"
#         f"PWD={st.secrets['database']['password']}"
#     )
#     return pyodbc.connect(connection_string)

# conn = init_connection()

# @st.cache_resource
def init_connection():
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={st.secrets['database']['matnafoods.com.ng']};"
        f"DATABASE={st.secrets['database']['matnafoo_CBH']};"
        f"UID={st.secrets['database']['matnafoo_kesbes']};"
        f"PWD={st.secrets['database']['My#ame@2505']}"
    )
    try:
        conn = pyodbc.connect(connection_string, timeout=10)
        return conn
    except pyodbc.OperationalError as e:
        error_message = str(e)
        if "Named Pipes Provider" in error_message:
            st.error("⚠️ Unable to connect to the database. Please check the following:")
            st.markdown(
                """
                - Ensure the SQL Server is running and accessible.
                - Verify that the server name is correct in your configuration.
                - Check if remote connections are enabled for SQL Server.
                - Make sure the SQL Server firewall allows incoming connections on the specified port.
                """
            )
        elif "Login timeout expired" in error_message:
            st.error("⏳ Connection to the database timed out. Please try again later.")
        else:
            st.error("🚨 A database connection error occurred. Please contact the system administrator.")

        # Log technical details for debugging
        with open("db_error_log.txt", "a") as log_file:
            log_file.write(f"OperationalError: {error_message}\n")
        
        # Reraise for developer-level debugging if needed
        raise
    except Exception as e:
        st.error("An unexpected error occurred. Please contact the system administrator.")
        
        # Log technical details for debugging
        with open("db_error_log.txt", "a") as log_file:
            log_file.write(f"General Error: {str(e)}\n")
        
        # Reraise for developer-level debugging if needed
        raise



# Function to insert data into the database
def insert_data(action, *args):
    conn = init_connection()
    cursor = conn.cursor()
    if action == 'Card Details':
        cursor.execute("""
            INSERT INTO tblCard(RegID, RegDate, CardClass, CardType, \
                                ShelveNo,HMO)
            VALUES (?, ?, ?, ?, ?, ?)
        """, args)
    elif action == 'Personal Details':
        cursor.execute("""
            INSERT INTO tblPATIENT(PATID,RegID,FName, LName, MName, \
                                   Gender, MStatus,\
            StateOfOrigin, DateOfBirth, PhoneNo, EmailAddress) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, args)
    elif action == 'Contact Details':
        cursor.execute("""
            INSERT INTO tblAddress (PATID, HouseNo, StreetName, City, State, \
                                    PostCode, Country) 
            VALUES (?, ?, ?,?, ?, ?, ?)
        """, args)
        
    elif action == 'Next of Kin Details':
        cursor.execute("""
            INSERT INTO tblNEXTOFKIN (PATID,nxtFName, nxtLName, \
                                      nxtRelationship, nxtEmailAddress, \
                                      nxtPhoneNo) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, args)	
    elif action =='New Staff':
        cursor.execute("""
                    INSERT INTO staff(Username, RegDate, FName, LName, \
                                        Password,ModifiedDate, DeptID)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
        """, args)				
    conn.commit()
    cursor.close()
    # conn.close()
    
# --------------------------Database Connection Ends---------------------------
