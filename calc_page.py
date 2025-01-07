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

connectivity_plan = {
    "5GB":85000,
    "10GB":135000,
    "20GB":240000,
    "30GB":345000,
    "50GB":560000,
    "75GB":822000,
    "100GB":1085000,
    "500GB":5305000,
    "750GB":7942000,
    "1000GB":10579000
}
cloud_plan = {
    "Shared": 1_000_000, 
    "Dedicated": 21_160_203
}

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
    #st.sidebar.success("Data loaded successfully!")
except Exception as e:
    st.sidebar.error(f"Error loading data: {e}")
    cctv_data = pd.DataFrame()
    dvr_nvr_data = pd.DataFrame()
    installation_data = pd.DataFrame()


# Sidebar: Select Components
st.sidebar.header("Configuration Form")
st.sidebar.write("(Select Parameter to Include)")
include_cctv = st.sidebar.checkbox("CCTV", value=True)
include_dvr_nvr = st.sidebar.checkbox("DVR/NVR", value=True)
include_installation = st.sidebar.checkbox("Installation", value=True)
include_platform = st.sidebar.checkbox("Platform", value=False)
include_license = st.sidebar.checkbox("License", value=False)
include_cloud = st.sidebar.checkbox("Cloud", value=False)
include_connectivity = st.sidebar.checkbox("Connectivity", value=False)

include_additional_item = st.sidebar.checkbox("Additional Items")

# Two-column layout
col1, col2 = st.columns([2, 1])

# Costs dictionary to hold calculated costs
unit_price = {}
costs = {}

