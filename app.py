# app.py

import streamlit as st
from datetime import datetime
from models import (
    ContentCreatorInfo,
    ValueObject,
    ChallengeObject,
    AchievementObject,
    LifeEventObject,
    BusinessObject
)
from agent import ContentAnalysisAgent, AgentConfig
from utils import save_output_to_markdown
import json

# Initialize the AI Agent
def initialize_agent():
    config = AgentConfig(
        name="CreatorAnalyst v1.0",
        role="Comprehensive YouTube Creator Analysis System"
    )
    return ContentAnalysisAgent(config)

# Main application
def main():
    st.set_page_config(
        page_title="YouTube Creator Analyst",
        page_icon="📊",
        layout="wide"
    )

    # Initialize session state
    if 'creator_data' not in st.session_state:
        st.session_state.creator_data = {}
    if 'analysis' not in st.session_state:
        st.session_state.analysis = {}

    # Initialize agent
    agent = initialize_agent()

    # Header Section
    st.title("📈 YouTube Creator Analysis System")
    st.markdown("""
    ### Comprehensive Content Creator Profiling Tool
    Analyze YouTube creators' personal lives, businesses, values, challenges, and achievements.
    """)

    # Main Form
    with st.form("creator_info_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Personal Information")
            creator_name = st.text_input("Creator Name*", help="Full channel name or personal name")
            channel_url = st.text_input("YouTube Channel URL*")
            niche = st.selectbox(
                "Primary Content Niche*",
                ["Tech", "Lifestyle", "Education", "Entertainment", "Gaming", "Other"]
            )
            start_year = st.number_input("Channel Start Year*", 2005, datetime.now().year)

        with col2:
            st.subheader("Demographic Info")
            country = st.text_input("Country", "Unknown")
            age = st.number_input("Age", 18, 100)
            team_size = st.number_input("Team Size", 0, 100, 0)
            monthly_views = st.number_input("Avg Monthly Views (millions)", 0.0, 100.0, 0.0)

        # Dynamic Lists
        st.subheader("Core Elements")
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Values", "Challenges", "Achievements", "Life Events", "Businesses"])

        with tab1:
            st.markdown("**Core Values**")
            if 'values_count' not in st.session_state:
                st.session_state.values_count = 1
            for i in range(st.session_state.values_count):
                with st.container():
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.text_input(f"Value {i+1} Name*", key=f"value_name_{i}")
                    with col_b:
                        st.text_area(f"Value {i+1} Description", key=f"value_desc_{i}")

            # استخدام st.form_submit_button بدلاً من st.button
            if st.form_submit_button("➕ Add Value"):
                st.session_state.values_count += 1


        # Similar tabs for Challenges, Achievements, Life Events, and Businesses
        # (Implementation pattern similar to Values tab)

        # Form submission
        submitted = st.form_submit_button("Analyze Creator")
        if submitted:
            try:
                # Validate required fields
                if not creator_name or not channel_url or not niche:
                    st.error("Please fill all required fields (*)")
                    return

                # Process form data
                process_creator_data(agent)
                st.success("Analysis completed successfully!")
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")

    # Display Results
    if st.session_state.analysis:
        st.divider()
        st.subheader("Analysis Results")
        
        # Generate report
        report_path = agent.generate_report(st.session_state.analysis)
        
        col_left, col_right = st.columns(2)
        with col_left:
            st.download_button(
                label="Download Full Report",
                data=json.dumps(st.session_state.analysis, indent=2),
                file_name=f"{creator_name}_analysis.json",
                mime="application/json"
            )
            
        with col_right:
            with open(report_path, "r") as f:
                st.download_button(
                    label="Download Markdown Report",
                    data=f,
                    file_name=f"{creator_name}_analysis.md",
                    mime="text/markdown"
                )

        # Show analysis preview
        with st.expander("Preview Analysis Summary"):
            st.json(st.session_state.analysis)

def process_creator_data(agent):
    """Process form data and run analysis"""
    # Collect values
    values = []
    for i in range(st.session_state.values_count):
        values.append(ValueObject(
            name=st.session_state[f"value_name_{i}"],
            description=st.session_state.get(f"value_desc_{i}", "")
        ))

    # Collect other sections similarly (challenges, achievements, etc.)
    
    # Build ContentCreatorInfo object
    creator_info = ContentCreatorInfo(
        personal_info={
            "name": st.session_state.creator_name,
            "channel_url": st.session_state.channel_url,
            "niche": st.session_state.niche,
            "start_year": st.session_state.start_year,
            "country": st.session_state.country,
            "age": st.session_state.age,
            "team_size": st.session_state.team_size,
            "monthly_views": st.session_state.monthly_views
        },
        values=values,
        challenges=[],  # Add collected challenges
        achievements=[],  # Add collected achievements
        life_events=[],  # Add collected life events
        businesses=[]  # Add collected businesses
    )

    # Run analysis
    analysis = agent.analyze_creator(creator_info.dict())
    st.session_state.analysis = analysis

if __name__ == "__main__":
    main()