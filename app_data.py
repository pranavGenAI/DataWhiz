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

st.set_page_config(page_title="DataViz     ", layout='wide')
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Accenture_logo.svg/1200px-Accenture_logo.svg.png", width=150)
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
        background: linear-gradient(45deg, #FFFFFF 60%, #FAE9D3 40%, #e7abb4 30%);
        animation: my_animation 20s ease infinite;
        background-size: 200% 200%;
        background-attachment: fixed;
    }
    
    
    
    @keyframes my_animation {
        0% {background-position: 0% 0%;}
        80% {background-position: 80% 80%;}
    
    }
    
    [data-testid=stAlert] {
        background: linear-gradient(180deg, #ffffff 45%, #ffffff 55%, #ffffff 70%);
        color: black;
    }
    
    div.stButton > button:first-child {
        background:linear-gradient(45deg, #c9024b 45%, #ba0158 55%, #cd006d 70%);
        color: white;
        border: none;
    }
    div.stButton > button:hover {
        background:linear-gradient(45deg, #ce026f 45%, #970e79 55%, #6c028d 70%);
        background-color:#ce1126;
    }
    div.stButton > button:active {
        position:relative;
        top:3px;
    }    
    

    </style>''', unsafe_allow_html=True)


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
