import streamlit as st 
from pandasai.llm import GooglePalm
import os
import pandas as pd
from pandasai import SmartDataframe
#from pandasai import PandasAI
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

api_key = st.secrets['GEMINI_API_KEY']


def chat_with_csv(df,prompt):
    llm = GooglePalm(api_key=api_key)
    pandas_ai = SmartDataframe(df, config={"llm": llm})
    #pandas_ai = PandasAI(llm, save_charts=True)
    result = pandas_ai.chat(prompt)
    return result

st.set_page_config(layout='wide')

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
            background: linear-gradient(45deg, rgb(245, 58, 126) 30%, rgb(200, 1, 200) 55%, rgb(197, 45, 243) 20%);
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
                    fig_number = plt.get_fignums()
                    if fig_number:
                        st.pyplot(plt.gcf())
                        st.write(result)
                    else:
                        st.write(result)
                        st.success("Success!!!")
