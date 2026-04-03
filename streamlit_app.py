import streamlit as st
import requests

# HuggingFace free model API
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

st.set_page_config(page_title="AI Student Chatbot")

st.title("🎓 Free AI Student Chatbot")
st.write("Ask questions about Machine Learning, Python, or assignments.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
prompt = st.chat_input("Ask your question")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    # Send request to model
    payload = {"inputs": prompt}

    response = requests.post(API_URL, json=payload)

    try:
        answer = response.json()[0]["generated_text"]
    except:
        answer = "Model is loading. Please try again in a few seconds."

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
