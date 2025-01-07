import streamlit as st


def submit_form(cctv_model, nvr_model):
    # save data
    st.session_state.init_cctv = cctv_model 
    st.session_state.init_dvr = nvr_model
    
    # go to the next page
    #st.write(f"{st.session_state.init_cctv}, {st.session_state.init_dvr}")
    
    st.write("From Function Callback")
    st.write(f"{cctv_model}, {nvr_model}")
    
    st.write("From Session State") 
    st.write(f"{st.session_state.init_cctv}, {st.session_state.init_dvr}")
    
def first_page():
    st.title("Home page")
    
    # Initialize session state for variables if not already initialized
    if "init_cctv" not in st.session_state:
        st.session_state.init_cctv = "nothing"
    if "init_dvr" not in st.session_state:
        st.session_state.init_dvr = "nothing"
    
    
    with st.form("my_form"):
        cctv_model = st.text_input("Select CCTV")
        nvr_model = st.text_input("Select NVR")
        
        submitted = st.form_submit_button(label='Submit')
        
        if submitted:
            submit_form(cctv_model, nvr_model)
            
            st.switch_page("pages/page_1.py")

def second_page():
    st.title("Second Page")

pg = st.navigation([
    st.Page(first_page, title="Home Page", icon="🏠"),
    st.Page("./pages/page_1.py", title="Price Calculator", icon="🧮")
])
pg.run()