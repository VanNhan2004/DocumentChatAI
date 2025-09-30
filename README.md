# 📄 AI-Powered Document ChatBot

## 🌟 Overview
This project is an **AI-powered chatbot** that allows users to query information directly from their own documents.  
By uploading files such as **PDF, DOCX, or CSV**, the system processes and indexes the content into a **vector database**.  
Users can then ask questions in natural language, and the chatbot retrieves the most relevant context to generate accurate answers.

---

## 🚀 Features
- 📂 Support for multiple document formats: **PDF, DOCX, CSV**  
- 🔍 Text preprocessing and splitting for better retrieval  
- 🧠 Embedding generation with **HuggingFace models**  
- 📊 Vector storage and similarity search using **FAISS**  
- 💬 Natural language question answering powered by **ChatOllama (LLM)**  
- ⚡ Modular and extensible architecture  

---

## 🛠️ Tech Stack

| Component        | Technology Used |
|------------------|-----------------|
| Embeddings       | HuggingFace Transformers |
| Vector Database  | FAISS |
| Orchestration    | LangChain |
| File Parsing     | PyPDF2, Pandas, python-docx |
| LLM Backend      | ChatOllama / Ollama |

---

## 📂 Project Structure
```
ChatBot/
│── main.py                # Main entry point
│── README.md              # Documentation
│── setup.txt              # Setup instructions
│── data/                  # Example documents
│   ├── data.pdf
│   ├── data.docx
│   └── toyota.csv
│── src/                   # Source code
│   ├── chatbot.py         # Chatbot pipeline
│   ├── config.py          # Configurations
│   ├── data_loader.py     # File parsing & preprocessing
│   ├── prompt.py          # Prompt templates
│   └── vector_store.py    # FAISS storage & retrieval
│── vector_db/             # Vector index (FAISS + pickle)
```

---

## ⚙️ Installation

### 1. Clone the repository
```bash
github
```

### 2. Create a virtual environment
```bash
python -m venv venv
# Activate it
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate    # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing:
```bash
pip install langchain langchain-community langchain-huggingface faiss-cpu PyPDF2 pandas python-docx
```

### 4. (Optional) Install Ollama
For running **ChatOllama**, follow the [Ollama installation guide](https://ollama.ai).

---

## ▶️ Usage

Run the chatbot:
```bash
python main.py
```

Steps:
1. Load or index your documents (`.pdf`, `.docx`, `.csv`).  
2. Ask questions in natural language.  
3. The chatbot will retrieve and generate context-aware answers.  

---

## 🔮 Roadmap
- [ ] Support for Excel files (`.xlsx`)  
- [ ] Add OCR for scanned documents  
- [ ] Advanced analytics for CSV data  
- [ ] Docker deployment for easier distribution  
- [ ] Fine-tuned LLM for specialized domains  

---

## 📜 License
This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute it.

---

## 👨‍💻 Author
Developed by **Nguyen Van Nhan**  
🎓 Student ID: 2200002045  
🏫 Nguyen Tat Thanh University
