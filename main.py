import streamlit as st

import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import streamlit as st



# Load the configuration file
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

try:
    authenticator.login()
except Exception as e:
    st.error(f"An error occurred during authentication: {e}")
    st.write("Please check your credentials and try again.")
    
    
pg = st.navigation([
    st.Page("cctv_recommender.py", title="CCTV Recommender", icon="📷"),
    st.Page("calculator_page.py", title="Solution Calculator", icon="🧮"),
])

if st.session_state.get('authentication_status'):
    authenticator.logout()
    pg.run()
elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your username and password')



