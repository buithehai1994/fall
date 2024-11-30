import streamlit as st
import streamlit.components.v1 as components

# Set page configuration (must be the first Streamlit command)
st.set_page_config(page_title="Population Presentation", layout="wide")

# Inject custom CSS for responsive layout and better positioning
st.markdown(
    """
    <style>
        /* Customizing the progress bar */
        .progress-bar {
            width: 100%;
            height: 20px;
            background-color: #f0f0f0;
            border-radius: 10px;
            margin-top: 5px;
        }

        .progress-bar-fill {
            height: 100%;
            background-color: #4caf50;
            border-radius: 10px;
            transition: width 0.3s ease;
        }

        /* Styling the slide titles */
        h1 {
            font-size: 2.5em;
            font-weight: bold;
            color: #333;
            text-align: center;
            margin-top: 0; /* Reduced margin to avoid extra space */
        }

        h3 {
            font-size: 1.5em;
            color: #555;
            text-align: center;
            margin-top: -5px; /* Reduced margin to pull slide info closer */
        }

        /* Navigation button styling */
        .stButton button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
        }

        .stButton button:disabled {
            background-color: #ccc;
        }

        /* Sidebar styles */
        .css-1d391kg {
            background-color: #f4f4f4;
        }

        .css-ffhzg2 {
            font-size: 18px;
        }

        /* Customize the dropdown in the sidebar */
        .stSelectbox select {
            font-size: 16px;
            background-color: #fafafa;
        }

        .stSelectbox label {
            font-size: 18px;
        }

        /* Customize the layout of the iframe (graph space) */
        iframe {
            width: 100% !important;
            height: 600px; /* Reduced height for more space at the bottom */
            border: none;
            margin-top: 10px; /* Reduced space above the graph */
        }

        /* Make the sidebar slightly smaller to save space */
        .css-1d391kg {
            width: 250px;
        }

        .css-ffhzg2 {
            padding-top: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Updated list of HTML file paths without the Crude Rate Explanation slide
html_files = [
    "html/injures_by_type_bar_chart.html",
    "html/injures_by_type_pie_chart.html",
    "html/annual_number_of_injury_cases_by_type.html",
    "html/Age_Standardised_rate_of_death_Injury.html",
    "html/injures_by_age_causes_stacked_bar_chart.html",
    "html/injures_by_age_causes_stacked_bar_percentage.html",
    "html/population_by_age_group_and_sex_dashboard.html",
    "html/population_by_year_dashboard.html",
    "html/predicted_total_pop_by_area.html",
    "html/crude_rate_explanation.html",
    # Removed the Crude Rate Explanation slide
    "html/predicted_injures_by_age_causes_stacked_bar_chart.html",
    "html/predicted_injures_by_age_causes_stacked_bar_chart_percentage.html",
]

# Updated slide titles list without the Crude Rate Explanation slide
slide_titles = [
    "Injuries by Type (Bar Chart)",
    "Injuries by Type (Pie Chart)",
    "Annual Number of Injury Cases by Type",
    "Age Standardised Rate of Death (Injury)",
    "Injuries by Age Causes (Stacked Bar Chart)",
    "Injuries by Age Causes (Stacked Bar Chart Percentage)",
    "Population by Age Group and Gender",
    "Population by Year",
    "Predicted Total Population by Area",
    "Crude rate",
    # Updated titles list without the Crude Rate Explanation
    "Predicted Injuries by Age Causes (Stacked Bar Chart)",
    "Predicted Injuries by Age Causes (Stacked Bar Chart Percentage)"
]

# Title for the presentation
st.title("Population Presentation")

# Sidebar navigation
tabs = ["Introduction", "Presentation"]
selected_tab = st.sidebar.radio("Select a Tab", tabs, index=1)

if selected_tab == "Introduction":
    # Display intro content here
    st.write("""
        # Welcome to the Population Presentation

        This dashboard provides various insights on population statistics, including:
        
        - Population by Age Group and Gender
        - Population by Total Age Group
        - Population by Year
        
        Navigate through the slides to explore the data visualizations in more detail.
    """)

else:
    # Initialize session state for the current slide
    if 'current_slide' not in st.session_state:
        st.session_state.current_slide = 0

    # Get the current slide index
    current_slide = st.session_state.current_slide

    # Progress bar
    st.markdown(f"#### Slide {current_slide + 1} of {len(html_files)}: {slide_titles[current_slide]}")
    progress_percentage = ((current_slide + 1) / len(html_files)) * 100
    st.markdown(
        f"""
        <div class="progress-bar">
            <div class="progress-bar-fill" style="width: {progress_percentage}%;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Create columns for navigation buttons
    col1, col2, col3 = st.columns([1, 5, 1])

    # Navigation logic
    with col1:
        if st.button("⬅️ Previous", key="prev", disabled=current_slide == 0):
            st.session_state.current_slide -= 1
            st.rerun()

    with col3:
        if st.button("Next ➡️", key="next", disabled=current_slide == len(html_files) - 1):
            st.session_state.current_slide += 1
            st.rerun()

    # Set iframe height for the first 6 slides (increased height)
    if current_slide < 6:
        iframe_height = 800  # Increased height for the first 6 slides
    else:
        iframe_height = 600  # Default height for other slides

    # Render the current slide
    try:
        # Display the HTML content from the file
        html_path = html_files[current_slide]
        with open(html_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Render the HTML content inside a responsive iframe
        components.html(html_content, height=iframe_height, width=1000, scrolling=True)

    except FileNotFoundError:
        st.error(f"File not found: {html_path}")

    # Dropdown for direct navigation to a specific slide
    st.sidebar.markdown("### Go to Slide")
    slide_index = st.sidebar.selectbox(
        "Select Slide", 
        options=range(len(html_files)), 
        format_func=lambda x: f"{x + 1}: {slide_titles[x]}",
        index=current_slide,
    )
    if slide_index != current_slide:
        st.session_state.current_slide = slide_index
        st.rerun()
