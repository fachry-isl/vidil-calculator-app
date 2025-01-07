import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Google Sheets API setup
def fetch_data_from_google_sheet(sheet_id, worksheet_name):
    """
    Fetch data from a specific worksheet of the Google Sheet.
    """
    # Create a connection object.
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Fetch data from the specified worksheet
    df = conn.read(spreadsheet_id=sheet_id, worksheet=worksheet_name)
    return pd.DataFrame(df)

# App Title
st.title("CCTV Solution Cost Calculator")

# Google Sheets setup
SHEET_ID = "1wtbl4cC3Qc98FFM6KFjR1-k9fRQ7uC-Go4pKaancUAc"  # Replace with your actual Google Sheet ID
CCTV_WORKSHEET = "Camera and CCTV(App)"  # Replace with the worksheet name for CCTV data
DVR_NVR_WORKSHEET = "NVR/DVR(App)"  # Replace with the worksheet name for DVR/NVR data
INSTALLATION_WORKSHEET = "Installation(App)"  # Replace with the worksheet name for Installation data

# Load Data from Google Sheets
try:
    cctv_data = fetch_data_from_google_sheet(SHEET_ID, CCTV_WORKSHEET)
    dvr_nvr_data = fetch_data_from_google_sheet(SHEET_ID, DVR_NVR_WORKSHEET)
    installation_data = fetch_data_from_google_sheet(SHEET_ID, INSTALLATION_WORKSHEET)
    st.sidebar.success("Data loaded successfully!")
except Exception as e:
    st.sidebar.error(f"Error loading data: {e}")
    cctv_data = pd.DataFrame()
    dvr_nvr_data = pd.DataFrame()
    installation_data = pd.DataFrame()

# Sidebar: Select Components
st.sidebar.header("Select Components")
include_cctv = st.sidebar.checkbox("CCTV", value=True)
include_dvr_nvr = st.sidebar.checkbox("DVR/NVR", value=True)
include_installation = st.sidebar.checkbox("Installation", value=True)

costs = {}

# CCTV Section
if include_cctv and not cctv_data.empty:
    st.subheader("CCTV")
    
    # Search or Select CCTV
    cctv_options = cctv_data["Model"].tolist()  # Adjust column name
    selected_cctv = st.selectbox("Select a CCTV Device", options=[""] + cctv_options)
    
    if selected_cctv:
        # Display selected CCTV details
        cctv_details = cctv_data[cctv_data["Model"] == selected_cctv].iloc[0]
        st.write("Selected CCTV Details:")
        st.json(cctv_details.to_dict())
        
        # Add quantity input
        cctv_quantity = st.number_input("Number of CCTVs", min_value=1, value=1, step=1)
        
        # Calculate cost
        cctv_price = cctv_details["Price"]  # Adjust column name
        costs['CCTV'] = cctv_quantity * cctv_price
    else:
        st.info("Select a CCTV device to continue.")

# DVR/NVR Section
if include_dvr_nvr and not dvr_nvr_data.empty:
    st.subheader("DVR/NVR")
    
    # Search or Select DVR/NVR
    dvr_nvr_options = dvr_nvr_data["Model"].tolist()  # Adjust column name
    selected_dvr_nvr = st.selectbox("Select a DVR/NVR Device", options=[""] + dvr_nvr_options)
    
    if selected_dvr_nvr:
        # Display selected DVR/NVR details
        dvr_nvr_details = dvr_nvr_data[dvr_nvr_data["Model"] == selected_dvr_nvr].iloc[0]
        st.write("Selected DVR/NVR Details:")
        st.json(dvr_nvr_details.to_dict())
        
        # Add quantity input
        dvr_nvr_quantity = st.number_input("Number of DVR/NVR Units", min_value=1, value=1, step=1)
        
        # Calculate cost
        dvr_nvr_price = dvr_nvr_details["Price"]  # Adjust column name
        costs['DVR/NVR'] = dvr_nvr_quantity * dvr_nvr_price
    else:
        st.info("Select a DVR/NVR device to continue.")

# Installation Section
if include_installation and not installation_data.empty:
    st.subheader("Installation")
    # Select Installation Type
    installation_options = installation_data["Installation Package"].tolist()  # Adjust column name
    selected_installation = st.selectbox("Select Installation Type", options=[""] + installation_options)
    
    if selected_installation:
        # Display selected Installation details
        installation_details = installation_data[installation_data["Installation Package"] == selected_installation].iloc[0]
        st.write("Selected Installation Details:")
        st.json(installation_details.to_dict())
        
        # Add cost directly (assuming one-time fee)
        installation_cost = installation_details["Price Middle"]  # Adjust column name
        costs['Installation'] = installation_cost
    else:
        st.info("Select an installation type to continue.")

# Calculate Total
total_cost = sum(costs.values())
st.markdown("---")
st.subheader(f"Total Cost: Rp.{total_cost:,.0f}")

# Optional: Display Breakdown
if st.checkbox("Show Cost Breakdown"):
    st.write(costs)

# Export as Report
if st.button("Generate Report"):
    report = f"""
    CCTV Solution Cost Breakdown:
    {costs}

    Total Cost: Rp.{total_cost:,.0f}
    """
    st.download_button("Download Report", report, "cost_report.txt")
