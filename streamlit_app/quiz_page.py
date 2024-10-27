# quiz_page.py
import sys
import os
sys.path.insert(0, os.path.abspath('../src'))
import json
import random
import streamlit as st
from qgen import *
from difflib import SequenceMatcher

# Ensure session state variables for tracking quizzes are initialized
if 'num_quizzes' not in st.session_state:
    st.session_state.num_quizzes = 0
if 'quiz_scores' not in st.session_state:
    st.session_state.quiz_scores = []

def load_or_generate_quiz_questions():
    pdf_paths = [random.choice(["../example.pdf", "../recursion.pdf"])]
    processor = EducationalPDFProcessor()
    return processor.process_pdf_and_generate_qa(pdf_paths, max_questions=3, use_beam_search=False)

def check_similarity(answer, correct_answer):
    return SequenceMatcher(None, answer, correct_answer).ratio() > 0.7

def quiz_page(navigate_to):
    st.title("🎓 Welcome to the Interactive Programming Quiz")

    if 'question_index' not in st.session_state:
        st.session_state.question_index = 0
    if 'show_feedback' not in st.session_state:
        st.session_state.show_feedback = False
    if 'quiz_complete' not in st.session_state:
        st.session_state.quiz_complete = False
    if 'selected_user' in st.session_state:
        user_key = f"quiz_questions_{st.session_state.selected_user}"

        if user_key not in st.session_state:
            st.session_state[user_key] = load_or_generate_quiz_questions()
        
        quiz_questions = st.session_state[user_key]

        st.markdown(f"**Question {min(st.session_state.question_index + 1, len(quiz_questions))} of {len(quiz_questions)}**")

        if not st.session_state.quiz_complete:
            question_data = quiz_questions[st.session_state.question_index]
            st.subheader(f"Question {st.session_state.question_index + 1}")
            st.write(question_data["question"])

            if len(question_data["options"]) == 1:
                user_answer = st.text_input("Your answer:", key=f"answer_input_{st.session_state.question_index}")
                if st.button("Submit Answer", key=f"submit_{st.session_state.question_index}"):
                    st.session_state[f"answer_{st.session_state.question_index}"] = user_answer
                    check_answer(user_answer, question_data)
            else:
                selected_option = st.radio("Select your answer:", question_data["options"], key=f"q{st.session_state.question_index}")
                if st.button("Submit Answer", key=f"submit_{st.session_state.question_index}"):
                    st.session_state[f"answer_{st.session_state.question_index}"] = selected_option
                    check_answer(selected_option, question_data)

            if st.session_state.show_feedback:
                st.button("Next Question ➡️", on_click=next_question, key=f"next{st.session_state.question_index}")
        else:
            st.subheader("Quiz Completed! 🎉")
            st.write("You've reached the end of the quiz. Thank you for participating!")
            st.balloons()
            record_quiz_score()
            if st.button("Back to User Statistics"):
                reset_quiz_state()
                navigate_to('user_statistics')

def display_question(quiz_questions):
    st.markdown(f"**Question {st.session_state.question_index + 1} of {len(quiz_questions)}**")
    question_data = quiz_questions[st.session_state.question_index]
    st.subheader(f"Question {st.session_state.question_index + 1}")
    st.write(question_data["question"])
    # Answer handling (similarity or multiple-choice)
    if len(question_data["options"]) == 1:
        handle_text_answer(question_data)
    else:
        handle_multiple_choice(question_data)

def handle_text_answer(question_data):
    user_answer = st.text_input("Your answer:", key=f"answer_{st.session_state.question_index}")
    if st.button("Submit Answer", key=f"submit_{st.session_state.question_index}"):
        check_and_provide_feedback(user_answer, question_data["correct"], question_data["explanation"])

def handle_multiple_choice(question_data):
    selected_option = st.radio("Select your answer:", question_data["options"], key=f"q{st.session_state.question_index}")
    if st.button("Submit Answer", key=f"submit_{st.session_state.question_index}"):
        check_and_provide_feedback(selected_option, question_data["correct"], question_data["explanation"])

def check_and_provide_feedback(answer, correct_answer, explanation):
    if check_similarity(answer, correct_answer) if isinstance(answer, str) else answer == correct_answer:
        st.success("🎉 Correct! Great job!")
    else:
        st.error("❌ That's incorrect.")
        st.write(f"The correct answer is: **{correct_answer}**")
        st.write(f"Explanation: {explanation}")
    st.session_state.show_feedback = True
    st.button("Next Question ➡️", on_click=next_question)

def next_question():
    # Move to the next question or mark quiz as complete
    if st.session_state.question_index + 1 >= 3:
        st.session_state.quiz_complete = True
    else:
        st.session_state.question_index += 1
    st.session_state.show_feedback = False

def reset_quiz_state():
    st.session_state.question_index = 0
    st.session_state.show_feedback = False
    st.session_state.quiz_complete = False

def check_answer(user_answer, question_data):
    if check_similarity(user_answer, question_data["correct"]):
        st.success("🎉 Correct! Great job!")
    else:
        st.error("❌ That's incorrect.")
        st.write(f"The correct answer is: **{question_data['correct']}**")
        st.write(f"Explanation: {question_data['explanation']}")
    st.session_state.show_feedback = True

def record_quiz_score():
    score = sum(
        1 for i in range(3) if check_similarity(
            st.session_state.get(f"answer_{i}", ""), 
            st.session_state[f"quiz_questions_{st.session_state.selected_user}"][i]["correct"]
        )
    ) * 100 / 3
    st.session_state.quiz_scores.append(score)
    st.session_state.num_quizzes += 1



