import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# Page configuration
st.set_page_config(
    page_title="AI Department Assistant",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Department Assistant")
st.markdown("Ask questions about **Machine Learning, Python, Coding, or Assignments**")

# Sidebar information
with st.sidebar:
    st.header("About")
    st.write("""
    This AI assistant helps students with:

    • Machine Learning doubts  
    • Python coding help  
    • Assignment explanations  
    • Concept clarification
    """)

    st.write("---")
    st.write("Developed for Students")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask your question here...")

if prompt:

    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages
            )

            reply = response.choices[0].message.content

            st.markdown(reply)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

# Footer
st.write("---")
st.caption("AI Department Assistant | Streamlit Project")
