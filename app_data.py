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

api_key = st.secrets['GEMINI_API_KEY']


def chat_with_csv(df,prompt):
    llm = GooglePalm(api_key=api_key)
    pandas_ai = SmartDataframe(df, config={"llm": llm})
    #pandas_ai = PandasAI(llm, save_charts=True)
    result = pandas_ai.chat(prompt)
    return result

st.set_page_config(page_title="DataViz     ", layout='wide')
background_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mathematical Symbols Background</title>
    <style>
        body {
            margin: 0;
            overflow: hidden;
            background: (45deg, #FFFFFF 55%, #FAE9D3 65%, #efb7bf 80%);
        }
        canvas {
            display: block;
        }
    </style>
</head>
<body>
    <canvas id="symbolfield"></canvas>
    <script>
        const canvas = document.getElementById('symbolfield');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const symbols = ['α', 'β', 'γ', 'δ', 'ζ', 'θ', 'λ', 'μ', 'π', 'σ', 'τ', 'φ', 'ω', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
        const numSymbols = 100;
        const glowDuration = 1000; // Glow duration in milliseconds

        let symbolObjects = [];

        function initializeSymbols() {
            for (let i = 0; i < numSymbols; i++) {
                symbolObjects.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    symbol: symbols[Math.floor(Math.random() * symbols.length)],
                    fontSize: Math.random() * 20 + 4, // Random font size between 10 and 40
                    speedX: Math.random() * 0.5 - 0.25,
                    speedY: Math.random() * 0.5 - 0.25,
                    glow: false,
                    glowStart: 0
                });
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            for (let i = 0; i < numSymbols; i++) {
                let symbolObj = symbolObjects[i];

                // Calculate glow intensity based on time elapsed since glow started
                let glowIntensity = 0;
                if (symbolObj.glow) {
                    let elapsedTime = Date.now() - symbolObj.glowStart;
                    glowIntensity = 0.8 * (1 - elapsedTime / glowDuration); // Decreasing glow intensity over time
                    if (elapsedTime >= glowDuration) {
                        symbolObj.glow = false; // Reset glow state after glow duration
                    }
                }

                ctx.font = `${symbolObj.fontSize}px Arial`;

                // Set glow effect if symbol should glow
                if (glowIntensity > 0) {
                    ctx.shadowColor = 'rgba(255, 255, 255, 0.8)';
                    ctx.shadowBlur = 20 * glowIntensity;
                } else {
                    ctx.shadowColor = 'transparent';
                    ctx.shadowBlur = 0;
                }

                ctx.fillStyle = 'rgba(255, 255, 255, 0.1)'; // Adjusted transparency to 80%
                ctx.fillText(symbolObj.symbol, symbolObj.x, symbolObj.y);

                symbolObj.x += symbolObj.speedX;
                symbolObj.y += symbolObj.speedY;

                if (symbolObj.x < -20) {
                    symbolObj.x = canvas.width + 20;
                }
                if (symbolObj.x > canvas.width + 20) {
                    symbolObj.x = -20;
                }
                if (symbolObj.y < -20) {
                    symbolObj.y = canvas.height + 20;
                }
                if (symbolObj.y > canvas.height + 20) {
                    symbolObj.y = -20;
                }
            }

            requestAnimationFrame(draw);
        }

        initializeSymbols();
        draw();

        window.addEventListener('resize', function() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            initializeSymbols();
        });

        canvas.addEventListener('mousemove', function(event) {
            let mouseX = event.clientX;
            let mouseY = event.clientY;
            for (let i = 0; i < numSymbols; i++) {
                let symbolObj = symbolObjects[i];
                let dx = mouseX - symbolObj.x;
                let dy = mouseY - symbolObj.y;
                let distance = Math.sqrt(dx * dx + dy * dy);
                if (distance < 50) {
                    symbolObj.speedX = dx * 0.01;
                    symbolObj.speedY = dy * 0.01;
                    if (!symbolObj.glow) {
                        symbolObj.glow = true;
                        symbolObj.glowStart = Date.now();
                    }
                }
            }
        });
    </script>
</body>
</html>
"""

# Embed the HTML code into the Streamlit app
st.components.v1.html(background_html, height=800)

st.components.v1.html(background_html, height=1000)
st.markdown("""
<style>
    iframe {
        position: fixed;
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;
        border: none;
        height: 100%;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


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
        background: linear-gradient(45deg, #FFFFFF 55%, #FAE9D3 65%, #efb7bf 80%);
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
        background:linear-gradient(45deg, #E95C85 45%, #C853AC 70%);
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
