import streamlit as st
import os
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain.chains import ConversationalRetrievalChain


def add_vertical_space(spaces=1):
    for _ in range(spaces):
        st.sidebar.markdown("---")

def main():
    st.set_page_config(page_title="DataWhiz 📊")
    st.title("DataWhiz Chatbot 📊💬")
    st.subheader("Your personal data analyst! 👨🏻‍💻")

    st.sidebar.title("DataWhiz")


    DB_FAISS_PATH = "vectorstore/db_faiss"
    TEMP_DIR = "temp"

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=['csv'])

    add_vertical_space(1)
    st.sidebar.write('Accenture S&C GN H&PS')

    if uploaded_file is not None:
        file_path = os.path.join(TEMP_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        st.write(f"Uploaded file: {uploaded_file.name}")
        st.write("Processing CSV file...")

        loader = CSVLoader(file_path=file_path, encoding="utf-8", csv_args={'delimiter': ','})
        data = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
        text_chunks = text_splitter.split_documents(data)

        st.write(f"Total text chunks: {len(text_chunks)}")
        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        docsearch = FAISS.from_documents(text_chunks, embeddings)
        docsearch.save_local(DB_FAISS_PATH)

        llm = CTransformers(model="C:/Users/pranav.baviskar/Desktop/Learning/GenAI/Datawhiz/models/llama-2-7b-chat.ggmlv3.q4_0.bin",
                            model_type="llama",
                            max_new_tokens=512,
                            temperature=0.1)

        qa = ConversationalRetrievalChain.from_llm(llm, retriever=docsearch.as_retriever())

        st.write("Enter your query:")
        query = st.text_input("Input Prompt:")
        if query:
            with st.spinner("Processing your question..."):
                chat_history = []
                result = qa({"question": query, "chat_history": chat_history})
                st.write("Response:", result['answer'])

        os.remove(file_path)

if __name__ == "__main__":
    main()
