# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 19:09:38 2024

@author: KesBes
"""
import streamlit as st
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dbconnect import init_connection

conn = init_connection()
cursor = conn.cursor()
def patDashboard():   
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