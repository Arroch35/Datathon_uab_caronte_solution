# user_statistics_page.py

import streamlit as st
import pandas as pd
from pandasql import sqldf

def user_statistics_page(navigate_to):
    # Load the user statistics data
    df = pd.read_csv("../data/users_clean_vApplication.csv")

    # Filter data for the selected user
    user_data = df[df['userid'] == int(st.session_state.selected_user)]
    print(user_data)
    # Create a top row with two columns: one for the title and one for the "Start Quiz" button aligned to the right
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.title(f"Hello, {st.session_state.selected_user}! 👋")

    with col2:
        st.button("Start Quiz", on_click=lambda: reset_quiz_and_navigate(navigate_to, 'quiz'))

    # Main content: user statistics and charts
    st.subheader("Your Statistics 📊")

    # Track statistics internally
    num_quizzes = st.session_state.get('num_quizzes', 0)
    avg_score = sum(st.session_state.get('quiz_scores', [])) / num_quizzes if num_quizzes > 0 else 0

    num_quizzes = st.session_state.num_quizzes
    avg_score = sum(st.session_state.quiz_scores) / num_quizzes if num_quizzes > 0 else 0

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Number of Quizzes Taken", num_quizzes)
    with col2:
        st.metric("Average Score", f"{avg_score:.2f}%")

    # Quiz Scores Over Time
    st.subheader("Quiz Scores Over Time 📈")
    st.line_chart(pd.Series(st.session_state.get('quiz_scores', [])))

    # Average Grades for Lesson
    st.subheader("Average Grades for Lesson 🧮")
    if not user_data.empty:
        user_data['problema_number'] = user_data['activitat'].str.extract(r'Problema\s+(\d+)')
        result = user_data.groupby(['userid', 'problema_number'], as_index=False)['grade'].mean()
        st.bar_chart(result.set_index('problema_number')['grade'])

    # Performance Breakdown by Topic
    st.subheader("Number of Tries Per Activity 📚")
    neval_activities=f"select activitat, nevaluations from user_data where userid={int(st.session_state.selected_user)}"
    data_neval = sqldf(neval_activities)
    topics = data_neval['nevaluations']
    performance = data_neval['activitat']
    df_performance = pd.DataFrame({'Topic': topics, 'Performance': performance})
    st.bar_chart(df_performance.set_index('Topic'))

    st.button("Back to User Details", on_click=lambda: navigate_to('user_details'))

def reset_quiz_and_navigate(navigate_to, page_name):
    st.session_state.question_index = 0
    st.session_state.show_feedback = False
    st.session_state.quiz_complete = False
    navigate_to(page_name)


