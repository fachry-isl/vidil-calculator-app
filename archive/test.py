import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

@st.cache_data
def fetch_data_from_google_sheet(sheet_id, worksheet_name):
    """
    Fetch data from a specific worksheet of the Google Sheet.
    """
    # Create a connection object.
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Fetch data from the specified worksheet
    df = conn.read(spreadsheet_id=sheet_id, worksheet=worksheet_name)
    return pd.DataFrame(df)

SHEET_ID = "1wtbl4cC3Qc98FFM6KFjR1-k9fRQ7uC-Go4pKaancUAc"
st.write("CCTV Data:", fetch_data_from_google_sheet(SHEET_ID, "Camera and CCTV(App)").head())
st.write("DVR/NVR Data:", fetch_data_from_google_sheet(SHEET_ID, "NVR/DVR(App)").head())
st.write("Installation Data:", fetch_data_from_google_sheet(SHEET_ID, "Installation(App)").head())
