import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt
import plotly.express as px
import re
from helper import cloud_plan, connectivity_plan, data_usage, color_discrete_map, appliance_managed_service, compression_hardware

st.set_page_config(layout="wide")

# Google Sheets API setup
def fetch_data_from_google_sheet(sheet_id, worksheet_name):
    """
    Fetch data from a specific worksheet of the Google Sheet.
    """
    # Create a connection object.
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Fetch data from the specified worksheet
    df = conn.read(spreadsheet_id=sheet_id, worksheet=worksheet_name)
    return pd.DataFrame(df)


# App Title
st.title("Video Intelligent Solution Calculator 📷")

# Google Sheets setup
SHEET_ID = "1wtbl4cC3Qc98FFM6KFjR1-k9fRQ7uC-Go4pKaancUAc"  # The Google Sheet ID
CCTV_WORKSHEET = "Camera and CCTV(App)"  # The worksheet name of CCTV data
DVR_NVR_WORKSHEET = "NVR/DVR(App)"  # The worksheet name of DVR/NVR data
INSTALLATION_WORKSHEET = "Installation(App)"  # The worksheet name of Installation data

# Load Data from Google Sheets
try:
    cctv_data = fetch_data_from_google_sheet(SHEET_ID, CCTV_WORKSHEET)
    dvr_nvr_data = fetch_data_from_google_sheet(SHEET_ID, DVR_NVR_WORKSHEET)
    installation_data = fetch_data_from_google_sheet(SHEET_ID, INSTALLATION_WORKSHEET)
except Exception as e:
    st.sidebar.error(f"Error loading data: {e}")
    cctv_data = pd.DataFrame()
    dvr_nvr_data = pd.DataFrame()
    installation_data = pd.DataFrame()
    
# Sidebar: Select Components
st.sidebar.header("Configuration Form")
st.sidebar.write("(Select Parameter to Include)")
include_cctv = st.sidebar.checkbox("CCTV", value=True)
include_dvr_nvr = st.sidebar.checkbox("DVR/NVR", value=True)
include_installation = st.sidebar.checkbox("Installation", value=True)
include_platform = st.sidebar.checkbox("Platform", value=False)
include_license = st.sidebar.checkbox("License", value=False)
include_cloud = st.sidebar.checkbox("Cloud", value=False)
include_connectivity = st.sidebar.checkbox("Connectivity", value=False, key="connectivity")
include_managed_service = st.sidebar.checkbox("Managed Service", value=False)

# Two-column layout
col1, col2 = st.columns([2, 1])

# Costs dictionary to hold calculated costs
unit_price = {}
costs = {}
export_select_data = {}
connectivity = {}
# Connectivity Plan
cctv_resolution = 0
# Compatibility flags
cctv_signal_type = None
cctv_quantity = 0
cctv_connectivity = ""
dvr_nvr_channel = 0
dvr_or_nvr = ""
recurring_flag = False


