import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(page_title="AI Student Chatbot", page_icon="🤖")

st.title("🤖 AI Chatbot for Students")
st.write("Ask questions about Machine Learning, Python, or assignments.")

# Initialize Groq API
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("❌ GROQ_API_KEY not found. Add it in Streamlit Secrets.")
    st.stop()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
prompt = st.chat_input("Ask your question")

if prompt:

    with st.chat_message("user"):
        st.write(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an AI tutor helping engineering students understand Machine Learning and Python."}
            ] + st.session_state.messages
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = f"⚠️ Error: {e}"

    with st.chat_message("assistant"):
        st.write(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })
