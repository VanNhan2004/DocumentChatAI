# 🤖 NVN-ChatBot — Chatbot Hỏi Đáp Dựa Trên Tài Liệu PDF

Dự án này xây dựng một **chatbot AI** có khả năng **trả lời câu hỏi dựa trên dữ liệu văn bản hoặc tài liệu PDF**, sử dụng **LangChain**, **FAISS**, và **Ollama LLM (Llama3.2)**.  
Ứng dụng được triển khai với **Streamlit**, giúp bạn có thể trò chuyện trực tiếp qua giao diện web.

---

## 🧠 **Chức năng chính**
- ✅ Đọc và xử lý nhiều tệp **PDF** trong thư mục `data/`.
- ✅ Tự động chia nhỏ tài liệu thành **đoạn (chunk)** để tối ưu tìm kiếm ngữ nghĩa.
- ✅ Tạo và lưu trữ **vector database** (FAISS) cho việc truy xuất dữ liệu nhanh.
- ✅ Tích hợp **retriever kết hợp (FAISS + BM25)** để cải thiện độ chính xác.
- ✅ Chatbot sử dụng **LLM (Ollama - Llama3.2)** để sinh phản hồi tự nhiên.
- ✅ Giao diện thân thiện bằng **Streamlit**, hỗ trợ hiển thị đoạn văn bản liên quan.

---

## 🏗️ **Cấu trúc thư mục**
```
📦 NVN-ChatBot
├── 📂 data/                     # Chứa các file PDF dữ liệu gốc
│   └── ...
├── 📂 vector_db/                # Lưu trữ FAISS index (tự động tạo)
├── 📂 src/
│   ├── chatbot.py               # Hàm xử lý câu hỏi và phản hồi
│   ├── llm_model.py             # Khởi tạo mô hình ngôn ngữ (Ollama)
│   ├── loader.py                # Load và chia nhỏ dữ liệu PDF
│   ├── prompts.py               # Định nghĩa PromptTemplate cho chatbot
│   └── vectorstore.py           # Tạo / load / kết hợp retriever (FAISS + BM25)
├── main.py                      # File chính chạy ứng dụng Streamlit
├── requirements.txt             # Danh sách thư viện cần cài đặt
└── README.md                    # Tài liệu hướng dẫn (file này)
```

---

## ⚙️ **Cài đặt môi trường**

### 1️⃣ Clone dự án và vào thư mục:
```bash
git clone https://github.com/<your_username>/NVN-ChatBot.git
cd NVN-ChatBot
```

### 2️⃣ Tạo môi trường ảo (khuyến nghị):
```bash
python -m venv venv
source venv/Scripts/activate      # Windows
# hoặc
source venv/bin/activate          # macOS/Linux
```

### 3️⃣ Cài đặt các thư viện cần thiết:
Tạo file `requirements.txt` với nội dung sau:
```text
streamlit
langchain
langchain-community
langchain-huggingface
faiss-cpu
PyMuPDF
sentence-transformers
ollama
```

Sau đó chạy:
```bash
pip install -r requirements.txt
```

---

## 🧩 **Chuẩn bị dữ liệu**
1. Tạo thư mục `data/` trong dự án.
2. Đặt các file `.pdf` chứa nội dung luật, tài liệu hoặc văn bản bạn muốn chatbot sử dụng.
3. Khi chạy lần đầu, chatbot sẽ tự động xử lý PDF và tạo **FAISS index** trong `vector_db/`.

---

## 🚀 **Chạy ứng dụng**
```bash
streamlit run main.py
```

- Ứng dụng sẽ mở trên trình duyệt tại địa chỉ:
  ```
  http://localhost:8501
  ```

---

## 💬 **Cách hoạt động**
1. Khi bạn nhập câu hỏi, chatbot sẽ:
   - Lấy các đoạn văn bản liên quan từ FAISS + BM25 retriever.
   - Đưa các đoạn đó vào prompt.
   - Gửi prompt đến LLM (Ollama - Llama3.2).
   - Trả về câu trả lời chính xác và ngắn gọn.
2. Bạn có thể mở phần **"Thông tin liên quan"** để xem đoạn văn bản gốc.

---

## 🧩 **Chi tiết các module chính**

| File | Chức năng |
|------|------------|
| `chatbot.py` | Hàm `ask_question()` xử lý câu hỏi người dùng, kết hợp tài liệu và prompt để tạo phản hồi. |
| `llm_model.py` | Khởi tạo mô hình Ollama (Llama3.2) và chain QA. |
| `loader.py` | Tải và chia nhỏ dữ liệu PDF thành các đoạn văn bản có kích thước phù hợp. |
| `prompts.py` | Prompt template cho chatbot NVN (chống bịa đặt, trả lời tự nhiên). |
| `vectorstore.py` | Xử lý embedding, tạo FAISS index, và kết hợp retriever FAISS + BM25. |
| `main.py` | Ứng dụng Streamlit chính: giao diện chat, hiển thị phản hồi và tài liệu liên quan. |

---

## 🧠 **Mô hình sử dụng**
- **LLM:** Ollama (`llama3.2`)  
- **Embedding:** Sentence Transformers (`all-MiniLM-L6-v2`)  
- **Vector Database:** FAISS  
- **Retriever kết hợp:** FAISS (semantic) + BM25 (lexical)

---

## 📄 **Ghi chú thêm**
- Nếu chưa cài **Ollama**, tải tại [https://ollama.ai](https://ollama.ai)
- Chạy mô hình trước khi mở ứng dụng:
  ```bash
  ollama run llama3.2
  ```
- Khi muốn cập nhật dữ liệu, chỉ cần xóa thư mục `vector_db/` và chạy lại ứng dụng.

---
