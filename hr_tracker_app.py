import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

# Custom CSS for navy background, white text, spacing, dividing line, and header icon
st.markdown(
    """
    <style>
    /* Background & text color for entire app */
    .main {
        background-color: #1a2e4b;  /* Navy Blue */
        color: white;
        padding: 20px 40px;
        font-family: 'Arial', sans-serif;
    }
    
    /* Make all text white inside Streamlit components */
    .stText, .stMarkdown, .stMetric > div {
        color: white !important;
    }
    
    /* Add spacing between elements */
    .css-1d391kg, .css-1d391kg > div {  /* main container & inner divs */
        gap: 30px;
    }
    
    /* Style for your headers */
    h1, h2, h3, .css-1v0mbdj h1 {
        color: white;
    }

    /* Style for the dividing line between two columns */
    .divider {
        border-left: 2px solid #ffffff99; /* white with some transparency */
        height: 100%;
        margin: 0 15px;
    }
    
    /* Style for your metric boxes to stand out on navy */
    .metric-box {
        border-radius: 10px;
        padding: 15px;
        margin: 10px auto;
        width: 180px;
        font-family: Arial, sans-serif;
    }

    /* Override the Streamlit multiselect dropdown background to navy */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #001f4d;
        color: white;
    }

    /* HR Icon style */
    .header-icon {
        font-size: 30px;
        margin-right: 10px;
        vertical-align: middle;
    }
    </style>
    """, unsafe_allow_html=True
)


## Read Data & replace blanks with NA
df_permanent = pd.read_excel('Tracker.xlsx', sheet_name = 'Ramp_Perm')
df_permanent = df_permanent.fillna('NA')

df_temp = pd.read_excel('Tracker.xlsx', sheet_name = 'Ramp_Temp')
df_temp = df_temp.fillna('NA')

df_ppl = pd.read_excel('Tracker.xlsx', sheet_name = 'People_Supply')
df_ppl = df_ppl.fillna('NA')


## Combining Permanent & Temp Role Data
df_all = pd.concat([df_permanent, df_temp], ignore_index=True, sort=False)

### Normalized Roles -- Add more as needed
vehicle_technician = ['Maintenance Vehicle Technician', 'Vehicle Maintenance  Technician']


## Update all roles to Normalized Roles
df_all.loc[df_all['Normalized Role'].isin(vehicle_technician), 'Normalized Role'] = 'Vehicle Technician'


## Renaming columns Site and # of People
#df_all = df_all.rename(columns={'# People' : 'People', 'Activity Type' : 'Activity_Type_Permanent'})

## Streamlit App
st.markdown(
    """
    <h1>
      <span class="header-icon">👩‍💼</span> <!-- HR icon emoji -->
      Alstom Position Tracker
    </h1>
    """,
    unsafe_allow_html=True
)

## Drop Down User input
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div style='font-family: Arial, sans-serif; font-weight: 600; font-size: 16px; margin-bottom: 6px;'>Function</div>", unsafe_allow_html=True)
    function = sorted(set(df_all['Function'].tolist()))
    function.insert(0, "All")
    selected_functions = st.multiselect("", options=function, default=["All"])

with col2:
    st.markdown("<div style='font-family: Arial, sans-serif; font-weight: 600; font-size: 16px; margin-bottom: 6px;'>Normalized Role</div>", unsafe_allow_html=True)
    role = sorted(set(df_all['Normalized Role'].tolist()))
    role.insert(0, "All")
    selected_roles = st.multiselect("", options=role, default=["All"])

with col3:
    st.markdown("<div style='font-family: Arial, sans-serif; font-weight: 600; font-size: 16px; margin-bottom: 6px;'>Site</div>", unsafe_allow_html=True)
    site = sorted(set(df_all['Site'].tolist()))
    site.insert(0, "All")
    selected_sites = st.multiselect("", options=site, default=["All"])



## Apply Function filter Criteria
if "All" not in selected_functions:
    df_all = df_all[df_all['Function'].isin(selected_functions)]

# Apply Role filter
if "All" not in selected_roles:
    df_all = df_all[df_all['Normalized Role'].isin(selected_roles)]

# Apply Site filter
if "All" not in selected_sites:
    df_all = df_all[df_all['Site'].isin(selected_sites)]


# STEP 6: Split by Activity Type
ramp_down_df = df_all[df_all['Activity Type'] == "Ramp-Down"]
ramp_up_df = df_all[df_all['Activity Type'] == "Ramp-Up"]


