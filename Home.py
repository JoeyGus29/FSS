# home.py

import streamlit as st

# Simulated "user database" (for demo purposes only)
if "users" not in st.session_state:
    st.session_state.users = {"test@example.com": "password123"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_email" not in st.session_state:
    st.session_state.login_email = ""
if "signup_mode" not in st.session_state:
    st.session_state.signup_mode = False

def login():
    st.session_state.logged_in = True

def logout():
    st.session_state.logged_in = False
    st.session_state.login_email = ""

def show_login():
    st.header("GridironIQ Login")
    st.write("Don't have an account? [Sign up here](#)", unsafe_allow_html=True)
    with st.form("login_form"):
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        submit = st.form_submit_button("Log in")
        if submit:
            if email in st.session_state.users and st.session_state.users[email] == password:
                st.success("Login successful!")
                st.session_state.login_email = email
                login()
            else:
                st.error("Invalid email or password.")

def show_signup():
    st.header("GridironIQ Sign Up")
    st.write("Already have an account? [Log in here](#)", unsafe_allow_html=True)
    with st.form("signup_form"):
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        submit = st.form_submit_button("Sign up")
        if submit:
            if email in st.session_state.users:
                st.error("Email already registered.")
            else:
                st.session_state.users[email] = password
                st.success("Sign up successful! Please log in.")
                st.session_state.signup_mode = False

# Toggle between login and signup
if not st.session_state.logged_in:
    if not st.session_state.signup_mode:
        show_login()
        if st.button("Sign up for an account"):
            st.session_state.signup_mode = True
    else:
        show_signup()
        if st.button("Back to login"):
            st.session_state.signup_mode = False
else:
    st.success(f"Welcome, {st.session_state.login_email}!")
    if st.button("Log out"):
        logout()
    st.markdown("---")
    st.write("🏈 **Welcome to the GridironIQ Fantasy Success Score Dashboard!**")
    st.write("Use the sidebar to navigate to player rankings and analysis pages.")
