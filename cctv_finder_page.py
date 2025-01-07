import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("CCTV Recommendation System")

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
   
# Initialize data from Google Sheets
SHEET_ID = "1wtbl4cC3Qc98FFM6KFjR1-k9fRQ7uC-Go4pKaancUAc"  # Replace with your actual Google Sheet ID
CCTV_WORKSHEET = "Camera and CCTV(App)"  # Replace with the worksheet name for CCTV data
# Load Data from Google Sheets
try:
    cctv_data = fetch_data_from_google_sheet(SHEET_ID, CCTV_WORKSHEET)
except Exception as e:
    st.sidebar.error(f"Error loading data: {e}")
    cctv_data = pd.DataFrame()

# Initialize session state for variables if not already initialized
if "finder_data" not in st.session_state:
    st.session_state.finder_data = cctv_data

# Sidebar: Metrics
def update_sidebar_metrics(filtered_data):
    """
    Updates the metrics displayed in the sidebar dynamically based on filtered data.
    """
    st.sidebar.write("### Statistics")
    total_matched = len(filtered_data)
    avg_price = filtered_data["Price"].mean() if not filtered_data.empty else 0
    min_price = filtered_data["Price"].min() if not filtered_data.empty else 0
    max_price = filtered_data["Price"].max() if not filtered_data.empty else 0

    st.sidebar.metric(label="Total matched CCTV", value=total_matched)
    st.sidebar.progress(total_matched / len(cctv_data))
    st.sidebar.metric(label="Average Price (Rp.)", value=f"{avg_price:,.0f}")
    st.sidebar.metric(label="Max Price (Rp.)", value=f"{max_price:,.0f}")
    st.sidebar.metric(label="Min Price (Rp.)", value=f"{min_price:,.0f}")


# Sidebar Refresh
#update_sidebar_metrics(st.session_state.finder_data)



st.subheader("Resolution")
resolution = st.selectbox("Choose the level of detail of your camera", ["Basic", "Sharp", "Very Clear"], index=None)


options = {
    "Basic Clarity (Good for Small Areas)": "Ideal for small spaces, motion detection, presence detection, and monitoring basic activities. (Low resolution, good for general use)",
    "Sharp and Detailed (Good for Recognizing Faces)": "Perfect for medium spaces requiring facial recognition, intruder detection, and behavior analysis. (1080p resolution, suitable for offices and retail)",
    "Very Clear (Good for Seeing Small Details or Big Spaces)": "Best for large areas or precise tasks like license plate recognition, crowd analysis, or detailed quality control. (4K resolution, suited for large venues or industrial use)"
}

for key, value in options.items():
    st.write(f"**{key}**: {value}")


st.subheader("Indoor or Outdoor")
outdoor = st.selectbox("Where will you install the cameras?", ["Indoor", "Outdoor"], index=None)


st.subheader("Connectivity")
connectivity = st.selectbox("How does your camera will send or receive data? Choose your connection type", ["Ethernet", "4G SIM", "Wi-Fi"], index=None)

st.subheader("Power Source")
power_source = st.selectbox("How will you power the camera?", ["Cable", "Solar Panel"], index=None)

resolution_map = {
    "2MP": "Basic",
    "3MP": "Basic",
    "4MP": "Sharp",
    "5MP": "Sharp",
    "6MP": "Very Clear",
    "8MP": "Very Clear"
}

outdoor_map = {
    "No": "Indoor",
    "Yes": "Outdoor"
}
   
    
# Filter data based on user selections
filtered_data = cctv_data.copy()

# Apply resolution filter
if resolution is not None:
    filtered_data = filtered_data[
        filtered_data["Resolution*"].apply(lambda x: resolution_map.get(x) == resolution)
    ]

# Apply outdoor filter
if outdoor is not None:
    filtered_data = filtered_data[
        filtered_data["Outdoor"].apply(lambda x: outdoor_map.get(x) == outdoor)
    ]

# Apply connectivity filter
if connectivity is not None:
    filtered_data = filtered_data[
        filtered_data["Connectivity"] == connectivity
    ]

# Apply power source filter
if power_source is not None:
    filtered_data = filtered_data[
        filtered_data["Power Source"] == power_source
    ]


# Update metrics in the sidebar
update_sidebar_metrics(filtered_data)



generate_recommendation = st.button("Generate Recommendation")

if generate_recommendation:
    st.dataframe(filtered_data[["Brand", "Model", "Resolution*", "Outdoor", "Connectivity", "Power Source", "Price"]])
    


