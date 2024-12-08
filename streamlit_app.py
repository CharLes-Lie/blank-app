import streamlit as st
from datetime import datetime, timedelta
import re

# Initialize session state for activities
if "activities" not in st.session_state:
    st.session_state.activities = []

# Utility functions
def validate_time_format(time_str):
    """Validate that the time is in the HH:MM format."""
    time_pattern = r"^(2[0-3]|[01]?[0-9]):([0-5][0-9])$"
    return bool(re.match(time_pattern, time_str))

def calculate_duration(start_time, end_time):
    """Calculate the duration of an activity in minutes."""
    start = datetime.strptime(start_time, "%H:%M")
    end = datetime.strptime(end_time, "%H:%M")
    
    # Handle scenarios where end time is on the next day
    if end < start:
        end += timedelta(days=1)
    
    duration = (end - start).seconds // 60
    return duration

# App layout
def add_activity():
    """Form to add a new activity."""
    with st.form("Add Activity Form"):
        st.write("### Add a New Activity")
        activity_name = st.text_input("Activity Name", placeholder="Enter activity name")
        start_time = st.text_input("Start Time (HH:MM)", placeholder="e.g., 09:00")
        end_time = st.text_input("End Time (HH:MM)", placeholder="e.g., 10:30")
        priority = st.selectbox("Priority Level", ["High", "Medium", "Low"])
        submitted = st.form_submit_button("Add Activity")
        
        if submitted:
            if not activity_name:
                st.warning("Please enter an activity name.")
            elif not validate_time_format(start_time) or not validate_time_format(end_time):
                st.error("Please enter valid start and end times in HH:MM format.")
            elif start_time >= end_time:
                st.error("Start time must be earlier than end time.")
            else:
                st.session_state.activities.append({
                    "name": activity_name,
                    "start_time": start_time,
                    "end_time": end_time,
                    "priority": priority,
                    "duration": calculate_duration(start_time, end_time)
                })
                st.success(f"Activity '{activity_name}' added successfully!")

def display_activities():
    """Display all added activities."""
    st.write("### Your Planned Activities")
    if st.session_state.activities:
        for i, activity in enumerate(st.session_state.activities):
            st.write(f"**{i + 1}. {activity['name']}**")
            st.write(f"- 🕒 **Time**: {activity['start_time']} to {activity['end_time']} "
                    f"({activity['duration']} mins)")
            st.write(f"- ⭐ **Priority**: {activity['priority']}")
            st.divider()
    else:
        st.info("No activities added yet. Use the 'Add Activity' button to get started!")

def prioritize_activities():
    """Prioritize activities based on duration and display suggestions."""
    st.session_state.activities.sort(
        key=lambda x: x["duration"], reverse=True
    )
    st.write("### Suggested Activity Prioritization")
    for i, activity in enumerate(st.session_state.activities):
        st.write(f"**{i + 1}. {activity['name']}**")
        st.write(f"- 🕒 **Time**: {activity['start_time']} to {activity['end_time']} "
                f"({activity['duration']} mins)")
        st.write(f"- ⭐ **Priority**: {activity['priority']}")
        st.divider()

def summary_and_reassurance():
    """Display summary and give motivating messages."""
    total_activities = len(st.session_state.activities)
    st.write("### Daily Summary")
    st.write(f"**Total Activities Planned**: {total_activities}")
    
    # Motivation
    if total_activities == 0:
        st.info("No activities planned? Use this time to relax, reflect, or set some goals!")
    elif total_activities <= 3:
        st.success("You're off to a great start! Focus and finish strong!")
    elif total_activities <= 6:
        st.success("You've got a productive day ahead! Remember to take breaks!")
    else:
        st.warning("You have a packed schedule! Stay organized and take care of yourself.")

    # Suggest breaks after intensive tasks
    if total_activities > 0:
        st.write("\n**Recommended Breaks**")
        st.write("☕ Take a 10-15 minute break after every 90 minutes of work.")
        st.write("🧘 Use short pauses to stretch or be lazy between tasks!")

# Main app function
def main():
    st.header("DayMaster 📋", divider="grey")
    st.write("#### Plan, prioritize, and conquer your day! 🌟")
    
    st.sidebar.header("Navigation")
    page = st.sidebar.radio(
        "Choose an option:",
        ["Add a New Activity", "View Activities", "Prioritize & Summarize"]
    )

    if page == "Add a New Activity":
        add_activity()
    elif page == "View Activities":
        display_activities()
    elif page == "Prioritize & Summarize":
        if st.session_state.activities:
            prioritize_activities()
            summary_and_reassurance()
        else:
            st.info("No activities to prioritize yet. Start by adding some!")

# Run the app
if __name__ == "__main__":
    main()


