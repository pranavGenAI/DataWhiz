import streamlit as st 
from pandasai.llm import GooglePalm
import os
import pandas as pd
from pandasai import SmartDataframe
#from pandasai import PandasAI
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from streamlit.components.v1 import html
import hashlib
import json

api_key = "AIzaSyCiPGxwD04JwxifewrYiqzufyd25VjKBkw"
#st.secrets['GEMINI_API_KEY']

st.set_page_config(page_title="DataViz", layout='wide')

def chat_with_csv(df, prompt):
    llm = GooglePalm(api_key=api_key)
    pandas_ai = SmartDataframe(df, config={"llm": llm})
    result = pandas_ai.chat(prompt)
    return result

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Define users and hashed passwords for simplicity
users = {
    "pranav.baviskar": hash_password("pranav123")
}

TOKEN_FILE = "./data/token_counts_dataanalyst.json"

def read_token_counts():
    try:
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def write_token_counts(token_counts):
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_counts, f)

def get_token_count(username):
    token_counts = read_token_counts()
    return token_counts.get(username, 1000)  # Default to 1000 tokens if not found

def update_token_count(username, count):
    token_counts = read_token_counts()
    token_counts[username] = count
    write_token_counts(token_counts)

def login():
    col1, col2, col3 = st.columns([1, 1, 1])  # Create three columns with equal width
    with col2:  # Center the input fields in the middle column
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Sign in"):
            hashed_password = hash_password(password)
            if username in users and users[username] == hashed_password:
                token_counts = read_token_counts()
                tokens_remaining = token_counts.get(username, 500)  # Default to 500 tokens if not found
                
                if tokens_remaining > 0:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.tokens_remaining = tokens_remaining
                    st.session_state.tokens_consumed = 0
                    st.success("Logged in successfully!")
                    st.experimental_rerun()  # Refresh to show logged-in state
                else:
                    st.error("No tokens remaining. Please contact support.")
            else:
                st.error("Invalid username or password")
    # Add the footer section
    col4, col5, col6, col7, col8, col9 = st.columns([1, 1, 1, 1, 1, 1])
    st.markdown("")
    st.markdown("")
    with col7:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.write("**Design & Developed by:**")
    with col9:
        st.image("https://lh3.googleusercontent.com/drive-viewer/AKGpiha2TPFebW5deI-uoKPuD2Yoq_4xws137dj4LaFW3APyb_BkQ5NNKtwtH__KDr3E-_KbygMPh3D5VPqZPR5-ymj17acBxJgBLA=s2560", width=150)
    with col8:
        st.image("https://lh3.googleusercontent.com/drive-viewer/AKGpihZfq-IzkSSrziXqoQ8r0ypLiLPAQPW245Aq-NP6-90LEExUcBRM0L_mrr30zFXUzzN985zDpKWrcmptsWMF98vGmZjnfeEibg=s2560", width=150)

def logout():
    # Clear session state on logout
    st.session_state.logged_in = False
    del st.session_state.username
    del st.session_state.tokens_remaining
    del st.session_state.tokens_consumed
    st.success("Logged out successfully!")
    st.experimental_rerun()  # Refresh to show logged-out state

st.image("https://www.vgen.it/wp-content/uploads/2021/04/logo-accenture-ludo.png", width=150)
st.markdown("")
st.markdown("""
    <style>
        @keyframes gradientAnimation {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }

        .animated-gradient-text {
            font-family: "Graphik Black";
            font-size: 42px;
            background: linear-gradient(to right, #7953cd 20%, #00affa 30%, #0190cd 70%, #764ada 80%);
            background-size: 300% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradientAnimation 10s ease-in-out infinite;
        }
    </style>
    <p class="animated-gradient-text">
        DataViz: Your personal data analyst!
    </p>
""", unsafe_allow_html=True)

st.markdown('''<style>
    .stApp > header {
        background-color: transparent;
    }
    .stApp {    
        background: linear-gradient(45deg, #001f3f 55%, #007f7f 65%, #005f5f 80%);
        animation: my_animation 20s ease infinite;
        background-size: 200% 200%;
        background-attachment: fixed;
    }
    
    @keyframes my_animation {
        0% {background-position: 0% 0%;}
        80% {background-position: 80% 80%;}
    }
    
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #00bfbf 45%, #008f8f 70%);
        color: white;
        border: none;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(45deg, #00a9a9 45%, #007f7f 55%, #005f5f 70%);
    }
    
    div.stButton > button:active {
        position:relative;
        top:3px;
    }    
</style>''', unsafe_allow_html=True)

# Ensure session state variables are initialized
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "tokens_consumed" not in st.session_state:
    st.session_state.tokens_consumed = 0
if "tokens_remaining" not in st.session_state:
    st.session_state.tokens_remaining = 0
    
if st.session_state.logged_in:
    st.sidebar.write(f"Welcome, {st.session_state.username}")
    st.sidebar.write(f"Tokens remaining: {st.session_state.tokens_remaining}")
    if st.sidebar.button("Logout"):
        logout()
    input_csv = st.file_uploader("Upload your CSV file", type=['csv'])

    if input_csv is not None:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.info("CSV Uploaded Successfully")
            data = pd.read_csv(input_csv)
            st.dataframe(data, use_container_width=True)

        with col2:
            st.info("Chat Below")
            input_text = st.text_area("Enter your query")

            if input_text is not None:
                if st.button("Chat with CSV"):
                    st.info("Your Query: " + input_text)
                    result = chat_with_csv(data, input_text)
                    fig_number = plt.get_fignums()
                    if fig_number:
                        st.pyplot(plt.gcf())
                        st.write(result)
                    else:
                        st.write(result)
                        st.success("Success!!!")

else:
    login()
