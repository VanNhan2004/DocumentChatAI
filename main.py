# src/main.py

import os
from src.config import DATA_FOLDER, VECTOR_DB_FOLDER
from src.data_loader import load_files
from src.vector_store import build_vector_store_from_text, load_vector_store
from src.chatbot import create_qa_chain

def main():
    # 1. Kiểm tra dữ liệu PDF
    if not os.path.exists(DATA_FOLDER):
        print(f"⚠️ Không tìm thấy thư mục {DATA_FOLDER}/. Hãy đặt file PDF vào đó.")
        return

    # 2. Tạo hoặc load FAISS index
    if not os.path.exists(VECTOR_DB_FOLDER) or not os.listdir(VECTOR_DB_FOLDER):
        print("⚙️ Chưa có FAISS index, đang tạo mới...")
        text = load_files(DATA_FOLDER)
        if not text:
            print("⚠️ Không có dữ liệu để build index.")
            return
        vector_store = build_vector_store_from_text(text)
    else:
        print("📂 Đang load FAISS index từ vector_db/...")
        vector_store = load_vector_store()

    # 3. Tạo chatbot chain
    qa = create_qa_chain(vector_store)

    print("✅ Chatbot sẵn sàng! Gõ 'exit' để thoát.\n")
    while True:
        q = input("💬 Câu hỏi: ").strip()
        if q.lower() in ("exit", "quit", "q"):
            break
        if not q:
            continue

        result = qa.invoke({"query": q})
        answer = result.get("result") or result.get("answer") or result.get("output_text") or str(result)
        print("🤖 Trả lời:", answer.strip(), "\n")

if __name__ == "__main__":
    main()
