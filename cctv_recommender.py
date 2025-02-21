import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import extra_streamlit_components as stx

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
def update_sidebar_metrics(filtered_data, container):
    """
    Updates the metrics displayed in the sidebar dynamically based on filtered data.
    """
    container.write("### Statistics")
    total_matched = len(filtered_data)
    avg_price = filtered_data["Price"].mean() if not filtered_data.empty else 0
    min_price = filtered_data["Price"].min() if not filtered_data.empty else 0
    max_price = filtered_data["Price"].max() if not filtered_data.empty else 0

    container.metric(label="Total matched CCTV", value=total_matched)
    container.progress(total_matched / len(cctv_data))
    container.metric(label="Average Price (Rp.)", value=f"{avg_price:,.0f}")
    container.metric(label="Max Price (Rp.)", value=f"{max_price:,.0f}")
    container.metric(label="Min Price (Rp.)", value=f"{min_price:,.0f}")


# Sidebar Refresh
#update_sidebar_metrics(st.session_state.finder_data)

usecase_model_map = {
    "Retail": ["Customer Behaviour Analysis", "Loss Prevention & Security", "Automated Checkout & Queue Management"],
    "Mining": ["Worker Safety & Compliance", "Operational Efficiency & Equipment Monitoring", "Environmental & Perimeter Security"],
    "Banking": ["Fraud Prevention & ATM Security", "Branch Optimization & Customer Experience", "Access Control & Security Monitoring"]
}

#tabs1, tabs2 = st.tabs(['Based on Specs', 'Based on Usecase'])
with st.container(border=True):
    st.markdown("###### Choose your preference")
    chosen_id = stx.tab_bar(default="tab1", data=[
        stx.TabBarItemData(id="tab1", title="Specification", description="Based on CCTV Specification"),
        stx.TabBarItemData(id="tab2", title="Usecase", description="Based on Industry Usecases")])

if chosen_id == "tab1":
    placeholder = st.sidebar.container() 
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
    update_sidebar_metrics(filtered_data, placeholder)

    generate_recommendation = st.button("Generate Recommendation")

    if generate_recommendation:
        st.dataframe(filtered_data[["Brand", "Model", "Resolution*", "Outdoor", "Connectivity", "Power Source", "Price"]])
        
        
