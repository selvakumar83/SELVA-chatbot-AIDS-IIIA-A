import streamlit as st
from groq import Groq

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="AI Student Chatbot")

st.title("🎓 AI Student Chatbot")

st.write("Ask questions about Machine Learning, Python, or assignments.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
prompt = st.chat_input("Ask your question")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.write(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