with col1:
    # CCTV Section
    if include_cctv and not cctv_data.empty:
        st.subheader("CCTV")
        cctv_options = cctv_data["Model"].tolist()  # Adjust column name
        selected_cctv = st.selectbox("Select a CCTV Device", options= cctv_options, index=None)
        if selected_cctv:
            cctv_details = cctv_data[cctv_data["Model"] == selected_cctv].iloc[0]
            cctv_price = cctv_details["Price"]  # Adjust column name
            st.write(f"{selected_cctv} - Rp.{cctv_price:,.0f}")
            cctv_quantity = st.number_input("Number of CCTVs", min_value=1, value=1, step=1)
            unit_price[f'{selected_cctv}'] = cctv_price
            costs[f'{selected_cctv}x({cctv_quantity})'] = cctv_quantity * cctv_price
    
    # DVR/NVR Section
    if include_dvr_nvr and not dvr_nvr_data.empty:
        st.subheader("DVR/NVR")
        dvr_nvr_options = dvr_nvr_data["Model"].tolist()
        selected_dvr_nvr = st.selectbox("Select a DVR/NVR Device", options= dvr_nvr_options, index=None)
        if selected_dvr_nvr:
            dvr_nvr_details = dvr_nvr_data[dvr_nvr_data["Model"] == selected_dvr_nvr].iloc[0]
            dvr_nvr_price = dvr_nvr_details["Price"]
            st.write(f"{selected_dvr_nvr} - {dvr_nvr_details['Channel']:,.0f} Channels - Rp.{dvr_nvr_price:,.0f}")
            dvr_nvr_quantity = st.number_input("Number of DVR/NVR Units", min_value=1, value=1, step=1)
            unit_price[f'{selected_dvr_nvr}'] = dvr_nvr_price
            costs[f'{selected_dvr_nvr}x({dvr_nvr_quantity})'] = dvr_nvr_quantity * dvr_nvr_price

    # Installation Section
    if include_installation and not installation_data.empty:
        st.subheader("Installation")
        installation_options = installation_data["Installation Package"].tolist()
        selected_installation = st.selectbox("Select Installation Type", options=installation_options, index=None)
      
        if selected_installation:
            number_area = st.number_input("Number of Point", min_value=1, step=1)
            installation_details = installation_data[installation_data["Installation Package"] == selected_installation].iloc[0]
            install_complexity_map = {
                0:f"Basic {installation_details['Price Lower']:,.0f}",
                1:f"Intermediate {installation_details['Price Middle']:,.0f}",
                2:f"Advanced {installation_details['Price Upper']:,.0f}"
            }
            

            installation_complexity = st.select_slider("Select Installation Complexity (Affects Price per Point)", 
                options=[f"Basic {installation_details['Price Lower']:,.0f}", 
                         f"Intermediate {installation_details['Price Middle']:,.0f}", 
                         f"Advanced {installation_details['Price Upper']:,.0f}"])
            
            if installation_complexity == install_complexity_map[0]:
                installation_cost = installation_details["Price Lower"]
            elif installation_complexity == install_complexity_map[1]:
                installation_cost = installation_details["Price Middle"]
            elif installation_complexity == install_complexity_map[2]:
                installation_cost = installation_details["Price Upper"]
                
            unit_price[f'{selected_installation}'] = installation_cost
            costs[f'{selected_installation}x({number_area})'] = installation_cost * number_area
            
    # Platform Section
    if include_platform and not installation_data.empty:
        st.subheader("Platform")
        de_quantity = st.number_input("Number of Data Engineer", min_value=1, step=1, value=None)
        ds_quantity = st.number_input("Number of Data Science", min_value=1, step=1, value=None)
        pm_quantity = st.number_input("Number of Project Manager", min_value=1, step=1, value=None)
        mle_quantity = st.number_input("Number of Machine Learning Engineer", min_value=1, step=1, value=None)
        
        if de_quantity != None:
            costs[f'Data Engineerx({de_quantity})'] = 2000_000*de_quantity
        if ds_quantity != None:
            costs[f'Data Sciencex({ds_quantity})'] = 2000_000*ds_quantity
        if pm_quantity != None:
            costs[f'Project Managerx({pm_quantity})'] = 2000_000*pm_quantity
        if mle_quantity != None:
            costs[f'ML Engineerx({mle_quantity})'] = 2000_000*mle_quantity
    
    # License Section
    if include_license and not installation_data.empty:
        st.subheader("License")
        license_package = st.selectbox("Select License Package", options=["Smart Dashboard for Video Intelligence License"], index=None)
        if license_package != None:
            costs[f'Smart Dashboard License'] = 72_900_000 
        
        
    # Cloud Section
    if include_cloud and not installation_data.empty:
        st.subheader("Cloud")
        cloud_package = st.selectbox("Select Cloud Plan", options=list(cloud_plan.keys()), index=None)
        cloud_quantity = st.number_input("Input Number of Months (Cloud)", min_value=1, value=1, step=1)
        if cloud_package != None:
            costs[f'Cloud - {cloud_package} ({cloud_quantity} Months)'] = cloud_plan[cloud_package] * cloud_quantity
        
        
        st.write("Note: Include Maintenance & Warranty Services")
        
    # Connectivity Section
    if include_connectivity and not installation_data.empty:
        st.subheader("Connectivity")
        connectivity_package = st.selectbox("Select Connectivity Plan", list(connectivity_plan.keys()), index=None)
        connectivity_quantity = st.number_input("Input Number of Months (Quota)", min_value=1, value=1, step=1)
        if connectivity_package != None:
            costs[f'Telkomsel Quota - {connectivity_package} ({connectivity_quantity} Months)'] = connectivity_plan[connectivity_package] * connectivity_quantity
           

    # Additional Item Section
    if 'additional_cost_total' not in st.session_state:
        st.session_state['additional_cost_total'] = 0
    if include_additional_item:
        st.subheader("Additional Item")
        item_name = st.text_input("Enter item name")
        item_price = st.number_input("Enter item price", min_value=0.0, step=0.1)
        item_quantity = st.number_input("Enter item quantity", min_value=1, step=1)
        if st.button("Add Custom Item"):
            new_item_cost = item_price * item_quantity
            st.session_state['additional_cost_total'] += new_item_cost
            st.success(f"Item '{item_name}' added successfully!")

with col2:
    st.subheader("Price Breakdown")
    if costs:
        if include_cctv:
                st.markdown("##### CCTV") 
        for item, cost in costs.items():
            st.write(f"{item}: Rp.{cost:,.0f}")

    #st.divider()
    
    total_cost = sum(costs.values()) + st.session_state.get('additional_cost_total', 0)
    st.metric(label="Estimated Total Cost", value=f"Rp.{total_cost:,.0f}")
    
    
    st.subheader("Compability")
    st.warning("Your selected CCTV and DVR/NVR are not compatible.")
    st.warning("Your selected CCTV and Installation are not compatible.")