elif chosen_id == "tab2":
    placeholder = st.sidebar.container() 
    
    usecase = None
    
    # Filter data based on user selections
    filtered_data = cctv_data.copy()
    
    st.subheader("Industry")
    industry = st.selectbox("Choose your Industry", ["Retail", "Banking", "Mining"], index=None)
    
    if industry != None:
        st.subheader("Usecase")
        usecase = st.selectbox("Choose your Usecase", usecase_model_map[industry], index=None)
        
    # Convert FPS column to integer by extracting numbers
    filtered_data['Frame Rate'] = filtered_data['Frame Rate'].str.extract(r'(\d+)').astype(float)

    # Convert Resolution* column to integer by extracting numbers
    filtered_data['Resolution*'] = filtered_data['Resolution*'].str.extract(r'(\d+)').astype(float)

        
    if usecase == "Customer Behaviour Analysis":
        st.markdown("""
            
            Goal:
            - Improve Customer Shopping Experience - Store Layout Optimization.
            - Improve Operational Efficiency - Inventory Management, Customer.
            - Improve Sales - Product Placement, Marketing Effectiveness.
            
            Analytics:
            - KPIs: Orders, Shopper Count, Basket Size and Checkout time.
            - Sales growth vs. share, sales growth v shelf placement.
            - Visualizations such as heat maps and customer journey.
            
            Recommended CCTV Specs:
            - 4MP-8MP resolution provides enough detail to track individual customers while covering large areas
            - 15-30 fps is sufficient for tracking walking customers - no need for higher framerates
            -  Wide-angle lenses recommended to cover maximum floor space with fewer cameras
            - Lower framerate (15 fps) acceptable for heat mapping and general movement patterns
            - AI analytics capabilities needed for automatic pattern recognition and customer counting
            """)
        
        with st.expander("Location Detail"):
            st.image("./assets/retail_location.png", use_container_width=True)
        
        tabs_cust1, tabs_cust2 = st.tabs(['General', 'Heatmap'])
        
        with tabs_cust1:
            # Apply the filtering conditions
            filtered_data = filtered_data[
                (filtered_data['Resolution*'].between(4, 8)) &  # Resolution condition (4MP-8MP)
                (filtered_data['Frame Rate'].between(15, 30)) &  # FPS condition (15-30 FPS)
                (filtered_data['Outdoor'] == "No")   # Indoor condition
            ]
        
            st.dataframe(filtered_data[["Brand", "Model", "Resolution*", "Outdoor", "Connectivity", "Power Source", "Price"]])
        with tabs_cust2:
            st.warning("Please note that the data for this usecase is not available.", icon='⚠️')
            
        

    elif usecase == "Loss Prevention & Security":
        st.markdown("""
                    Recommended CCTV Specs:
                    - 4K resolution crucial for facial details and evidence-quality footage
                    - 30 fps needed to capture quick movements and prevent motion blur
                    - IR illumination important for after-hours security
                    - Higher resolution helps identify small objects like concealed merchandise
                    - Facial recognition requires high detail for accuracy, hence 4K 
                    """)
        # Apply the filtering conditions
        filtered_data = filtered_data[
            (filtered_data['Resolution*'] == 8) &
            (filtered_data['Frame Rate'] == 30) &
            (filtered_data['Outdoor'] == "No")
        ]
        
        st.dataframe(filtered_data[["Brand", "Model", "Resolution*", "Outdoor", "Connectivity", "Power Source", "Price"]])
    elif usecase == "Automated Checkout & Queue Management":
        st.markdown("""
                    Recommended CCTV Specs:
                    - 2MP-4MP sufficient for overhead views of checkout areas
                    - Higher framerate (30-60 fps) needed to track quick hand movements for item picking
                    - Ceiling-mounted for best view of queues and checkout activity
                    - Lower resolution acceptable as cameras are typically mounted closer to subjects
                    """)
        # Apply the filtering conditions
        filtered_data = filtered_data[
            (filtered_data['Resolution*'].between(2, 4)) &
            (filtered_data['Frame Rate'].between(30, 60)) &
            (filtered_data['Outdoor'] == "No")
        ]
        st.dataframe(filtered_data[["Brand", "Model", "Resolution*", "Outdoor", "Connectivity", "Power Source", "Price"]])
    elif usecase ==  "Worker Safety & Compliance":
        st.markdown("""
                    Recommended CCTV Specs:
                    - High resolution needed to clearly identify safety equipment (helmets, vests)
                    - 30 fps captures normal movement well
                    - IP67 rating essential for dust protection
                    - IR capability needed for low-light underground operations
                    - Must be explosion-protected in certain areas """)
        # Apply the filtering conditions
        filtered_data = filtered_data[
            (filtered_data['Resolution*'].between(4, 8)) &
            (filtered_data['Frame Rate'] == 30) &
            (filtered_data['IP Rating*'] == "IP67")
        ]
        st.dataframe(filtered_data[["Brand", "Model", "Resolution*", "Outdoor", "Connectivity", "Power Source", "Price"]])
    elif usecase == "Operational Efficiency & Equipment Monitoring":
        st.markdown("""
                    Recommended CCTV Specs:
                    - Thermal imaging crucial for equipment temperature monitoring
                    - Dual sensors (thermal + optical) provide comprehensive monitoring
                    - Lower thermal resolution sufficient for heat detection
                    - 4K optical for clear visual inspection
                    - Vibration resistance important near heavy machinery
                    """)
        st.warning("Please note that the data for this usecase is not available.", icon='⚠️')
    elif usecase == "Environmental & Perimeter Security":
        st.markdown("""
                    Recommended CCTV Specs:
                    - 4K resolution needed for long-range perimeter monitoring
                    - Long-range IR for nighttime surveillance
                    - Wide dynamic range for varying lighting conditions
                    - Robust housing for extreme weather conditions
                    - High resolution helps detect small changes in environmental conditions
                    """)
        
        filtered_data = filtered_data[
            (filtered_data['Resolution*'] == 8) &
            (filtered_data['Outdoor'] == "Yes")
        ]
        st.dataframe(filtered_data[["Brand", "Model", "Resolution*", "Outdoor", "Connectivity", "Power Source", "Price"]])
    elif usecase == "Fraud Prevention & ATM Security":
        st.markdown("""
                    Recommended CCTV Specs:
                    - 4K essential for facial details and transaction evidence
                    - Higher framerate captures quick movements like card skimmer installation
                    - WDR crucial for handling bright outdoor/dark indoor transitions
                    - Multiple angles needed to capture all ATM interaction points
                    - Anti-vandal design for public-facing cameras 
                    """)
        
        filtered_data = filtered_data[
            (filtered_data['Resolution*'] == 8) &
            (filtered_data['Frame Rate'] == 30) &
            (filtered_data['Outdoor'] == "Yes")
        ]
        st.dataframe(filtered_data[["Brand", "Model", "Resolution*", "Outdoor", "Connectivity", "Power Source", "Price"]])
    elif usecase == "Branch Optimization & Customer Experience":
        st.markdown("""
                    Recommended CCTV Specs:
                    - Resolution sufficient for people counting and movement tracking
                    - Lower framerate acceptable for general movement analysis
                    - Heat mapping requires good overhead coverage
                    - Multi-sensor cameras provide better coverage of large areas
                    - Analytics for queue measurement and customer flow
                    """)
        st.dataframe(filtered_data[["Brand", "Model", "Resolution*", "Outdoor", "Connectivity", "Power Source", "Price"]])
    elif usecase == "Access Control & Security Monitoring":
        st.markdown("""
                    Recommended CCTV Specs:
                    - 4K resolution crucial for accurate facial recognition
                    - 30 fps captures natural walking pace
                    - Advanced facial recognition requires high detail
                    - Good low-light performance for varying conditions
                    - Multi-factor authentication integration capability
                    """)
        st.dataframe(filtered_data[["Brand", "Model", "Resolution*", "Outdoor", "Connectivity", "Power Source", "Price"]]) 
    update_sidebar_metrics(filtered_data, placeholder)
    

        
