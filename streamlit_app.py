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
    st.error("❌ GROQ_API_KEY not found. Please add it in Streamlit Secrets.")
    st.stop()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
prompt = st.chat_input("Ask your question")

if prompt:

    # Show user message
    with st.chat_message("user"):
        st.write(prompt)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are an AI tutor helping engineering students understand Machine Learning and Python."}
            ] + st.session_state.messages
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = f"⚠️ Error: {e}"

    # Show AI response
    with st.chat_message("assistant"):
        st.write(reply)

    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })
