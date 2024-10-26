# quiz_page.py

import streamlit as st

def quiz_page(navigate_to):
    st.title("🎓 Welcome to the Interactive Programming Quiz")

    # Initialize quiz-related session state variables
    if 'question_index' not in st.session_state:
        st.session_state.question_index = 0
    if 'show_feedback' not in st.session_state:
        st.session_state.show_feedback = False
    if 'quiz_complete' not in st.session_state:
        st.session_state.quiz_complete = False

    # Define quiz questions
    quiz_questions = [
        {
            "question": "What is the output of the following code if x = 5? \n\n `print(x * 2)`",
            "options": ["A) 10", "B) 15", "C) 5", "D) None of the above"],
            "correct": "A) 10",
            "explanation": "The code multiplies the value of x by 2, so with x = 5, the output is 10."
        },
        {
            "question": "Which data type is used to store True/False values in Python?",
            "options": ["A) int", "B) str", "C) bool", "D) float"],
            "correct": "C) bool",
            "explanation": "The 'bool' type is used for Boolean values, which can either be True or False."
        },
        {
            "question": "What will be the result of `len([1, 2, 3, 4])`?",
            "options": ["A) 3", "B) 4", "C) 5", "D) Error"],
            "correct": "B) 4",
            "explanation": "The len() function returns the number of items in a list. Here, there are 4 items."
        }
    ]

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
