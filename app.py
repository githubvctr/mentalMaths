import streamlit as st
from mental_maths.assessment import Assessment
from mental_maths.question_generator import QuestionGenerator
import pandas as pd
import yaml
import time

# Load configuration from config.yml
def load_config():
    with open("src/mental_maths/config.yml", "r") as file:
        return yaml.safe_load(file)

config = load_config()
section_question_counts = config["section_question_counts"]

# Page Configuration
st.set_page_config(page_title="Mental Maths Dashboard", layout="wide")

# Title
st.title("🧠 Mental Maths Interactive Dashboard")

# Sidebar - Test Configuration
st.sidebar.header("Test Configuration")
sections = st.sidebar.multiselect(
    "Choose Sections to Test:",
    ["Section 1", "Section 2", "Section 3"],
    default=["Section 1", "Section 2", "Section 3"]
)

# Initialize session state variables
if "assessment_started" not in st.session_state:
    st.session_state.assessment_started = False
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "questions" not in st.session_state:
    st.session_state.questions = []
if "correct_answers" not in st.session_state:
    st.session_state.correct_answers = []
if "choices" not in st.session_state:
    st.session_state.choices = []
if "user_answers" not in st.session_state:
    st.session_state.user_answers = []
if "current_section" not in st.session_state:
    st.session_state.current_section = 0
if "section_times" not in st.session_state:
    st.session_state.section_times = {}
if "question_start_time" not in st.session_state:
    st.session_state.question_start_time = None

# Function to start assessment
def start_assessment():
    st.session_state.assessment_started = True
    st.session_state.current_question = 0
    st.session_state.questions = []
    st.session_state.correct_answers = []
    st.session_state.choices = []
    st.session_state.user_answers = []
    st.session_state.current_section = 0
    st.session_state.section_times = {}
    st.session_state.question_start_time = time.time()
    
    assessment = Assessment(QuestionGenerator())

    for section_name in sections:
        sec_number = int(section_name.split()[-1])
        num_questions = section_question_counts[section_name]
        questions, answers, choices = assessment.question_generator.generate_questions(sec_number)

        st.session_state.questions.append((section_name, questions, answers, choices))

# Start Test Button
if not st.session_state.assessment_started:
    if st.button("Start Test"):
        start_assessment()
        st.rerun()

# Display Questions One by One
if st.session_state.assessment_started:
    sections_data = st.session_state.questions
    if st.session_state.current_section < len(sections_data):
        section_name, section_questions, section_answers, section_choices = sections_data[st.session_state.current_section]
        total_questions = len(section_questions)

        if st.session_state.current_question < total_questions:
            question_text = section_questions[st.session_state.current_question]
            correct_answer = section_answers[st.session_state.current_question]
            choices = section_choices[st.session_state.current_question] if section_name == "Section 3" else None

            st.subheader(f"{section_name} - Question {st.session_state.current_question + 1} / {total_questions}")
            st.write(f"{question_text} = ")

            with st.form(key="answer_form", clear_on_submit=True):
                if section_name == "Section 3":
                    user_answer = st.radio("Choose the correct answer:", choices, key="mcq_input")
                else:
                    user_answer = st.text_input("Your Answer", key="answer_input")

                submit_button = st.form_submit_button("Submit Answer")

            if submit_button and user_answer:
                time_taken = time.time() - st.session_state.question_start_time
                st.session_state.user_answers.append((section_name, question_text, user_answer, correct_answer, time_taken))
                st.session_state.current_question += 1
                st.session_state.question_start_time = time.time()
                st.rerun()

        else:
            # Section completed
            st.success(f"✅ {section_name} Completed!")

            section_results = [ua for ua in st.session_state.user_answers if ua[0] == section_name]
            correct_count = sum(1 for q in section_results if str(q[2]) == str(q[3]))
            avg_time_per_question = sum(q[4] for q in section_results) / len(section_results)

            st.write(f"**Score: {correct_count} / {total_questions}**")
            st.write(f"**Average Time per Question: {avg_time_per_question:.2f} seconds**")

            # Save section data
            st.session_state.section_times[section_name] = avg_time_per_question

            # If it's the last section, show "See Results" instead of "Next Section"
            if st.session_state.current_section == len(sections_data) - 1:
                if st.button("See Results"):
                    st.session_state.current_section += 1
                    st.session_state.current_question = 0
                    st.rerun()
            else:
                if st.button("Next Section"):
                    st.session_state.current_section += 1
                    st.session_state.current_question = 0
                    st.session_state.question_start_time = time.time()
                    st.rerun()

    else:
        # All sections completed
        st.success("🎉 All Sections Completed! Here are your results:")

        results_df = pd.DataFrame(st.session_state.user_answers, columns=["Section", "Question", "Your Answer", "Correct Answer", "Time Taken (s)"])
        results_df["Correct"] = results_df.apply(lambda row: "✅" if str(row["Your Answer"]) == str(row["Correct Answer"]) else "❌", axis=1)
        st.dataframe(results_df)

        # Save results
        results_df.to_csv("results.csv", index=False, mode='a', header=False)

        # Display section scores
        for section in sections:
            if section in st.session_state.section_times:
                st.write(f"**{section}: Average Time per Question - {st.session_state.section_times[section]:.2f} sec**")

        # Restart button
        if st.button("Restart Test"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
