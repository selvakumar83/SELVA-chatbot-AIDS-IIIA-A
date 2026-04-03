import streamlit as st
import pandas as pd
from groq import Groq
import graphviz
import plotly.express as px
from datetime import date
import os

st.set_page_config(page_title="AI Classroom Platform", layout="wide")

st.title("🎓 AI Classroom Platform")

# ---------------- API ----------------

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Please add GROQ_API_KEY in Streamlit secrets")
    st.stop()

# ---------------- MENU ----------------

menu = st.sidebar.radio(
    "Select Module",
    [
        "💬 AI Chatbot",
        "📋 Attendance Entry",
        "📊 Attendance Dashboard",
        "📈 ML Diagram Generator"
    ]
)

# ---------------- CHATBOT ----------------

if menu == "💬 AI Chatbot":

    st.header("AI Tutor")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input("Ask Machine Learning question")

    if prompt:

        st.session_state.messages.append({"role":"user","content":prompt})

        with st.chat_message("user"):
            st.write(prompt)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages
        )

        reply = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.write(reply)

        st.session_state.messages.append(
            {"role":"assistant","content":reply}
        )

# ---------------- ATTENDANCE ENTRY ----------------

if menu == "📋 Attendance Entry":

    st.header("Student Attendance")

    df = pd.read_csv("students.csv")

    today = st.date_input("Select Date", date.today())

    attendance_data = []

    for i,row in df.iterrows():

        status = st.selectbox(
            f"{row['Register']} - {row['Name']}",
            ["Present","Absent"],
            key=row["Register"]
        )

        attendance_data.append({
            "Register":row["Register"],
            "Name":row["Name"],
            "Status":status,
            "Date":today
        })

    if st.button("Save Attendance"):

        new_df = pd.DataFrame(attendance_data)

        if os.path.exists("attendance.csv"):
            new_df.to_csv("attendance.csv",mode="a",index=False,header=False)
        else:
            new_df.to_csv("attendance.csv",index=False)

        st.success("Attendance saved")

# ---------------- ATTENDANCE DASHBOARD ----------------

if menu == "📊 Attendance Dashboard":

    st.header("Attendance Analytics")

    if os.path.exists("attendance.csv"):

        data = pd.read_csv("attendance.csv")

        summary = data.groupby("Status").size().reset_index(name="Count")

        fig = px.pie(summary,values="Count",names="Status")

        st.plotly_chart(fig)

        st.subheader("Attendance Records")

        st.dataframe(data)

        st.download_button(
            "Download CSV",
            data.to_csv(index=False),
            "attendance.csv"
        )

    else:
        st.info("No attendance data yet")

# ---------------- ML DIAGRAMS ----------------

if menu == "📈 ML Diagram Generator":

    st.header("Machine Learning Diagrams")

    algo = st.selectbox(
        "Select Algorithm",
        ["Decision Tree","Neural Network","K-Means"]
    )

    dot = graphviz.Digraph()

    if algo == "Decision Tree":

        dot.node("A","Root")
        dot.node("B","Feature < 5")
        dot.node("C","Class A")
        dot.node("D","Class B")

        dot.edges(["AB","BC","BD"])

    if algo == "Neural Network":

        dot.node("I1","Input1")
        dot.node("I2","Input2")
        dot.node("H1","Hidden1")
        dot.node("H2","Hidden2")
        dot.node("O","Output")

        dot.edges([
            ("I1","H1"),
            ("I2","H1"),
            ("H1","H2"),
            ("H2","O")
        ])

    if algo == "K-Means":

        dot.node("A","Data Points")
        dot.node("B","Cluster 1")
        dot.node("C","Cluster 2")

        dot.edges([("A","B"),("A","C")])

    st.graphviz_chart(dot)
