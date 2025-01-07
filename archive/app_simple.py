import streamlit as st

# App Title
st.title("CCTV Solution Cost Calculator")

# Dynamic Input Form
st.sidebar.header("Select Components")
include_cctv = st.sidebar.checkbox("CCTV", value=True)
include_nvr = st.sidebar.checkbox("NVR/DVR")
include_service = st.sidebar.checkbox("Managed Service")
include_maintenance = st.sidebar.checkbox("Maintenance")
include_additional = st.sidebar.checkbox("Additional Equipment")

# Initialize cost dictionary
costs = {}

# CCTV Section
if include_cctv:
    st.subheader("CCTV")
    cctv_quantity = st.number_input("Number of CCTVs", min_value=0, value=0, step=1)
    cctv_price = st.number_input("Price per CCTV", min_value=0.0, value=0.0)
    costs['CCTV'] = cctv_quantity * cctv_price

# NVR/DVR Section
if include_nvr:
    st.subheader("NVR/DVR")
    nvr_quantity = st.number_input("Number of NVR/DVRs", min_value=0, value=0, step=1)
    nvr_price = st.number_input("Price per NVR/DVR", min_value=0.0, value=0.0)
    costs['NVR/DVR'] = nvr_quantity * nvr_price

# Managed Service Section
if include_service:
    st.subheader("Managed Service")
    service_months = st.number_input("Number of Months", min_value=0, value=0, step=1)
    service_price = st.number_input("Monthly Service Cost", min_value=0.0, value=0.0)
    costs['Managed Service'] = service_months * service_price

# Maintenance Section
if include_maintenance:
    st.subheader("Maintenance")
    maintenance_cost = st.number_input("Maintenance Cost", min_value=0.0, value=0.0)
    costs['Maintenance'] = maintenance_cost

# Additional Equipment Section
if include_additional:
    st.subheader("Additional Equipment")
    additional_items = st.text_area("List of Additional Equipment (Comma-separated)", "")
    additional_cost = st.number_input("Cost of Additional Equipment", min_value=0.0, value=0.0)
    costs['Additional Equipment'] = additional_cost

# Calculate Total
total_cost = sum(costs.values())
st.markdown("---")
st.subheader(f"Total Cost: ${total_cost:,.2f}")

# Optional: Display Breakdown
if st.checkbox("Show Cost Breakdown"):
    st.write(costs)

# Export as Report
if st.button("Generate Report"):
    report = f"""
    CCTV Solution Cost Breakdown:
    {costs}

    Total Cost: ${total_cost:,.2f}
    """
    st.download_button("Download Report", report, "cost_report.txt")
