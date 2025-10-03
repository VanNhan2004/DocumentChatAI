from langchain_ollama import ChatOllama

def init_llm(model_name="llama3.2"):
    return ChatOllama(model=model_name)

def qa_chain(llm, prompt):
    return llm | prompt
