import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
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
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# Tạo mới và lưu
vectorstore = FAISS.from_documents(docs, embedding_model)

# -------- LLM --------
llm = ChatOllama(model="llama3.2")

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# -------- Prompt cho chatbot --------
prompt = ChatPromptTemplate.from_template("""
Bạn là chatbot hỏi đáp về pháp luật Việt Nam. 
Yêu cầu:
- Trả lời ngắn gọn, rõ ràng, dễ hiểu.
- Nếu câu hỏi liên quan đến mức xử phạt, hãy trích chính xác số tiền và hành vi tương ứng.
- Tuyệt đối chỉ dựa vào dữ liệu trong phần CONTEXT bên dưới.
- Không được tự suy đoán, không được bịa thông tin.
- Nếu không có câu trả lời trong dữ liệu, hãy trả lời chính xác: 
  "Xin lỗi, tôi không có dữ liệu về vấn đề này."
- Nếu câu hỏi không liên quan đến pháp luật Việt Nam, hãy trả lời: 
  "Tôi xin lỗi, nhưng câu hỏi của bạn không liên quan đến thông tin về pháp luật Việt Nam. Tôi không thể trả lời câu hỏi này."

CONTEXT:
{context}

CÂU HỎI: {question}

TRẢ LỜI:
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