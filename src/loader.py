import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_pdfs(folder_path="./data", chunk_size=1000, chunk_overlap=200):
    all_docs = []
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n", "\n\n", ".", "?", "!", " "],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            loader = PyMuPDFLoader(file_path)
            docs = loader.load()
            chunks = splitter.split_documents(docs)
            all_docs.extend(chunks)
    return all_docs
