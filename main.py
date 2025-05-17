import re
import streamlit as st  # type: ignore

st.set_page_config(page_title="Password Strength Meter By FAMIA", page_icon="🌘", layout="centered")

st.title("🔒 Password Strength Meter")

if 'history' not in st.session_state:
    st.session_state.history = []

def check_password(password):
    score = 0
    feedback = []
    
    # Password length check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long")
    
    # Uppercase and lowercase check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Password should contain at least one uppercase and one lowercase letter")
    
    # Digit check
    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("❌ Password should contain at least one number")
    
    # Special character check
    if re.search(r'[!@#$%^&*()_+\-={}\[\]:;\"\'<>,.?/~`]', password):
        score += 1
    else:
        feedback.append("❌ Password should contain at least one special character")
    
    # Display password strength result
    if score >= 5:
        st.success("✅ Password is very strong")
    elif score == 4:
        st.success("✅ Password is strong")
    elif score == 3:
        st.warning("⚠️ Password is medium")
    else:
        st.error("❌ Password is weak")
    
    # Display improvement suggestions
    if feedback:
        with st.expander("Improve your password"):
            for f in feedback:
                st.write(f)
    
password = st.text_input("Enter your password", type="password", help="Ensure your password is strong and secure.")

if st.button("Check Password Strength"):
    if password:
        check_password(password)  
        if password in st.session_state.history:
            st.error("This password already exists in history. Please choose a different one.")
        else:
            st.session_state.show_history_button = True    
    else:
        st.warning("Please enter a password")

col1, col2 = st.columns(2)
if "show_history_button" in st.session_state and st.session_state.show_history_button:
    with col1:
        if st.button("Save Password"):
            if password in st.session_state.history:
                st.error("This password is already in history!")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters long.")
            elif not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password):
                st.error("Password must contain at least one uppercase and one lowercase letter.")
            elif not re.search(r"[0-9]", password):
                st.error("Password must contain at least one number.")
            elif not re.search(r'[!@#$%^&*()_+\-={}\[\]:;\"\'<>,.?/~`]', password):
                st.error("Password must contain at least one special character.")
            else:
                st.success("✅ Password saved successfully")
                st.session_state.history.append(password) 
    with col2:
        if st.button("Clear History"):
            st.session_state.history = [] 
            st.success("History cleared successfully")

st.subheader("Password History:")
if st.session_state.history:
    for index, item in enumerate(st.session_state.history, start=1):
        st.write(f"{index}. {item}")
else:
    st.write("No passwords saved yet.")