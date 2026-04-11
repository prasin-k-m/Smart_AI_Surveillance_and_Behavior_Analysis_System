
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import streamlit as st
st.set_page_config(page_title="AI Surveillance System", layout="wide")


import sqlite3
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from rag.chatbot import SurveillanceRAG


st_autorefresh(interval=5000, key="refresh")

#  LOAD CHATBOT 
@st.cache_resource
def load_bot():
    return SurveillanceRAG()

bot = load_bot()

# LOAD DATA 
def load_data():
    try:
        conn = sqlite3.connect("surveillance.db", check_same_thread=False)
        df = pd.read_sql_query(
            "SELECT * FROM events ORDER BY id DESC LIMIT 100",
            conn
        )
        conn.close()
        return df
    except Exception as e:
        st.error(f"DB Error: {e}")
        return pd.DataFrame()

df = load_data()

# TITLE 
st.title(" Smart AI Surveillance Dashboard ")

# LAYOUT 
left, right = st.columns([2, 1])


# DASHBOARD

with left:
    st.subheader("Overview")

    if df.empty:
        st.warning("No events found yet")
    else:
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Events", len(df))
        col2.metric("High Risk", len(df[df["risk"] == "HIGH"]))
        col3.metric("Medical Alerts", len(df[df["risk"] == "MEDICAL"]))

        st.subheader("Event Logs")
        st.dataframe(df, use_container_width=True)

        st.subheader("Risk Distribution")
        st.bar_chart(df["risk"].value_counts())


# CHATBOT 

with right:

    st.subheader("AI Assistant")

    # Session memory
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    user_input = st.chat_input("Ask about risks, people, alerts...")

    if user_input:
        # Show user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.markdown(user_input)

        # Assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking... please wait")

            try:
                response = bot.ask(user_input)

                if not response or response.strip() == "":
                    response = "No meaningful response from model."

            except Exception as e:
                response = f"Error: {str(e)}"

            message_placeholder.markdown(response)

        # Save response
        st.session_state.messages.append({
            "role": "assistant",
            "content": response })



# ollama run tinyllama
# streamlit run dashboard/app.py