# Form
with col1:
    # CCTV Section
    if include_cctv and not cctv_data.empty:
        st.subheader("CCTV")
        #cctv_options = cctv_data["Model"].tolist()  # Adjust column name
        cctv_custom_name = cctv_data["Brand"] + " - " + cctv_data["Model"] + " - " + cctv_data["Resolution*"] + " - " + cctv_data["Signal Type"] + cctv_data["Industrial Grade*"].apply(lambda x: " - Industrial" if isinstance(x, str) and x.lower() == 'yes' else "")
        selected_cctv = st.selectbox("Select a CCTV Device", options= cctv_custom_name, index=None)
        if selected_cctv:
            cctv_model_selected = selected_cctv.split(" - ")[1]
            cctv_details = cctv_data[cctv_data["Model"] == cctv_model_selected].iloc[0]
            cctv_price = cctv_details["Price"]  # Adjust column name
            cctv_signal_type = cctv_details["Signal Type"]
            cctv_connectivity = cctv_details["Connectivity"]
            st.write(f"Unit Price: Rp.{cctv_price:,.0f}")
            cctv_quantity = st.number_input("Number of CCTVs", min_value=1, value=1, step=1) 
            unit_price[f'{cctv_model_selected}'] = cctv_price
            
            # Handle Cost
            costs[f'CCTV - {cctv_model_selected}x({cctv_quantity})'] = cctv_quantity * cctv_price
            
            # Handle Data Export
            export_select_data["CCTV"] = f"CCTV;{cctv_details['Brand']} - {cctv_model_selected} - {cctv_details['Resolution*']};One Time;{cctv_quantity};{int(cctv_price)};{int(cctv_price * cctv_quantity)}"

            # Handle Connectivity Plan Data
            cctv_resolution = cctv_details['Resolution*']                
    # DVR/NVR Section
    if include_dvr_nvr and not dvr_nvr_data.empty:
        st.subheader("DVR/NVR")
        #dvr_nvr_options = dvr_nvr_data["Model"].tolist()
        if cctv_signal_type == "Digital":
            st.info(f"Your selecting CCTV with {cctv_signal_type} signal type We recommend using NVR!", icon='🤖')
        elif cctv_signal_type == "Analog":
            st.info(f"Your selecting CCTV with {cctv_signal_type} signal type We recommend using DVR!", icon='🤖')
        dvr_nvr_custom_name = dvr_nvr_data["Brand"] + " - " + dvr_nvr_data["Device"] + " - " + dvr_nvr_data["Model"] + " - " + dvr_nvr_data["Channel"].apply(lambda x: f"{x:,.0f}") + " Channels"
        selected_dvr_nvr = st.selectbox("Select a DVR/NVR Device", options= dvr_nvr_custom_name, index=None)
        if selected_dvr_nvr:
            selected_dvr_nvr = selected_dvr_nvr.split(" - ")[2]
            dvr_nvr_details = dvr_nvr_data[dvr_nvr_data["Model"] == selected_dvr_nvr].iloc[0]
            dvr_nvr_price = dvr_nvr_details["Price"]
            dvr_or_nvr =  dvr_nvr_details["Device"]
            dvr_nvr_channel = dvr_nvr_details["Channel"]
            dvr_nvr_quantity = st.number_input("Number of DVR/NVR Units", min_value=1, value=1, step=1)
            unit_price[f'{selected_dvr_nvr}'] = dvr_nvr_price
            costs[f'DVR/NVR - {selected_dvr_nvr}x({dvr_nvr_quantity})'] = dvr_nvr_quantity * dvr_nvr_price
            export_select_data["DVR/NVR"] = f"{dvr_or_nvr};{dvr_nvr_details['Brand']} - {dvr_or_nvr} - {selected_dvr_nvr} - {dvr_nvr_channel:,.0f} Channels;One Time;{dvr_nvr_quantity};{int(dvr_nvr_price)};{int(dvr_nvr_price * dvr_nvr_quantity)}"
    # Installation Section
    if include_installation and not installation_data.empty:
        st.subheader("Installation")
        installation_options = installation_data["Installation Package"].tolist()
        
        if cctv_resolution == "1MP":
            st.info("For 1MP CCTV, we recommend using Standard Installation Package", icon='🤖')
        else:
            st.info("You're selecting CCTV with resolution higher than 1MP, we recommend using Full HD Installation Package", icon='🤖')
        
        selected_installation = st.selectbox("Select Installation Type", options=installation_options, index=None)
       
      
        if selected_installation:
            number_area = st.number_input("Number of Point", min_value=1, step=1)
            installation_details = installation_data[installation_data["Installation Package"] == selected_installation].iloc[0]
            install_complexity_map = {
                0:f"Basic {installation_details['Price Lower']:,.0f}",
                1:f"Intermediate {installation_details['Price Middle']:,.0f}",
                2:f"Advanced {installation_details['Price Upper']:,.0f}"
            }

            installation_complexity = st.select_slider("Select Installation Complexity (Affects Price per Point)", 
                options=[f"Basic {installation_details['Price Lower']:,.0f}", 
                         f"Intermediate {installation_details['Price Middle']:,.0f}", 
                         f"Advanced {installation_details['Price Upper']:,.0f}"])
            
            if installation_complexity == install_complexity_map[0]:
                installation_cost = installation_details["Price Lower"]
            elif installation_complexity == install_complexity_map[1]:
                installation_cost = installation_details["Price Middle"]
            elif installation_complexity == install_complexity_map[2]:
                installation_cost = installation_details["Price Upper"]
                
            unit_price[f'I{selected_installation}'] = installation_cost
            costs[f'Installation - {selected_installation}x({number_area})'] = installation_cost * number_area
            
            export_select_data["Installation"] = f"Installation;{selected_installation};One Time;{number_area};{int(installation_cost)};{int(number_area * installation_cost)}"
    # Platform Section - Recurring
    if include_platform and not installation_data.empty:
        st.subheader("Platform")
        de_quantity = st.number_input("Number of Data Engineer", min_value=1, step=1, value=None)
        ds_quantity = st.number_input("Number of Data Science", min_value=1, step=1, value=None)
        pm_quantity = st.number_input("Number of Project Manager", min_value=1, step=1, value=None)
        mle_quantity = st.number_input("Number of Machine Learning Engineer", min_value=1, step=1, value=None)
        st.divider()
        platform_duration_year = st.number_input("Input Number of Year", min_value=1, value=1, step=1)
        
        if de_quantity != None:
            costs[f'Platform - Data Engineer ({de_quantity}) - {platform_duration_year} year'] = 2000_000*de_quantity*(platform_duration_year*12)
            # Export DE
            export_select_data["Platform-1"] = f"Platform;Data Engineer ({de_quantity}) - {platform_duration_year} Year;Recurring;{platform_duration_year};{2000_000};{2000_000*de_quantity*(platform_duration_year*12)};"
            recurring_flag = True
        if ds_quantity != None:
            costs[f'Platform - Data Science ({ds_quantity}) - {platform_duration_year} year'] = 2000_000*ds_quantity*(platform_duration_year*12)
            # Export DS
            export_select_data["Platform-2"] = f"Platform;Data Science ({ds_quantity}) - {platform_duration_year} Year;Recurring;{platform_duration_year};{2000_000};{2000_000*ds_quantity*(platform_duration_year*12)};"
            recurring_flag = True
        if pm_quantity != None:
            costs[f'Platform - Project Manager ({pm_quantity}) - {platform_duration_year} year'] = 2000_000*pm_quantity*(platform_duration_year*12)
             # Export PM
            export_select_data["Platform-3"] = f"Platform;Project Manager ({pm_quantity}) - {platform_duration_year} Year;Recurring;{platform_duration_year};{2000_000};{2000_000*pm_quantity*(platform_duration_year*12)};"
            recurring_flag = True
        if mle_quantity != None:
            costs[f'Platform - ML Engineer ({mle_quantity}) - {platform_duration_year} year'] = 2000_000*mle_quantity*(platform_duration_year*12)
            # Export MLE
            export_select_data["Platform-4"] = f"Platform;Machine Learning Engineer ({mle_quantity}) - {platform_duration_year} Year;Recurring;{platform_duration_year};{2000_000};{2000_000*mle_quantity*(platform_duration_year*12)}"
            recurring_flag = True      
    # License Section
    if include_license and not installation_data.empty:
        st.subheader("License")
        license_package = st.selectbox("Select License Package", options=["Smart Dashboard for Video Intelligence License"], index=None)
        if license_package != None:
            costs[f'License - Smart Dashboard License'] = 72_900_000 
            export_select_data["License"] = f"License;{license_package};One Time;1;72900000;72900000"
    # Cloud Section - Recurring
    if include_cloud and not installation_data.empty:
        st.subheader("Cloud")
        cloud_package = st.selectbox("Select Cloud Plan", options=list(cloud_plan.keys()), index=None)
        cloud_quantity = st.number_input("Input Number of Year (Cloud)", min_value=1, value=1, step=1)
        if cloud_package != None:
            recurring_flag = True
            costs[f'Cloud - {cloud_package} ({cloud_quantity} Year)'] = cloud_plan[cloud_package] * (12*cloud_quantity)
            export_select_data["Cloud"] = f"Cloud;{cloud_package};Recurring;{cloud_quantity};{cloud_plan[cloud_package]};{cloud_plan[cloud_package] * (12*cloud_quantity)}"

        
        st.write("Note: Include Maintenance & Warranty Services")
    # Connectivity Section - Recurring
    if include_connectivity and not installation_data.empty:
        st.subheader("Connectivity")
        if cctv_resolution != 0:
            st.info(f"Assuming CCTV streamed 24/7 based on your CCTV resolution {cctv_resolution} the CCTV would consume {data_usage[cctv_resolution]['monthly']} GB per Month.", icon='🤖')
        connectivity_package = st.selectbox("Select Connectivity Plan", list(connectivity_plan.keys()), index=None)
        connectivity_quantity = st.number_input("Input Number of Year (Quota)", min_value=1, value=1, step=1)
        if connectivity_package != None:
            costs[f'Connectivity - Telkomsel Quota - {connectivity_package} - {cctv_quantity} Device - ({connectivity_quantity} Year)'] = (connectivity_plan[connectivity_package]*cctv_quantity) * (12*connectivity_quantity)
            export_select_data["Connectivity"] = f"Connectivity;Telkomsel Quota - {connectivity_package} {cctv_quantity} Device - {connectivity_quantity} Year;Recurring;{connectivity_quantity};{connectivity_plan[connectivity_package]};{(connectivity_plan[connectivity_package]*cctv_quantity) * (12*connectivity_quantity)}"
            recurring_flag = True
        
        st.info(f"Would you like to use Compression Based Solution? This would reduce data usage by up to 40% which become {data_usage[cctv_resolution]['monthly'] * 0.4:0.0f} GB per Month.", icon='🤖')
        include_compression = st.checkbox("Use Compression Solution", value=False)
        if include_compression:
            st.markdown("#### Compression")
            if cctv_quantity <= 4 and cctv_quantity != 0:
                st.info("For 4 CCTV Devices or less, we recommend using Jetson Orin Nano 8 GB", icon='🤖')
            elif cctv_quantity <= 8 and cctv_quantity != 0:
                st.info("For 8 CCTV Devices or less, we recommend using Jetson AGX Orin 32 GB", icon='🤖')
            elif cctv_quantity > 8 and cctv_quantity != 0:
                st.info("For More than 8 CCTV Devices, we recommend using Jetson AGX Orin 64 GB", icon='🤖')
            compression_device = st.selectbox("Select Compression Device", options=compression_hardware.keys(), index=None)
            
            if compression_device != None:
                costs[f'Compression - {compression_device}'] = compression_hardware[compression_device]
                export_select_data["Compression"] = f"Compression;{compression_device};One Time;1;{compression_hardware[compression_device]};{compression_hardware[compression_device]}"
    # Managed Service Section - Recurring
    if include_managed_service and not installation_data.empty:
        st.subheader("Managed Service")
        managed_service = st.selectbox("Select Managed Service", options=list(appliance_managed_service.keys()), index=None)
        managed_service_duration = st.number_input("Input Number of Year (Managed Service)", min_value=1, value=1, step=1)
        #st.write(appliance_managed_service[managed_service])
        if managed_service != None:
            costs[f'Managed Service - {managed_service} ({managed_service_duration} Year)'] = appliance_managed_service[managed_service] * managed_service_duration
            export_select_data["Managed Service"] = f"Managed Service;{managed_service};Recurring;{managed_service_duration};{appliance_managed_service[managed_service]};{appliance_managed_service[managed_service] * managed_service_duration}"
            recurring_flag = True

