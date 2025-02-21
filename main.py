import streamlit as st

# Home page contain tutorial on how to use the website
def how_to_page():
    st.title("Flow Diagram")
    st.image("flowchart_app.jpg", use_container_width=True)

pg = st.navigation([
    st.Page("cctv_recommender.py", title="CCTV Recommender", icon="📷"),
    st.Page("calculator_page.py", title="Solution Calculator", icon="🧮")
])
pg.run()