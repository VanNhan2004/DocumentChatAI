import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# -------- Load PDF, split text --------
def load_pdfs(folder_path):
    all_text = ""
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            reader = PdfReader(os.path.join(folder_path, file))
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    all_text += page_text + "\n"
    return all_text

pdf_folder = "./data"
documents_text = load_pdfs(pdf_folder)

text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n","\n\n", ".", "?", "!", " "],
    chunk_size=1000,
    chunk_overlap=150,
    length_function=len
)
docs = text_splitter.create_documents([documents_text])

# -------- Embeddings & vectorstore --------
embedding_model = OllamaEmbeddings(model="llama3.2")
vectorstore = FAISS.from_documents(docs, embedding_model)

# -------- LLM --------
llm = ChatOllama(model="llama3.2")

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# -------- Prompt cho chatbot --------
prompt = ChatPromptTemplate.from_template("""
Bạn là một chatbot hỗ trợ khách hàng, thân thiện, nói ngắn gọn và dễ hiểu.
Chỉ sử dụng dữ liệu dưới đây để trả lời, không tự bịa thông tin.
Nếu không tìm thấy câu trả lời trong dữ liệu, hãy trả lời chính xác: "Xin lỗi, tôi không có dữ liệu về vấn đề này."

Dữ liệu:
{context}

Câu hỏi: {question}
Trả lời:
""")

qa_chain = LLMChain(llm=llm, prompt=prompt)

# -------- Hàm hỏi đáp --------
def ask(question):
    docs = retriever.invoke(question)
    context = "\n\n".join([d.page_content for d in docs])
    result = qa_chain.invoke({"context": context, "question": question})
    return result["text"]

# -------- Chat console --------
print("Chatbot LLaMA + RAG đã sẵn sàng! Nhập 'exit' để thoát.")
while True:
    question = input("Bạn: ")
    if question.lower() in ["exit", "quit"]:
        break
    answer = ask(question)
    print("Bot:", answer)
