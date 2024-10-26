# user_statistics_page.py

import streamlit as st
import pandas as pd

def user_statistics_page(navigate_to):
    # Create a top row with two columns: one for the title and one for the "Start Quiz" button aligned to the right
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.title(f"Hello, {st.session_state.selected_user}! 👋")

    with col2:
        st.button("Start Quiz", on_click=lambda: reset_quiz_and_navigate(navigate_to, 'quiz'))

    # Main content: user statistics and charts
    st.subheader("Your Statistics 📊")

    # Placeholder statistics (replace with actual data)
    num_quizzes = 5
    avg_score = 80

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Number of Quizzes Taken", num_quizzes)
    with col2:
        st.metric("Average Score", f"{avg_score}%")

    # Example plots
    st.subheader("Quiz Scores Over Time 📈")

    # Generate sample data
    dates = pd.date_range('2023-01-01', periods=num_quizzes)
    scores = [75, 85, 90, 80, 95]
    df_scores = pd.DataFrame({'Date': dates, 'Score': scores})

    # Line chart for scores over time
    st.line_chart(df_scores.set_index('Date')['Score'])

    # Additional Plots
    st.subheader("Score Distribution 🧮")
    # Histogram of scores
    st.bar_chart(df_scores['Score'])

    st.subheader("Performance Breakdown by Topic 📚")
    topics = ['Math', 'Science', 'History', 'Art', 'Technology']
    performance = [85, 90, 75, 80, 95]
    df_performance = pd.DataFrame({'Topic': topics, 'Performance': performance})

    # Bar chart for performance by topic
    st.bar_chart(df_performance.set_index('Topic'))

    st.button("Back to User Details", on_click=lambda: navigate_to('user_details'))

def reset_quiz_and_navigate(navigate_to, page_name):
    # Reset quiz session state variables
    st.session_state.question_index = 0
    st.session_state.show_feedback = False
    st.session_state.quiz_complete = False
    navigate_to(page_name)
