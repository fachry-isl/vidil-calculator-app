import streamlit as st
import extra_streamlit_components as stx

st.code("import extra_streamlit_components as stx")
chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="tab1", title="✍️ Write!", description="Display stuff in the sidebar"),
    stx.TabBarItemData(id="tab2", title="💔 Nothing", description="Don't show anything")])

placeholder = st.sidebar.container() 

if chosen_id == "tab1":
    placeholder.markdown(f"## Welcome to `{chosen_id}`")
    placeholder.info(f"Since we are in {chosen_id}, let's add a bunch of widgets")
    placeholder.image("https://placekitten.com/g/400/200",caption=f"Meowhy from {chosen_id}")
    placeholder.slider("A slider",0,10,5,1)
    placeholder.checkbox("A checkbox",True)
    placeholder.button("A button")
    
    placeholder.metric("A metric", 123)

elif chosen_id == "tab2":
    #placeholder = st.sidebar.container()
    placeholder.write("TAB 2 STATE")

st.markdown("""
**** 
### Don't forget to `pip install extra_streamlit_components`
# """)