# Price Breakdown
with col2:
    st.subheader("Price Breakdown")
    with st.container(border=True):
        if costs:
            platform_count = 0
            for item, cost in costs.items():
                #st.write(f"{item}: Rp.{cost:,.0f}")
                if item.startswith("CCTV"):
                    st.markdown(f"""
                                ##### CCTV
                                {item.replace('CCTV - ', '', 1)}: Rp.{cost:,.0f}
                                """)
                elif item.startswith("DVR/NVR"):
                    st.markdown("##### DVR/NVR")
                    st.write(f"{item.replace('DVR/NVR - ', '', 1)}: Rp.{cost:,.0f}")
                elif item.startswith("Installation"):
                    st.markdown("##### Installation")
                    st.write(f"{item.replace('Installation - ', '', 1)}: Rp.{cost:,.0f}")
                elif item.startswith("Platform"):
                    if platform_count == 0:
                        st.markdown("##### Platform")
                        platform_count += 1
                    st.write(f"{item.replace('Platform - ', '', 1)}: Rp.{cost:,.0f}")
                elif item.startswith("License"):
                    st.markdown("##### License")
                    st.write(f"{item.replace('License - ', '', 1)}: Rp.{cost:,.0f}")
                elif item.startswith("Cloud"):
                    st.markdown("##### Cloud")
                    st.write(f"{item.replace('Cloud - ', '', 1)}: Rp.{cost:,.0f}")
                elif item.startswith("Connectivity"):
                    st.markdown("##### Connectivity")
                    st.write(f"{item.replace('Connectivity - ', '', 1)}: Rp.{cost:,.0f}")
                elif item.startswith("Managed Service"):
                    st.markdown("##### Managed Service")
                    st.write(f"{item.replace('Managed Service - ', '', 1)}: Rp.{cost:,.0f}")
                elif item.startswith("Compression"):
                    st.markdown("##### Compression")
                    st.write(f"{item.replace('Compression - ', '', 1)}: Rp.{cost:,.0f}")
            st.divider()        
            total_cost = sum(costs.values()) + st.session_state.get('additional_cost_total', 0)
            
            st.metric(label="Estimated Total Cost", value=f"Rp.{total_cost:,.0f}")
            
            with st.expander("See Margin Calculation"):
                st.write(f"Margin +10% : Rp.{total_cost*1.10:,.0f}")
                st.write(f"Margin +15% : Rp.{total_cost*1.15:,.0f}")
                st.write(f"Margin +20% : Rp.{total_cost*1.20:,.0f}")
                st.write(f"Margin +25% : Rp.{total_cost*1.25:,.0f}")
                st.write(f"Margin +30% : Rp.{total_cost*1.3:,.0f}")
                st.write(f"Margin +35% : Rp.{total_cost*1.35:,.0f}")

            with st.expander("See Cost Distribution"):
                cost_dist_dict = {
                    "CCTV": 0,
                    "NVR/DVR": 0,
                    "Installation": 0,
                    "Platform": 0,
                    "License": 0,
                    "Cloud": 0,
                    "Connectivity": 0,
                    "Managed Service": 0
                }
                
                # st.write(costs.split("-"))
                
                for key, value in costs.items():
                    item = key.split("-")
                    #st.write(item)
                    
                    if item[0].strip() == "CCTV":
                        cost_dist_dict["CCTV"] += value
                    elif item[0].strip() == "DVR/NVR":
                        cost_dist_dict["NVR/DVR"] += value
                    elif item[0].strip() == "Installation":
                        cost_dist_dict["Installation"] += value
                    elif item[0].strip() == "Platform":
                        cost_dist_dict["Platform"] += value
                    elif item[0].strip() == "License":
                        cost_dist_dict["License"] += value
                    elif item[0].strip() == "Cloud":
                        cost_dist_dict["Cloud"] += value
                    elif item[0].strip() == "Connectivity":
                        cost_dist_dict["Connectivity"] += value
                    elif item[0].strip() == "Managed Service":
                        cost_dist_dict["Managed Service"] += value
                        
                
                #st.write(cost_dist_dict)
                
                
                     
                cost_data = pd.DataFrame({
                "Category": [cost for cost in cost_dist_dict.keys()],
                "Cost": [cost for cost in cost_dist_dict.values()]
                })
                  
                fig = px.pie(cost_data, names="Category", values="Cost", color="Category", color_discrete_map=color_discrete_map)
                st.plotly_chart(fig)
            
    st.subheader("Compatibility")
    
    # 1. Make sure CCTV matches with DVR/NVR signal type
    if cctv_signal_type == "Digital":
        if dvr_or_nvr == "DVR":
            st.warning("1. CCTV and NVR is not compatible ❌")
        elif dvr_or_nvr == "NVR":
            st.success("1. CCTV and NVR is compatible ✅")
        else:
            st.warning("1. Digital CCTV requires NVR")
    elif cctv_signal_type == "Analog":
        st.warning("1. Analog CCTV requires DVR")
        if dvr_or_nvr == "DVR":
            st.success("1. CCTV and NVR is compatible ✅")
        elif dvr_or_nvr == "NVR":
            st.warning("1. CCTV and NVR is not compatible ❌")
        else:
            st.warning("1. Digital CCTV requires NVR")
    # 2. Make sure the number of CCTV matches with the number of DVR/NVR channels
    if cctv_quantity > dvr_nvr_channel:
        st.error("2. Number of CCTV devices exceed the number of DVR/NVR channels. Please reduce the number of CCTV devices or select other DVR/NVR model. ❌")
    elif cctv_quantity <= dvr_nvr_channel:
        if cctv_quantity != 0:
            st.success("2. Number of CCTV devices are less than the number of DVR/NVR channels. ✅")

