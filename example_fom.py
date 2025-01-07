import streamlit as st
import pandas as pd

# Load your camera database (replace with your actual Google Sheets integration)
# Example: df = pd.read_csv('camera_database.csv')
camera_database = [
    {"name": "Basic Indoor Camera", "resolution": "720p", "field_of_view": "90°", "night_vision": "No", "wireless": "Yes", "price": 50, "type": "Indoor"},
    {"name": "Mid-Range Outdoor Camera", "resolution": "1080p", "field_of_view": "120°", "night_vision": "Yes", "wireless": "Yes", "price": 150, "type": "Outdoor"},
    {"name": "Premium Outdoor Camera", "resolution": "4K", "field_of_view": "120°+", "night_vision": "Yes", "wireless": "No", "price": 300, "type": "Outdoor"},
]
df = pd.DataFrame(camera_database)

# Streamlit app
st.title("CCTV Recommendation System")

# Form for user input
with st.form("cctv_form"):
    # Monitoring Area
    space_type = st.selectbox("What kind of space do you want to monitor?", ["Room", "House or Office", "Yard or Parking Lot", "Other"])
    indoor_outdoor = st.selectbox("Is the space indoors or outdoors?", ["Indoors", "Outdoors", "Both"])
    area_size = st.selectbox("How big is the area?", ["Small", "Medium", "Large"])

    # Camera Features
    night_vision = st.radio("Do you need the cameras to work at night?", ["Yes", "No", "I’m not sure"])
    video_clarity = st.selectbox("How clear should the video be?", ["Basic clarity", "Sharp and detailed", "Very clear"])
    wireless = st.radio("Do you want cameras that can connect wirelessly?", ["Yes", "No", "I’m not sure"])
    motion_detection = st.radio("Do you want the cameras to notify you of movement?", ["Yes", "No", "I’m not sure"])

    # Number of Devices
    num_cameras = st.slider("How many cameras do you think you'll need?", 1, 10, 2)
    need_recorder = st.radio("Do you need a recorder to save the videos?", ["Yes", "No", "I’m not sure"])

    # Budget
    camera_budget = st.selectbox("What’s your budget for each camera?", ["Affordable", "Mid-range", "Premium"])
    total_budget = st.number_input("What’s your total budget for the entire setup?", value=1000)

    submitted = st.form_submit_button("Get Recommendations")

# Mapping logic
if submitted:
    # Map user answers to specs
    resolution_map = {
        "Basic clarity": "720p",
        "Sharp and detailed": "1080p",
        "Very clear": "4K",
    }
    resolution = resolution_map[video_clarity]

    field_of_view_map = {
        "Small": "90°",
        "Medium": "120°",
        "Large": "120°+",
    }
    field_of_view = field_of_view_map[area_size]

    type_map = {
        "Indoors": "Indoor",
        "Outdoors": "Outdoor",
        "Both": "Indoor/Outdoor",
    }
    camera_type = type_map[indoor_outdoor]

    # Filter database based on user inputs
    recommendations = df[
        (df["resolution"] == resolution) &
        (df["field_of_view"] == field_of_view) &
        (df["type"] == camera_type) &
        (df["price"] <= total_budget / num_cameras)
    ]

    # Display recommendations
    if not recommendations.empty:
        st.success("We found the following recommendations for you:")
        for _, row in recommendations.iterrows():
            st.write(f"- **{row['name']}**: ${row['price']} each")
    else:
        st.error("No cameras match your requirements. Try adjusting your inputs.")

# Additional logic for NVR and installation costs can be added here.
