import streamlit as st
import requests

# FastAPI base URL
BASE_URL = "http://localhost:8000"

# Page config
st.set_page_config(page_title="SHIKSHA AI Mentor", layout="centered")

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "student_id" not in st.session_state:
    st.session_state.student_id = ""

# Sign Up
def signup():
    st.subheader("Create Account")
    student_id = st.text_input("Student ID")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        res = requests.post(f"{BASE_URL}/signup/", json={"student_id": student_id, "password": password})
        if res.status_code == 200:
            st.success("Account created. You can now log in.")
        else:
            st.error(res.json().get("message", "Error occurred during signup."))

# Login
def login():
    st.subheader("Login")
    student_id = st.text_input("Student ID")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        res = requests.post(f"{BASE_URL}/login/", json={"student_id": student_id, "password": password})
        if res.status_code == 200:
            st.session_state.logged_in = True
            st.session_state.student_id = student_id
            st.success("Logged in successfully.")
        else:
            st.error(res.json().get("message", "Invalid credentials."))

# Ask Question
def ask_question():
    st.title("NCERT Mentor AI")
    st.subheader(f"Welcome, {st.session_state.student_id}")
    question = st.text_input("Enter your question:")
    if question:
        with st.spinner("Thinking..."):
            payload = {
                "question": question,
                "student_id": st.session_state.student_id
            }
            res = requests.post(f"{BASE_URL}/ask_question/", json=payload)
            if res.status_code == 200:
                answer = res.json().get("answer")
                st.success(f"Answer: {answer}")
            else:
                st.error("Failed to get answer from the mentor.")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Login", "Sign Up", "Chatbot"])

if page == "Login":
    login()
elif page == "Sign Up":
    signup()
elif page == "Chatbot":
    if st.session_state.logged_in:
        ask_question()
        if st.button("Sign Out"):
            st.session_state.logged_in = False
            st.session_state.student_id = ""
            st.success("Signed out successfully.")
            st.experimental_rerun()
    else:
        st.warning("Please log in first.")
