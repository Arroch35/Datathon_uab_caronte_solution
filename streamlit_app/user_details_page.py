# user_details_page.py

import streamlit as st

def user_details_page(navigate_to):
    # Create a top row for the title and the button, aligned together
    col1, col2 = st.columns([4, 1])

    with col1:
        st.title("Caronte 📋")

    with col2:
        st.button("AI Assistant", on_click=lambda: navigate_to('user_statistics'))

    # Display selected user details
    if 'selected_user' in st.session_state and st.session_state.selected_user:
        selected_user = st.session_state.selected_user
        pass_mark = st.session_state.get('pass_mark', False)

        st.subheader(f"Details for {selected_user}")
        st.write("Assigned Problems 📝")
        problems = ['Problem A', 'Problem B', 'Problem C']
        st.write(f"Problems assigned to {selected_user}: {', '.join(problems)}")

        # Check pass or fail and display messages accordingly
        if pass_mark:
            st.success("🎉 Congratulations! The predicted final mark indicates a pass.")
        else:
            st.error("⚠️ The predicted final mark indicates a fail.")
            st.write("**Recommendation:** We suggest retaking a quiz for improvement.")

        # "Back to User List" button
        st.button("Back to User List", on_click=lambda: navigate_to('user_list'))
    else:
        st.error("No user selected. Please go back to the User List page.")
