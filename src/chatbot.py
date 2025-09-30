# src/chatbot.py

from langchain_ollama import ChatOllama
from langchain.chains import RetrievalQA
from src.config import LLM_MODEL, TOP_K
from src.prompt import get_custom_prompt

def create_qa_chain(vector_store):
    """Khởi tạo RetrievalQA với LLM Ollama + custom prompt."""
    llm = ChatOllama(model=LLM_MODEL, temperature=0, max_tokens=512)
    retriever = vector_store.as_retriever(search_kwargs={"k": TOP_K})

    prompt = get_custom_prompt()
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )
    return qa
