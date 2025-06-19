# app.py
import streamlit as st
from dotenv import load_dotenv

# Import agent functions and visualizer
from agents import get_parser_agent, get_recommender_agent, get_matcher_agent, get_visualizer_agent
from visualizer import generate_career_graph

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Medical Career Path Mentor",
    page_icon="🩺",
    layout="wide"
)

# --- Load API Key ---
load_dotenv()

# --- Application Title ---
st.title("🩺 AI Medical Career Path Mentor")
st.markdown("Your personal guide to navigating the complexities of a healthcare career. Fill out the form below to begin.")

# --- Sidebar for User Input ---
st.sidebar.header("Your Profile")
st.sidebar.markdown("Please provide your details. The more information you give, the better the recommendations.")

with st.sidebar.form(key='profile_form'):
    academic_bg = st.text_area("Academic Background",
                               placeholder="e.g., M.B.B.S. from AIIMS, Delhi (2022); Internship at Safdarjung Hospital.")
    current_role = st.text_area("Current Role & Experience",
                                placeholder="e.g., Junior Resident in General Medicine at Apollo Hospitals for 1.5 years.")
    interests = st.text_area("Stated Interests & Goals",
                             placeholder="e.g., Interested in cardiology, particularly interventional procedures. Also curious about healthcare management and maybe an MBA in the future.")
    
    submit_button = st.form_submit_button(label='✨ Generate My Career Path')

# --- Main Panel for Agent Outputs ---
if submit_button and academic_bg and current_role and interests:
    full_user_input = f"Academic Background: {academic_bg}\n\nCurrent Role: {current_role}\n\nInterests: {interests}"

    # Agent processing starts here
    st.info("Your request has been submitted. The AI Agents are at work... Please wait.")

    # 1. Career History Parser Agent
    with st.spinner("Agent 1: Parsing your career history..."):
        try:
            parser_agent = get_parser_agent()
            parsed_summary = parser_agent.invoke({"user_input": full_user_input})['text']
        except Exception as e:
            st.error(f"Error with Parser Agent: {e}")
            st.stop()
            
    st.subheader("1. Your Profile Summary")
    st.success("Career History Parser Agent finished.")
    st.markdown(parsed_summary)
    
    # 2. Path Recommender Agent (RAG)
    with st.spinner("Agent 2: Retrieving documents and recommending paths..."):
        try:
            recommender_agent = get_recommender_agent()
            recommended_paths = recommender_agent.invoke(parsed_summary)
        except Exception as e:
            st.error(f"Error with Recommender Agent: {e}")
            st.stop()

    st.subheader("2. Recommended Career Paths")
    st.success("Path Recommender Agent finished.")
    st.markdown(recommended_paths)

    # 3. Mentor & Resource Matcher Agent
    with st.spinner("Agent 3: Matching you with mentors and resources..."):
        try:
            matcher_agent = get_matcher_agent()
            matched_resources = matcher_agent.invoke({"recommended_paths": recommended_paths})['text']
        except Exception as e:
            st.error(f"Error with Matcher Agent: {e}")
            st.stop()
            
    st.subheader("3. Suggested Mentors & Resources")
    st.success("Mentor & Resource Matcher Agent finished.")
    st.markdown(matched_resources)

    # 4. Career Path Visualizer Agent
    with st.spinner("Agent 4: Generating your career visualization..."):
        try:
            visualizer_agent = get_visualizer_agent()
            path_data_for_graph = visualizer_agent.invoke({"recommended_paths": recommended_paths})['text']
            career_graph = generate_career_graph(path_data_for_graph)
        except Exception as e:
            st.error(f"Error with Visualizer Agent: {e}")
            st.stop()

    st.subheader("4. Your Interactive Career Map")
    st.success("Career Path Visualizer Agent finished.")
    st.graphviz_chart(career_graph)

else:
    st.info("Please fill out the form in the sidebar to get started.")