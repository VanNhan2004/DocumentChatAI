# 📘 Chatbot LLaMA + RAG with FAISS

## 🚀 Introduction  
This project builds a customer support chatbot using **Retrieval-Augmented Generation (RAG)** combined with **LLaMA (Ollama)** to answer questions based on PDF documents.  

Instead of relying solely on the model's general knowledge, the chatbot searches for relevant information in PDF files (knowledge base) and only uses that data to generate responses. This helps reduce **hallucination** (fabricated answers).  

---

## ⚙️ Features  
- Read and process multiple **PDF** files from the `./data` folder.  
- Split text into smaller chunks using **RecursiveCharacterTextSplitter** for better embedding.  
- Create **vector embeddings** from documents with `OllamaEmbeddings`.  
- Store embeddings in **FAISS vectorstore** for fast retrieval.  
- Integrate **LLaMA (Ollama)** as the LLM backend.  
- The chatbot answers **only based on the provided documents**. If no relevant answer is found, it will respond with:  
  ```
  Sorry, I don't have data on this topic.
  ```  
- Chat directly in the terminal/console.  

---

## 📂 Project Structure  

```
📦 chatbot-rag-llama
 ┣ 📂 data/               # Folder containing PDF files
 ┣ 📜 main.py          # Main chatbot code
 ┣ 📜 README.md           # Project documentation
```

---

## 🛠 Installation  

### 1. Python and dependencies  
Install the required libraries:  

```bash
pip install PyPDF2 langchain langchain-community langchain-ollama faiss-cpu
```

### 2. Ollama + LLaMA  
- Download and install **Ollama**: [https://ollama.ai](https://ollama.ai)  
- Pull the LLaMA model (e.g., llama3.2):  

```bash
ollama pull llama3.2
```

---

## ▶️ Usage  

1. Place your PDF files into the `./data` folder.  
2. Run the chatbot:  

```bash
python chatbot.py
```

3. The console interface will appear:  

```
Chatbot LLaMA + RAG is ready! Type 'exit' to quit.
You:
```

4. Ask questions, for example:  

```
You: When was Company X founded?
Bot: Company X was founded in 2005.
```

---

## 🔍 Example  

- If data exists in the PDF:  
  ```
  You: Who is the director of the company?
  Bot: The company director is John Doe.
  ```

- If **no relevant data** exists in the PDF:  
  ```
  You: Who is Lionel Messi?
  Bot: Sorry, I don't have data on this topic.
  ```

---

## 🌱 Future Improvements  
- Add support for **DOCX, TXT, CSV** files.  
- Build a **web interface (Streamlit/Gradio)** instead of console-based chat.  
- Save and display **chat history**.  
- Optimize **vectorstore** for larger datasets.  
