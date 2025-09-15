import streamlit as st
from openai import OpenAI
import os

# Streamlit Page Config
st.set_page_config(page_title="Student Career Guidance AI", page_icon="🎓", layout="centered")

# Custom CSS for professional UI
st.markdown("""
    <style>
        body { background-color: #f4f6fa; }
        .main-title { text-align: center; font-size: 36px; font-weight: bold; color: #2C3E50; margin-bottom: 20px; }
        .subtitle { text-align: center; font-size: 18px; color: #7f8c8d; margin-bottom: 30px; }
        .chat-bubble-user { background-color: #3498db; color: white; padding: 10px 15px; border-radius: 15px; margin: 5px 0; max-width: 70%; margin-left: auto; }
        .chat-bubble-ai { background-color: #ecf0f1; color: #2C3E50; padding: 10px 15px; border-radius: 15px; margin: 5px 0; max-width: 70%; margin-right: auto; }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='main-title'>🎓 Student Career Guidance AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Upload a text file and ask questions about its content</div>", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Future Scope")
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

# File uploader
uploaded_file = st.file_uploader("Upload a text file (.txt)", type=["txt"])
file_content = ""
if uploaded_file:
    file_content = uploaded_file.read().decode("utf-8")
    st.info("File uploaded successfully! You can now ask questions about this file.")

# Initialize session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a professional career counselor. You can also analyze uploaded text files and answer questions about them."}
    ]

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'>{msg['content']}</div>", unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f"<div class='chat-bubble-ai'>{msg['content']}</div>", unsafe_allow_html=True)

# Chat input
if user_input := st.chat_input("Type your question here..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f"<div class='chat-bubble-user'>{user_input}</div>", unsafe_allow_html=True)

    if api_key:
        try:
            client = OpenAI(api_key=api_key)
            
            # Include file content in context if uploaded
            context_messages = st.session_state.messages.copy()
            if file_content:
                context_messages.append({"role": "system", "content": f"File content:\n{file_content}"})

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=context_messages
            )
            reply = response.choices[0].message.content

            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.markdown(f"<div class='chat-bubble-ai'>{reply}</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("Please add your API key in the sidebar to start chatting.")
