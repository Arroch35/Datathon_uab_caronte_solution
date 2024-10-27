# app.py

import streamlit as st
from user_list_page import user_list_page
from user_details_page import user_details_page
from user_statistics_page import user_statistics_page
from quiz_page import quiz_page




# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = 'user_list'

if 'selected_user' not in st.session_state:
    st.session_state.selected_user = None

# Function to navigate between pages
def navigate_to(page_name):
    st.session_state.page = page_name

def main():
    st.set_page_config(page_title="Interactive Programming Quiz", layout="wide")

    
    # Sidebar for navigation
    st.sidebar.title("Navigation 🧭")
    if st.session_state.selected_user:
        st.sidebar.write(f"Logged in as: **{st.session_state.selected_user}**")

        # Adjust sidebar options based on the current page
        if st.session_state.page == 'user_details':
            pages = ['User Details', 'Logout']
        elif st.session_state.page == 'user_statistics':
            pages = ['User Details', 'User Statistics', 'Quiz', 'Logout']
        else:
            pages = ['User Details', 'User Statistics', 'Quiz', 'Logout']
    else:
        pages = ['User List']  # Only show User List if no user is selected

    # Display navigation options based on conditions
    for page in pages:
        if st.sidebar.button(page, key=page):
            if page == 'Logout':
                # Reset session state on logout
                st.session_state.selected_user = None
                st.session_state.page = 'user_list'
            else:
                # Navigate to selected page
                st.session_state.page = page.lower().replace(' ', '_')

    # Display the selected page
    if st.session_state.page == 'user_list':
        user_list_page(navigate_to)
    elif st.session_state.page == 'user_details':
        user_details_page(navigate_to)
    elif st.session_state.page == 'user_statistics':
        if st.session_state.selected_user:
            user_statistics_page(navigate_to)
        else:
            st.warning("Please select a user to access statistics.")
    elif st.session_state.page == 'quiz':
        if st.session_state.selected_user:
            quiz_page(navigate_to)
        else:
            st.warning("Please select a user to access the quiz.")
    else:
        st.error("Page not found.")



if __name__ == "__main__":
    main()
