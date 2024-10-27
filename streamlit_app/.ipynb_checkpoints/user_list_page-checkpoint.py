# user_list_page.py

import streamlit as st
import pickle
import pandas as pd

def user_list_page(navigate_to):
    st.title("User List 👥")

    # Placeholder list of users (replace with your actual user data)
    users = ['1743', '1976', '473', '859']
    df = pd.read_csv("../data/users_processing_vModel.csv")


    st.write("Select a user to view details:")
    selected_user = st.selectbox("Users", users)

    def set_user_and_navigate():
        st.session_state.selected_user = selected_user
        user=df[df['userid']==int(selected_user)]
        user=user.drop('F_Grade', axis=1)
        user.drop('userid', axis=1)
        
        navigate_to('user_details')

    st.button("Go to User Details", on_click=set_user_and_navigate)
