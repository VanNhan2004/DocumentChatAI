import streamlit as st
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

from src.loader import load_pdfs
from src.vectorstore import create_vectorstore, load_vectorstore, get_hybrid_retriever
from src.prompts import get_chat_prompt
from src.llm_model import init_llm
from src.chatbot import ask_question

# ---------------- Setup trang ----------------
def setup_page():
    st.set_page_config(
        page_title="ChatBot_NVN",
        layout="wide"
    )

def initialize_app():
    setup_page()

# ---------------- Giao diện Chat ----------------
def setup_chat_interface(model_name="NVN-ChatBot"):
    st.title("Chat-NVN")
    st.caption(f"Trợ lý AI được hỗ trợ bởi {model_name}")

    # Khởi tạo lịch sử chat
    msgs = StreamlitChatMessageHistory(key="langchain_messages")
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Xin chào! Tôi có thể giúp gì cho bạn hôm nay?", "related_docs": None}
        ]
        msgs.add_ai_message("Xin chào! Tôi có thể giúp gì cho bạn hôm nay?")

    # Hiển thị lịch sử chat
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            col1, col2 = st.columns([3, 1])
            with col1:
                st.chat_message("assistant").write(msg["content"])
                if msg.get("related_docs"):
                    with st.expander("Thông tin liên quan"):
                        for i, doc in enumerate(msg["related_docs"], 1):
                            st.markdown(f"**Đoạn {i}:**")
                            st.write(doc.page_content.strip())
                            st.divider()
        else:
            col1, col2 = st.columns([1, 3])
            with col2:
                st.chat_message("human").write(msg["content"])

    return msgs

# ---------------- Xử lý tin nhắn người dùng ----------------
def handle_user_input(msgs, retriever, llm, prompt_template):
    if user_input := st.chat_input("Hãy nhập câu hỏi của bạn:"):
        # Hiển thị user message
        st.session_state.messages.append({"role": "human", "content": user_input, "related_docs": None})
        col1, col2 = st.columns([1, 3])
        with col2:
            st.chat_message("human").write(user_input)
        msgs.add_user_message(user_input)

        # Hiển thị bot đang suy nghĩ
        with st.spinner("Thinking...."):
            st_callback = StreamlitCallbackHandler(st.container())

            chat_history = [
                    {"role": msg["role"], "content": msg["content"]}
                    for msg in st.session_state.messages[:-1]
                    ]

            # Lấy dữ liệu liên quan
            related_docs = retriever.get_relevant_documents(user_input)

            # Gọi model
            answer = ask_question(retriever, user_input, llm, prompt_template)

        # Hiển thị câu trả lời và thông tin liên quan
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "related_docs": related_docs
        })
        col1, col2 = st.columns([3, 1])
        with col1:
            st.chat_message("assistant").write(answer)
            if related_docs:
                with st.expander("Thông tin liên quan"):
                    for i, doc in enumerate(related_docs, 1):
                        st.markdown(f"**Đoạn {i}:**")
                        st.write(doc.page_content.strip())
                        st.divider()

        msgs.add_ai_message(answer)

# ---------------- Main ----------------
def main():
    initialize_app()

    # Giao diện chat
    msgs = setup_chat_interface()

    # Load hoặc tạo vectorstore
    try:
        vectorstore = load_vectorstore()
    except FileNotFoundError:
        st.info("Chưa có vectorstore, đang tạo mới.....")
        documents = load_pdfs("./data")
        if not documents:
            st.warning("Chưa có dữ liệu, vui lòng thêm dữ liệu để ChatBot hoạt động.")
            return
        vectorstore = create_vectorstore(documents)

    retriever = get_hybrid_retriever(vectorstore)

    # Khởi tạo LLM và prompt
    llm = init_llm()
    prompt_template = get_chat_prompt()

    # Xử lý chat
    handle_user_input(msgs, retriever, llm, prompt_template)

if __name__ == "__main__":
    main()