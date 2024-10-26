# user_list_page.py

import streamlit as st

def user_list_page(navigate_to):
    st.title("User List 👥")

    # Placeholder list of users (replace with your actual user data)
    users = ['Alice', 'Bob', 'Charlie', 'David']

    st.write("Select a user to view details:")
    selected_user = st.selectbox("Users", users)

    def set_user_and_navigate():
        st.session_state.selected_user = selected_user
        navigate_to('user_details')

    st.button("Go to User Details", on_click=set_user_and_navigate)
