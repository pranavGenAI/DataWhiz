import streamlit as st 
from pandasai.llm import GooglePalm
import os
import pandas as pd
from pandasai import SmartDataframe
from pandasai import PandasAI

api_key = st.secrets['GEMINI_API_KEY']


def chat_with_csv(df,prompt):
    llm = GooglePalm(api_key=api_key)
    pandas_ai = PandasAI(llm)
    result = pandas_ai.run(df, prompt=prompt)
    print(result)
    return result

st.set_page_config(page_title="DataViz Analyst Chatbot 📊💬", layout='wide')

st.title("DataViz Chatbot 📊💬")
st.markdown('<style>h1{color: orange; text-align: center;}</style>', unsafe_allow_html=True)
st.subheader('Your personal data analyst for data visualization! 👨🏻‍💻')
st.markdown('<style>h3{color: Orange;  text-align: center;}</style>', unsafe_allow_html=True)

input_csv = st.file_uploader("Upload your CSV file", type=['csv'])

if input_csv is not None:

        col1, col2 = st.columns([1,1])

        with col1:
            st.info("CSV Uploaded Successfully")
            data = pd.read_csv(input_csv)
            st.dataframe(data, use_container_width=True)

        with col2:

            st.info("Chat Below")
            
            input_text = st.text_area("Enter your query")

            if input_text is not None:
                if st.button("Chat with CSV"):
                    st.info("Your Query: "+input_text)
                    result = chat_with_csv(data, input_text)
                    st.success(result)
