# quiz_page.py
import sys
import os
sys.path.insert(0, os.path.abspath('../src'))
import json
from qgen import *
import streamlit as st


def load_or_generate_quiz_questions():
    pdf_paths = ["../example.pdf"]
    processor = EducationalPDFProcessor()
    return processor.process_pdf_and_generate_qa(pdf_paths, max_questions=3, use_beam_search=False)

def quiz_page(navigate_to):
    st.title("🎓 Welcome to the Interactive Programming Quiz")

    # Initialize quiz-related session state variables
    if 'question_index' not in st.session_state:
        st.session_state.question_index = 0
    if 'show_feedback' not in st.session_state:
        st.session_state.show_feedback = False
    if 'quiz_complete' not in st.session_state:
        st.session_state.quiz_complete = False

    # Load questions only if the selected user has not been processed
    if 'selected_user' in st.session_state:
        user_key = f"quiz_questions_{st.session_state.selected_user}"

        # Check if quiz questions already exist for the selected user
        if user_key not in st.session_state:
            # Generate questions for a new user
            st.session_state[user_key] = load_or_generate_quiz_questions()
        
        # Retrieve the questions for the current user
        quiz_questions = st.session_state[user_key]

        # Teacher's Recommendations in an expander box
        with st.expander("📘 Teacher's Recommendations"):
            st.write("""
            - Review the basics of programming functions before starting.
            - Focus on understanding control flow, especially loops and conditional statements.
            - Practice with sample code snippets to reinforce learning.
            """)

        # Display a progress indicator
        st.markdown(f"**Question {min(st.session_state.question_index + 1, len(quiz_questions))} of {len(quiz_questions)}**")

        # Check if the quiz is complete
        if not st.session_state.quiz_complete:
            # Display the current question and options
            question_data = quiz_questions[st.session_state.question_index]
            st.subheader(f"Question {st.session_state.question_index + 1}")
            st.write(question_data["question"])  # Display the question text

            # Display options as a radio button group
            selected_option = st.radio("Select your answer:", question_data["options"], key=f"q{st.session_state.question_index}")

            # Submit answer button
            if st.button("Submit Answer", key=f"submit{st.session_state.question_index}"):
                if selected_option == question_data["correct"]:
                    st.success("🎉 Correct! Great job!")
                else:
                    st.error("❌ That's incorrect.")
                    st.write(f"The correct answer is: **{question_data['correct']}**")
                    st.write(f"Explanation: {question_data['explanation']}")
                st.session_state.show_feedback = True  # Show the Next Question button after feedback

            # Show Next Question button only after submitting the answer
            if st.session_state.show_feedback:
                st.button("Next Question ➡️", on_click=next_question, key=f"next{st.session_state.question_index}")
        
        else:
            # Display completion message after the last question
            st.subheader("Quiz Completed! 🎉")
            st.write("You've reached the end of the quiz. Thank you for participating!")
            st.balloons()  # Display balloons animation on completion

            # Single-click navigation to go back to User Statistics
            if st.button("Back to User Statistics"):
                reset_quiz_state()
                navigate_to('user_statistics')

def next_question():
    # Move to the next question and check if we've reached the end
    if st.session_state.question_index + 1 >= 3:  # Replace 3 with len(quiz_questions) for dynamic quizzes
        st.session_state.quiz_complete = True
    else:
        st.session_state.question_index += 1
    st.session_state.show_feedback = False

def reset_quiz_state():
    """Reset the quiz-related session state variables to start fresh."""
    st.session_state.question_index = 0
    st.session_state.show_feedback = False
    st.session_state.quiz_complete = False