df_export = pd.DataFrame()
df_export_1year = pd.DataFrame()
df_export_3year = pd.DataFrame()
df_export_2year = pd.DataFrame()

def calculate_cost_margin_yearly(num_year, df):
    for _, value in export_select_data.items():
        item = value.split(";")
        
        total_price = 0
        # Get number of Data Engineer (5) - 1 Year -> 5
        if item[0] == "CCTV":
            total_price = float(item[4])*cctv_quantity
        elif item[0] == "DVR" or  item[0] == "NVR":
            total_price = float(item[4])*dvr_nvr_quantity
        elif item[0] == "Installation":
            total_price = float(item[4])*int(item[3])
        elif item[0] == "Platform":
           model =  item[1]   
           match = re.search(r'\((\d+)\)', model)
           if match:
                number_people = int(match.group(1))
                total_price = float(item[4])*number_people*(12*num_year)  # Convert to float if needed for arithmetic operations
        elif item[0] == "Connectivity":
            total_price = float(item[4])*cctv_quantity*(12*num_year)
        elif item[0] == "Cloud":
            total_price = float(item[4])*(12*num_year)
        else:
            total_price = float(item[4])
        
        if item[2] == "Recurring":
            # Organize Export Item into a DataFrame
            df_export_row = pd.DataFrame([{
                'Item': item[0],
                'Model/Package': item[1],
                'Term': item[2],
                'Qty': num_year,  
                'Total Price': total_price*num_year,
                'Margin +5%': total_price * 1.05,
                'Margin +10%': total_price * 1.1,
                'Margin +15%': total_price * 1.15,
                'Margin +20%': total_price * 1.2,
                'Margin +25%': total_price * 1.25,
                'Margin +30%': total_price * 1.3,
                'Margin +35%': total_price * 1.35
            }])

            # Merge to df_export
            df = pd.concat([df, df_export_row], axis=0, ignore_index=True)
        else: 
            # Organize Export Item into a DataFrame
            df_export_row = pd.DataFrame([{
                'Item': item[0],
                'Model/Package': item[1],
                'Term': item[2],
                'Qty': int(item[3]),  # Convert quantity to integer
                'Total Price': total_price,
                'Margin +5%': total_price * 1.05,
                'Margin +10%': total_price * 1.1,
                'Margin +15%': total_price * 1.15,
                'Margin +20%': total_price * 1.2,
                'Margin +25%': total_price * 1.25,
                'Margin +30%': total_price * 1.3,
                'Margin +35%': total_price * 1.35
            }])
            # Merge to df_export
            df = pd.concat([df, df_export_row], axis=0, ignore_index=True)
            
    return df


