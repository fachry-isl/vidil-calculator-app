import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
    

# App Title
st.title("Test")



# Sidebar: Select Components
st.sidebar.header("Select Components")
include_additional_item = st.sidebar.checkbox("Additional Item", value=True)


costs = {}


if include_additional_item:
    st.subheader("Additional Item")
    # Create a session dictionary for custom item
    if 'custom_items' not in st.session_state:
        st.session_state['custom_items'] = []
        
    if 'item_id' not in st.session_state:
        st.session_state['item_id'] = 0  
        
    if ' additional_cost_total' not in st.session_state:
        st.session_state['additional_cost_total']  = 0
    
    item_name = st.text_input("Enter item name")
    item_price = st.number_input("Enter item price", min_value=0.0, step=0.1)
    item_quantity = st.number_input("Enter item quantity", min_value=1, step=1)

    # Add item to custom_items list when the button is clicked
    if st.button("Add Custom Item"):
        
        # Incremental item_id for each added item
        st.session_state['item_id'] += 1

        if item_name and item_price > 0 and item_quantity > 0:
            st.session_state.custom_items.append({"item_id": st.session_state['item_id'], "name": item_name, "price": item_price, "quantity": item_quantity, "total_price": item_price*item_quantity})
            st.success(f"Item '{item_name}' added successfully!")
        else:
            st.error("Please fill in all fields with valid data.")
    
        custom_items_df = pd.DataFrame(st.session_state.custom_items)
        st.write("Custom Items Added:")
        st.dataframe(custom_items_df)

        # Calculate total cost from custom items
        for item in st.session_state.custom_items:
            st.session_state['additional_cost_total'] += item["price"] * item["quantity"]
        st.write(f"Total cost for additional items: Rp.{st.session_state['additional_cost_total']:.0f}")

