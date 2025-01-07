import streamlit as st

# Home page contain tutorial on how to use the website
def how_to_page():
    st.title("Flow Diagram")
    st.image("flowchart_app.jpg", use_container_width=True)

pg = st.navigation([
    st.Page(how_to_page, title="How To Use", icon="💡"),
    st.Page("cctv_finder_page.py", title="1. Find your CCTV", icon="📷"),
    st.Page("calc_page.py", title="2. Solution Calculator", icon="🧮")
])
pg.run()