## Metrics Required for Quick Info
total_ramp_up = df_all[df_all['Activity Type'] == 'Ramp-Up']['# People'].sum()
total_ramp_down = df_all[df_all['Activity Type'] == 'Ramp-Down']['# People'].sum()


white_collar_up_count = df_all[(df_all['WC/BC'] == 'WC') & (df_all['Activity Type'] == 'Ramp-Up')]['# People'].sum()
blue_collar_up_count = df_all[(df_all['WC/BC'] == 'BC') & (df_all['Activity Type'] == 'Ramp-Up')]['# People'].sum()


white_collar_down_count = df_all[(df_all['WC/BC'] == 'WC') & (df_all['Activity Type'] == 'Ramp-Down')]['# People'].sum()
blue_collar_down_count = df_all[(df_all['WC/BC'] == 'BC') & (df_all['Activity Type'] == 'Ramp-Down')]['# People'].sum()


# STEP 7: Show side-by-side
def boxed_metric(label, value, border_color="#4CAF50"):
    return f"""
    <div class="metric-box" style="
        border: 2px solid {border_color};
        display: flex;
        flex-direction: column;
        align-items: center;
        font-family: 'Arial', sans-serif;
    ">
        <div style="font-size: 16px; font-weight: 600; margin-bottom: 8px; color:white;">{label}</div>
        <div style="font-size: 36px; font-weight: 700; color: {border_color};">{value}</div>
    </div>
    """

#col1, col2 = st.columns([1.2, 1.2])
col1, divider_col, col2 = st.columns([1.2, 0.05, 1.2])

with col1:
    st.markdown("<h2 style='text-align: center;'>Ramp-Up Info</h2>", unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(boxed_metric("Total Ramp-Up Roles", int(total_ramp_up)), unsafe_allow_html=True)
    with m2:
        st.markdown(boxed_metric("Total White-Collar Roles", int(white_collar_up_count), border_color="#1E90FF"), unsafe_allow_html=True)
    with m3:
        st.markdown(boxed_metric("Total Blue-Collar Roles", int(blue_collar_up_count), border_color="#FF8C00"), unsafe_allow_html=True)

with divider_col:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # You can also keep this if you want to display the table:
    # st.write(ramp_up_df)

with col2:
    st.markdown("<h2 style='text-align: center;'>Ramp-Down Info</h2>", unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(boxed_metric("Total Ramp-Down Roles", int(total_ramp_down)), unsafe_allow_html=True)
    with m2:
        st.markdown(boxed_metric("Total White-Collar Roles", int(white_collar_down_count), border_color="#1E90FF"), unsafe_allow_html=True)
    with m3:
        st.markdown(boxed_metric("Total Blue-Collar Roles", int(blue_collar_down_count), border_color="#FF8C00"), unsafe_allow_html=True)
    

## People Availability List
# 1. Filter df_all to ramp-up activity
ramp_up_roles = df_all[df_all['Activity Type'] == 'Ramp-Up']

# 2. Apply your dropdown filters on ramp_up_roles
if "All" not in selected_functions:
    ramp_up_roles = ramp_up_roles[ramp_up_roles['Function'].isin(selected_functions)]

if "All" not in selected_sites:
    ramp_up_roles = ramp_up_roles[ramp_up_roles['Site'].isin(selected_sites)]

if "All" not in selected_roles:
    ramp_up_roles = ramp_up_roles[ramp_up_roles['Normalized Role'].isin(selected_roles)]

# 3. Get filtered roles list to use for filtering df_ppl
filtered_roles = ramp_up_roles['Normalized Role'].unique()

# 4. Now filter df_ppl where Normalized Role is in filtered_roles
filtered_employees = df_ppl[df_ppl['Normalized Role'].isin(filtered_roles)]

filtered_employees_merged = filtered_employees.merge(
    df_all[['Normalized Role', '# People', 'Site']],
    on='Normalized Role',
    how='left'
)

filtered_employees_merged = filtered_employees_merged.rename(columns={'# People' : 'People_Required', 'Site' : 'Site Required'})

st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
st.write("<div style='font-family: Arial, sans-serif; font-weight: 600; font-size: 16px; margin-bottom: 6px;'>Employees Availability Data</div>", unsafe_allow_html=True)
st.write(filtered_employees_merged)

