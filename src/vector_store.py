# src/vector_store.py

import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from src.config import EMBEDDING_MODEL, VECTOR_DB_FOLDER

def build_vector_store_from_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n", ".", "?", "!", " "],
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    chunks = splitter.split_text(text)
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vector_store = FAISS.from_texts(chunks, embeddings)

    os.makedirs(VECTOR_DB_FOLDER, exist_ok=True)
    vector_store.save_local(VECTOR_DB_FOLDER)
    return vector_store

def load_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return FAISS.load_local(VECTOR_DB_FOLDER, embeddings, allow_dangerous_deserialization=True)