st.divider()

st.header("Detailed Cost Breakdown")

# Display the detailed cost breakdown
def generate_kpi(df_kpi, year):
    total_price_kpi = df_kpi['Total Price'].sum()
    
    # Display KPIs horizontally
    kpi_columns = st.columns(4)
    kpi_columns[0].metric(label="Cost Price", value=f"{total_price_kpi:,.0f}")
    kpi_columns[1].metric(label="Margin +25%", value=f"{total_price_kpi*1.25:,.0f}")
    kpi_columns[2].metric(label="Margin +30%", value=f"{total_price_kpi*1.30:,.0f}")
    kpi_columns[3].metric(label="Margin +35%", value=f"{total_price_kpi*1.35:,.0f}")

def generate_bar_proportion(df_bar_proportion):
    # Group by 'Item' and calculate the total price for each item
    df_grouped = df_bar_proportion.groupby('Item', as_index=False).sum()
    # Calculate the percentage for each item
    df_grouped['Percentage'] = (df_grouped['Total Price'] / df_grouped['Total Price'].sum()) * 100
    # Sort the DataFrame by 'Total Price' in descending order
    df_grouped = df_grouped.sort_values(by='Total Price', ascending=True)
    
    df_grouped[" "] = " "
    fig = px.bar(df_grouped, 
                   x="Total Price", 
                   y=" ", orientation='h', 
                   color='Item',
                   text=df_grouped['Percentage'].apply(lambda x: f'{x:.2f}%'),
                   color_discrete_map=color_discrete_map)
    
    # Update the layout to show the text inside the bars and set the height
    fig.update_traces(textposition='inside')
    fig.update_layout(
        height=200,  # Set the height of the plot
        legend=dict(
            title_text="",  # Set the title of the legend
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
    
     # Disable the y-axis label and title
    fig.update_yaxes(showticklabels=False, title='')
    fig.update_xaxes(showticklabels=False, title='')

    return fig

if cctv_quantity != 0 and recurring_flag == True:
    with st.container(border=True):
        df_export_1year = calculate_cost_margin_yearly(1, df_export_1year)
        st.subheader(f"1 Year Cost and Margin Calculation")
        st.plotly_chart(generate_bar_proportion(df_export_1year))
        generate_kpi(df_export_1year, 1)
        st.dataframe(df_export_1year, use_container_width=True, height=422)

    with st.container(border=True):
        df_export_2year = calculate_cost_margin_yearly(2, df_export_2year)
        st.subheader(f"2 Year Cost and Margin Calculation")
        generate_kpi(df_export_2year, 2)
        st.plotly_chart(generate_bar_proportion(df_export_2year))
        st.dataframe(df_export_2year, use_container_width=True, height=422)

    with st.container(border=True):
        df_export_3year = calculate_cost_margin_yearly(3, df_export_3year)
        st.subheader(f"3 Year Cost and Margin Calculation")
        generate_kpi(df_export_3year, 3)
        st.plotly_chart(generate_bar_proportion(df_export_3year))
        st.dataframe(df_export_3year, use_container_width=True, height=422)


