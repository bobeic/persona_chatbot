from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from enum import Enum
import streamlit as st
from PyPDF2 import PdfReader
from io import StringIO
import pickle
import os

# setup doc_type enum
DocType = Enum("DocType", ["text/csv", "youtube", "pdf"])

store_path = "faiss_store_persona.pk1"


def load_vector_store():
    with open(store_path, "rb") as f:
        db = pickle.load(f)

    st.success("Successfully loaded store")
    st.session_state.db = db

    return db

def load_page():
    embeddings = OpenAIEmbeddings(openai_api_key=st.session_state.api_key)

    # streamlit website
    st.title("Add docs")

    current_type = st.selectbox("type", [doc.name for doc in DocType])

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
        length_function=len,
    )

    texts_list = []
    docs_list = []

    if current_type == "text/csv":
        file = st.file_uploader("Upload text file here")
        if file:
            stringio = StringIO(file.getvalue().decode("utf-8"))

            texts = text_splitter.split_text(stringio.read())
            st.success("Loaded file")
            texts_list += texts

    elif current_type == "youtube":
        url = st.text_input("Youtube url")
        if url:
            loader = YoutubeLoader.from_youtube_url(url)
            transcript = loader.load()
            docs = text_splitter.split_documents(transcript)
            st.success("Loaded file")
            docs_list += docs

    elif current_type == "pdf":
        pdf = st.file_uploader("Upload pdf file here", type="pdf")
        if pdf:
            pdf_reader = PdfReader(pdf)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            texts = text_splitter.split_text(text)
            st.success("Loaded file")
            texts_list += texts

    else:
        raise Exception("Not a valid form of document")

    col1, col2, _ = st.columns([1, 1, 3])

    with col1:
        if st.button("Submit docs"):
            if docs_list and texts_list:
                db = FAISS.from_documents(docs_list, embeddings)
                db1 = FAISS.from_texts(texts_list, embeddings)
                db.merge_from(db1)
                st.success("Documents submitted successfully")

            elif docs_list:
                db = FAISS.from_documents(docs_list, embeddings)
                st.success("Documents submitted successfully")

            elif texts_list:
                db = FAISS.from_texts(texts_list, embeddings)
                st.success("Documents submitted successfully")

            else:
                st.error("No docs submitted")

            with open(store_path, "wb") as f:
                pickle.dump(db, f)

            # st.write("successfully stored docs")

            st.session_state.db = db

            # if "db" not in st.session_state.keys():
            #     st.write("No db stored")
            # else:
            #     st.write("db stored")

    with col2:
        if os.path.isfile(store_path):
            st.button("Load docs", on_click=load_vector_store)



if "api_key" not in st.session_state.keys():
    st.error("No api key")
else:
    load_page()