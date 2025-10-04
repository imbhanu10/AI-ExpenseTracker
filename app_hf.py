import os
import json
import streamlit as st
import google.generativeai as genai

# Configure the Google API key from environment variable
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    st.error("Google API key not found. Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# Rest of your existing app.py code follows...
# [Previous content of app.py from line 1 to the end]
