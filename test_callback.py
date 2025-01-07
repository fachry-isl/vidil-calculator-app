import streamlit as st


def write():
    st.write("Hello")


with st.form("cctv_form"):
    weather = st.selectbox("Select the weather", ["Sunny", "Rainy", "Cloudy"], index=None)

    if weather is not None:
        st.sidebar.write("It is " + weather + " today")

    st.form_submit_button("Submit")
