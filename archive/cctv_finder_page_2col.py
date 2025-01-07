import streamlit as st

st.title("CCTV Recommendation System")

# Create two columns
col1, col2 = st.columns([3, 1])

# Left column for form inputs
with col1:
    with st.form("cctv_form"):
        st.subheader("Resolution")
        resolution = st.selectbox("Choose the level of detail of your camera", ["Basic", "Sharp", "Very clear"])
        
        options = {
            "Basic Clarity (Good for Small Areas)": "Ideal for small spaces, motion detection, presence detection, and monitoring basic activities. (Low resolution, good for general use)",
            "Sharp and Detailed (Good for Recognizing Faces)": "Perfect for medium spaces requiring facial recognition, intruder detection, and behavior analysis. (1080p resolution, suitable for offices and retail)",
            "Very Clear (Good for Seeing Small Details or Big Spaces)": "Best for large areas or precise tasks like license plate recognition, crowd analysis, or detailed quality control. (4K resolution, suited for large venues or industrial use)"
        }

        for key, value in options.items():
            st.write(f"**{key}**: {value}")
        
        
        st.subheader("Indoor or Outdoor")
        indoor = st.selectbox("Where will you install the cameras?", ["Indoor", "Outdoor"])
        
        st.subheader("Weather Resistance")
        weather_resistance = st.selectbox("Do you need weather-resistant cameras?", ["No", "Yes"])

        st.subheader("Night Vision")
        night_vision = st.selectbox("Do you need camera with extra night vision capability?", ["No", "Yes"])
        
        
        
        
        
        
        submitted = st.form_submit_button("Get Recommendations")
# Right column for price information
with col2:
    # Set up price ranges based on user input
    price_ranges = {
        "Basic": (100, 200),
        "Sharp": (300, 500),
        "Very clear": (600, 1000)
    }
    
    # Get the price range based on user input
    min_price, max_price = price_ranges.get(resolution, (0, 0))

    # Display minimum and maximum price bars
    st.write("### Statistics")

    # Second bar (highlighted based on user input)
    #st.write(f"**Total matched CCTV**")
    st.metric(label="Total matched CCTV", value=f"20")
    st.progress((min_price / 1000))
    
    
    st.metric(label="Average Price", value=f"Rp.500000")

    


