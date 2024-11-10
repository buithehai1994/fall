import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load and preprocess data
def load_data(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Rename columns for easier understanding
    df = df.rename(columns={
        'MeasureValueNumber': 'Number of Cases',
        'ReportingCategory2': 'Injury Type'
    })
    
    # Filter and clean the H1 data
    h1 = df[df['TableReference'] == 'H1']
    h1 = h1.rename(columns={'ReportingCategory4': 'Age Group'})
    h1 = h1[h1['Age Group'] != 'All ages']
    h1 = h1[h1['Injury Type'] != 'All external causes']

    # Filter and clean the D2 data
    d2 = df[df['TableReference'] == 'D2']
    d2 = d2[d2['Injury Type'] != 'All external causes']
    
    return h1, d2

# Path to the Excel file 
file_path = 'AIHW_INJCAT213_Machine_readable_21062024.xlsx'

# Streamlit sidebar UI components
st.sidebar.title("Navigation")

# Tab selection in the sidebar
tab = st.sidebar.radio("Select a Tab", [
    "Intro", 
    "Total Injuries by Type (Bar Chart)", 
    "Total Injuries by Type (Pie Chart)", 
    "Interactive Stacked Bar Chart by Age Group",
    "Percentage of Injury Cases by Age Group",
    "Annual Injury Cases by Year",
    "Insights",
    "References"
])

# Display the title and description
st.title("Injury Data Visualizer")

# Load the data
h1, d2 = load_data(file_path)

# Display content based on selected tab
if tab == "Intro":
    st.subheader("Introduction")
    st.markdown("""
        Welcome to the **Injury Data Visualizer**! This app helps you explore and understand injury data 
        provided by the AIHW (Australian Institute of Health and Welfare). It provides insights into 
        different types of injuries and trends across various age groups. You can use this tool to:
        
        1. **Explore the total number of injuries** by type through bar and pie charts.
        2. **Visualize injury cases by age group and type** using interactive stacked bar charts.
        3. **Understand trends** like which injury types are more prevalent in certain age groups.
        4. **Explore injury cases annually** through visualizations that break down the data by year.

        ### Features:
        - **Interactive Charts**: Explore data visually with interactive charts powered by Plotly.
        - **Insights**: Learn about the most common injuries and how they vary with age.
        
        Please use the navigation options on the sidebar to explore the different visualizations and insights.
        
        Note: Data is collected between 1 July 2022 to 30 June 2023
    """)

elif tab == "Total Injuries by Type (Bar Chart)":
    st.subheader("Total Number of Injuries by Type (Bar Chart)")
    grouped_by_type = h1.groupby('Injury Type', as_index=False)['Number of Cases'].sum()
    fig_bar = px.bar(
        grouped_by_type,
        x='Injury Type',
        y='Number of Cases',
        title="Total Number of Injuries by Type"
    )
    st.plotly_chart(fig_bar)

elif tab == "Total Injuries by Type (Pie Chart)":
    st.subheader("Total Number of Injuries by Type (Pie Chart)")
    grouped_by_type = h1.groupby('Injury Type', as_index=False)['Number of Cases'].sum()
    fig_pie = px.pie(
        grouped_by_type,
        names='Injury Type',
        values='Number of Cases',
        title="Total Number of Injuries by Type"
    )
    st.plotly_chart(fig_pie)

elif tab == "Interactive Stacked Bar Chart by Age Group":
    st.subheader("Interactive Stacked Bar Chart of Injury Cases by Age Group and Type")
    fig_stack = px.bar(
        h1,
        x='Age Group',
        y='Number of Cases',
        color='Injury Type',
        title="Interactive Stacked Bar Chart of Injury Cases by Age Group and Type"
    )
    fig_stack.update_layout(barmode='stack', xaxis={'categoryorder': 'category ascending'})
    st.plotly_chart(fig_stack)

elif tab == "Percentage of Injury Cases by Age Group":
    st.subheader("Percentage of Injury Cases by Age Group and Type (Stacked Bar Chart)")
    grouped = h1.groupby(['Age Group', 'Injury Type'], as_index=False)['Number of Cases'].sum()
    age_group_totals = grouped.groupby('Age Group')['Number of Cases'].transform('sum')
    grouped['Percentage'] = (grouped['Number of Cases'] / age_group_totals) * 100
    fig_percentage = px.bar(
        grouped,
        x='Age Group',
        y='Percentage',
        color='Injury Type',
        title="Percentage of Injury Cases by Age Group and Type"
    )
    fig_percentage.update_layout(barmode='stack', xaxis={'categoryorder': 'category ascending'})
    st.plotly_chart(fig_percentage)

elif tab == "Annual Injury Cases by Year":
    st.subheader("Annual Number of Injury Cases by Type (Bar Chart for D2 data)")
    d2_aggregated = d2.groupby(['ReportingCategory4', 'Injury Type'], as_index=False).agg({'Number of Cases': 'sum'})
    d2_aggregated = d2_aggregated.rename(columns={'ReportingCategory4': 'Year'})
    fig_d2 = px.bar(
        d2_aggregated,
        x='Year',
        y='Number of Cases',
        color='Injury Type',
        title="Annual Number of Injury Cases by Type (per 100,000 Population)"
    )
    fig_d2.update_layout(barmode='group')
    st.plotly_chart(fig_d2)

elif tab == "Insights":
    st.subheader("Injury Data Insights")
    st.markdown("""
        Based on the data visualized above, the following insights can be observed:
        
        1. **Falls are the most common type of injury** across all age groups. This is the leading cause of injury, as seen in both the bar and pie charts of injury types.
        
        2. **The frequency of fall-related injuries increases with age**. The interactive stacked bar chart and the percentage breakdown by age group reveal a significant rise in fall injuries among older age groups, particularly in people over 65 years of age.
        
        3. **Age Groups and Their Vulnerability**: Older adults (65+) tend to experience a higher proportion of fall-related injuries compared to younger groups. This trend is consistent across multiple visualizations, indicating a potential area for targeted injury prevention strategies.
        
        ### Recommendations:
        - Public health initiatives should focus on **preventing falls among the elderly**.
        - More resources can be dedicated to improving **safety in environments** where older adults spend time (e.g., homes, healthcare facilities).
    """)

elif tab == "References":
    st.subheader("Data Source References")
    st.markdown("""
        The data used in this application is sourced from the Australian Institute of Health and Welfare (AIHW). 
        You can access the full dataset and report at the following link:
        
        [AIHW - Injury in Australia](https://www.aihw.gov.au/reports/injury/injury-in-australia/data)
        
        This dataset provides comprehensive information about injuries in Australia, including data about injury types, 
        demographics, and geographical distribution.
        
        Please visit the above link for more detailed information and additional context regarding the data used in this application.
    """)
