from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
import os

VECTOR_DB_PATH = "./vector_db/faiss_index"  

def create_vectorstore(documents, save=True):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(documents, embedding_model)
    
    if save:
        os.makedirs(VECTOR_DB_PATH, exist_ok=True)
        vectorstore.save_local(VECTOR_DB_PATH)
        print(f"Vectorstore đã được lưu tại {VECTOR_DB_PATH}")
    return vectorstore

def load_vectorstore():
    if not os.path.exists(VECTOR_DB_PATH):
        raise FileNotFoundError(f"Không tìm thấy vectorstore tại {VECTOR_DB_PATH}")

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(VECTOR_DB_PATH, embedding_model, allow_dangerous_deserialization=True)
    print(f"Đã load vectorstore từ {VECTOR_DB_PATH}")
    return vectorstore


def get_hybrid_retriever(vectorstore, faiss_k=3, bm25_k=3):
    retriever_faiss = vectorstore.as_retriever(search_kwargs={"k": faiss_k})
    top_docs = vectorstore.similarity_search("", k=100)
    retriever_bm25 = BM25Retriever.from_documents(top_docs)
    retriever_bm25.k = bm25_k

    return EnsembleRetriever(
        retrievers=[retriever_faiss, retriever_bm25],
        weights=[0.7, 0.3]
    )
