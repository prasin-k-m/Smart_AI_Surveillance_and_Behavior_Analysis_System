# # dashboard/app.py

# # ---------------- PATH FIX ----------------
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# # ---------------- STREAMLIT ----------------
# import streamlit as st
# st.set_page_config(page_title="AI Surveillance System", layout="wide")

# # ---------------- IMPORTS ----------------
# import sqlite3
# import pandas as pd
# from streamlit_autorefresh import st_autorefresh
# from rag.chatbot import SurveillanceRAG

# # ---------------- AUTO REFRESH ----------------
# st_autorefresh(interval=3000, key="refresh")

# # ---------------- LOAD CHATBOT ----------------
# @st.cache_resource
# def load_bot():
#     return SurveillanceRAG()

# bot = load_bot()

# # ---------------- DB CONNECTION ----------------
# conn = sqlite3.connect("surveillance.db", check_same_thread=False)

# def load_data():
#     query = "SELECT * FROM events ORDER BY id DESC LIMIT 100"
#     return pd.read_sql_query(query, conn)

# df = load_data()

# # ---------------- TITLE ----------------
# st.title("🚀 Smart AI Surveillance Dashboard + Chatbot")

# # ---------------- HANDLE EMPTY ----------------
# if df.empty:
#     st.warning("⚠️ No events found yet")
#     st.stop()

# # =========================================================
# # 🧠 LAYOUT: LEFT = DASHBOARD | RIGHT = CHATBOT
# # =========================================================

# left, right = st.columns([2, 1])

# # =========================================================
# # 📊 LEFT SIDE → DASHBOARD
# # =========================================================
# with left:

#     st.subheader("📊 Overview")

#     col1, col2, col3 = st.columns(3)

#     col1.metric("Total Events", len(df))
#     col2.metric("High Risk", len(df[df["risk"] == "HIGH"]))
#     col3.metric("Medical Alerts", len(df[df["risk"] == "MEDICAL"]))

#     # ---------------- FILTER ----------------
#     st.subheader("🔍 Filter")

#     person_filter = st.selectbox(
#         "Select Person",
#         ["All"] + list(df["person"].unique())
#     )

#     filtered_df = df.copy()

#     if person_filter != "All":
#         filtered_df = filtered_df[filtered_df["person"] == person_filter]

#     # ---------------- ALERT ----------------
#     latest = filtered_df.iloc[0]

#     if latest["risk"] == "HIGH":
#         st.error(f"🚨 HIGH RISK ALERT: {latest['person']}")
#     elif latest["risk"] == "MEDICAL":
#         st.warning(f"⚠️ MEDICAL ALERT: {latest['person']}")

#     # ---------------- TABLE ----------------
#     st.subheader("📋 Event Logs")
#     st.dataframe(filtered_df, use_container_width=True)

#     # ---------------- CHART ----------------
#     st.subheader("📈 Risk Distribution")
#     st.bar_chart(filtered_df["risk"].value_counts())

# # =========================================================
# # 🤖 RIGHT SIDE → CHATBOT
# # =========================================================
# with right:

#     st.subheader("🤖 AI Assistant")

#     # ---------------- CHAT MEMORY ----------------
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # ---------------- DISPLAY CHAT ----------------
#     for msg in st.session_state.messages:
#         with st.chat_message(msg["role"]):
#             st.markdown(msg["content"])

#     # ---------------- USER INPUT ----------------
#     user_input = st.chat_input("Ask about surveillance...")

#     if user_input:
#         # show user message
#         st.chat_message("user").markdown(user_input)
#         st.session_state.messages.append({
#             "role": "user",
#             "content": user_input
#         })

#         # get response
#         try:
#             response = bot.ask(user_input)
#         except Exception as e:
#             response = f"⚠️ Error: {str(e)}"

#         # show response
#         with st.chat_message("assistant"):
#             st.markdown(response)

#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": response
#         })

#     # ---------------- QUICK BUTTONS ----------------
#     # st.markdown("### ⚡ Quick Actions")

#     # if st.button("🚨 High Risk"):
#     #     question = "Who are high risk people?"
#     # elif st.button("⚠️ Medical Alerts"):
#     #     question = "Show medical alerts"
#     # elif st.button("🕒 Latest Event"):
#     #     question = "Show latest event"
#     # else:
#     #     question = None

#     if question:
#         st.chat_message("user").markdown(question)
#         st.session_state.messages.append({"role": "user", "content": question})

#         try:
#             response = bot.ask(question)
#         except Exception as e:
#             response = f"⚠️ Error: {str(e)}"

#         with st.chat_message("assistant"):
#             st.markdown(response)

#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": response
#         })





# dashboard/app.py





# dashboard/app.py

# ---------------- PATH FIX ----------------
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ---------------- STREAMLIT ----------------
import streamlit as st
st.set_page_config(page_title="AI Surveillance System", layout="wide")

# ---------------- IMPORTS ----------------
import sqlite3
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from rag.chatbot import SurveillanceRAG

# ---------------- AUTO REFRESH ----------------
st_autorefresh(interval=3000, key="refresh")

# ---------------- LOAD CHATBOT ----------------
@st.cache_resource
def load_bot():
    return SurveillanceRAG()

bot = load_bot()

# ---------------- DB ----------------
conn = sqlite3.connect("surveillance.db", check_same_thread=False)

def load_data():
    try:
        return pd.read_sql_query(
            "SELECT * FROM events ORDER BY id DESC LIMIT 100",
            conn
        )
    except Exception as e:
        st.error(f"DB Error: {e}")
        return pd.DataFrame()

df = load_data()

# ---------------- TITLE ----------------
st.title("🚀 Smart AI Surveillance Dashboard + Chatbot")

if df.empty:
    st.warning("⚠️ No events found yet")

# ---------------- LAYOUT ----------------
left, right = st.columns([2, 1])

# =========================================================
# 📊 DASHBOARD
# =========================================================
with left:
    st.subheader("📊 Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Events", len(df))
    col2.metric("High Risk", len(df[df["risk"] == "HIGH"]))
    col3.metric("Medical Alerts", len(df[df["risk"] == "MEDICAL"]))

    st.subheader("📋 Event Logs")
    st.dataframe(df, use_container_width=True)

    st.subheader("📈 Risk Distribution")
    if not df.empty:
        st.bar_chart(df["risk"].value_counts())

# =========================================================
# 🤖 CHATBOT
# =========================================================
with right:

    st.subheader("🤖 AI Assistant")

    # ---------------- SESSION ----------------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ---------------- DISPLAY ----------------
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ---------------- INPUT ----------------
    user_input = st.chat_input("Ask something...")

    if user_input:
        # show user
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.markdown(user_input)

        # ---------------- BOT RESPONSE ----------------
        response = bot.ask(user_input)

        if not response:
            response = "⚠️ No response from chatbot"

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        with st.chat_message("assistant"):
            st.markdown(response)

        # 🔥 IMPORTANT FIX → force refresh
        st.rerun()