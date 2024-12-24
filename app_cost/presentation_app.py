import streamlit as st
import streamlit.components.v1 as components

# Set page configuration (must be the first Streamlit command)
st.set_page_config(page_title="Fall Expenditure Presentation", layout="wide")

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
            margin-top: 0;
        }

        h3 {
            font-size: 1.5em;
            color: #555;
            text-align: center;
            margin-top: -5px;
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

        iframe {
            width: 100% !important;
            height: 600px;
            border: none;
            margin-top: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Define slides (title and associated HTML files)
slides = [
    ("Total Expenditure Over Years", "html_cost/total_expenditure_over_years_line.html"),
    ("Expenditure Over Year by Area of Expenditure", "html_cost/area_of_expenditure_over_years.html"),
    ("Details of Expenditure", "html_cost/area_of_expenditure_over_years_bar.html"),
    ("Total Expenditure and Total Cases by Age Groups", "html_cost/total_expenditure_and_cases_over_age_group.html"),
    ("Average Expenditure per person by age groups", "html_cost/experditure_per_person_age_group.html"),
    ("Average Hospital cost vs Home cost per patient by Age Groups", "html_cost/average_hospital_vs_home_cost.html"),
    ("Total Hospital cost", "html_cost/total_cost_at_hospital.html"),
    ("Total Hospital cost by age group", "html_cost/cost_category_over_age_group_at_hospital.html"),
    ("Total Hospital cost by age group stacked bar chart", "html_cost/cost_category_over_age_group_percentage_at_hospital.html"),
    ("Total Home cost by age group", "html_cost/total_cost_at_home.html"),
    ("Total Home cost by age group and categories", "html_cost/cost_category_over_age_group_at_home.html"),
    ("Total Home cost by age group stacked bar chart", "html_cost/cost_category_over_age_group_percentage_at_home.html"),
    ("Average number of days in hospital for hospitalisations due to falls, by age group and sex, 2019–20", "html_cost/days_in_hospital.html"),
    ("Total Expenditure per Person for a Day by Age Groups and Gender", "html_cost/average_expenditure_a_day_age_group.html"),
]

# Title for the presentation
st.title("Fall Expenditure Presentation")

# Sidebar navigation tabs
tabs = ["Introduction", "Presentation", "Suggested Solution", "References"]
selected_tab = st.sidebar.radio("Select a Tab", tabs, index=1)

if selected_tab == "Introduction":
    # Introduction content
    st.write(""" 
        # Welcome to the Fall Expenditure Presentation

        Explore visual insights on Fall Expenditures, including:
        - Areas of expenditures for fall injuries
        - Estimated average expenditure per patient
        
        Navigate through the slides to view the interactive visualizations.
    """)

elif selected_tab == "Presentation":
    # Initialize session state for slide index
    if 'current_slide' not in st.session_state:
        st.session_state.current_slide = 0

    # Current slide index
    current_slide = st.session_state.current_slide

    # Progress bar
    st.markdown(f"#### Slide {current_slide + 1} of {len(slides)}: {slides[current_slide][0]}")
    progress_percentage = ((current_slide + 1) / len(slides)) * 100
    st.markdown(
        f"""
        <div class="progress-bar">
            <div class="progress-bar-fill" style="width: {progress_percentage}%;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 5, 1])

    with col1:
        if st.button("⬅️ Previous", key="prev", disabled=current_slide == 0):
            st.session_state.current_slide -= 1
            st.rerun()

    with col3:
        if st.button("Next ➡️", key="next", disabled=current_slide == len(slides) - 1):
            st.session_state.current_slide += 1
            st.rerun()

    # Display the selected HTML slide
    slide_title, html_filename = slides[current_slide]
    try:
        if slide_title == "Average Hospital cost vs Home cost per patient by Age Groups":
            # Add explanation for slide 6
            st.write("""
            ### Defining Hospital and Home Service Categories

            To better analyze healthcare costs, we categorize services as follows:

            **Hospital Services**
            - Public hospital outpatient
            - Public hospital emergency department
            - Public hospital admitted patient
            - Private hospital services
            - Medical imaging
            - Dental expenditure

            **Home Services**
            - General practitioner services
            - Allied health and other services
            - Pharmaceutical benefits scheme
            - Pathology
            - Specialist services
            """)

        with open(html_filename, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Embed HTML content
        components.html(html_content, height=600, scrolling=True)

    except FileNotFoundError:
        st.error(f"File not found: {html_filename}")

    # Dropdown for direct slide navigation
    st.sidebar.markdown("### Go to Slide")
    slide_index = st.sidebar.selectbox(
        "Select Slide", 
        options=range(len(slides)), 
        format_func=lambda x: f"{x + 1}: {slides[x][0]}",
        index=current_slide,
    )
    if slide_index != current_slide:
        st.session_state.current_slide = slide_index
        st.rerun()

elif selected_tab == "Suggested Solution":
    st.header("Suggested Solution: Camera-Assisted Monitoring Devices")
    st.markdown("""
    ### Overview
    Camera-assisted monitoring devices have emerged as a promising solution to prevent hospital falls. Evidence from various studies supports their effectiveness in reducing fall rates, particularly during overnight shifts and among older patients.

    ### Supporting Evidence
    - **Quigley et al. (2019)**: Demonstrated that older patients benefited more than younger patients from video monitoring when they actively participated in surveillance of their activities.
    - **Sand-Jecklin et al. (2018)**: Highlighted positive feedback from nursing staff and video monitoring technicians on the effectiveness of these devices. However, patients and families expressed concerns about privacy.
    - **Woltsche et al. (2022)**: Reported a significant reduction in overnight falls due to the use of portable video monitoring devices.

    ### Key Benefits
    - **Fall Reduction**: Studies consistently show reduced fall rates with video-assisted monitoring.
    - **Real-Time Intervention**: Allows healthcare staff to respond quickly to potential fall risks.
    - **Improved Safety for Older Patients**: Particularly effective in reducing falls in older patient populations.

    ### Challenges
    - **Privacy Concerns**: Patients and families have voiced concerns about the impact of video monitoring on privacy, which needs to be addressed through transparent communication and informed consent.

    ### Conclusion
    Implementing camera-assisted monitoring devices in hospital settings is a viable strategy to enhance patient safety and reduce falls. Addressing privacy concerns and fostering collaboration among patients, families, and healthcare staff are critical for the success of this approach.
    """)
    
elif selected_tab == "References":
    # References section
    st.write("""
        # Data Sources 

        The data and relevant information presented in this presentation is collected from the following sources:

        1. Health & welfare expenditure Data. (n.d.). Australian Institute of Health and Welfare. https://www.aihw.gov.au/reports-data/health-welfare-overview/health-welfare-expenditure/data

        2. Falls in older Australians 2019–20: hospitalisations and deaths among people aged 65 and over, Data. (n.d.). Australian Institute of Health and Welfare. https://www.aihw.gov.au/reports/injury/falls-in-older-australians-2019-20-hospitalisation/data
             
        3. Injury in Australia, Data. (15 C.E., November). Australian Institute of Health and Welfare. https://www.aihw.gov.au/reports/injury/injury-in-australia/data

        4. Oriaifo, P. (2023). Camera-assisted monitoring device as a tool to reduce falls in inpatient adults: An integrative review (Doctoral dissertation, Liberty University). Liberty University Digital Commons. https://digitalcommons.liberty.edu/doctoral/4902     

    """)
