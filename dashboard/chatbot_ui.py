# # # import streamlit as st
# # # from rag.chatbot import SurveillanceRAG

# # # bot = SurveillanceRAG()

# # # st.title("🤖 Surveillance AI Assistant")

# # # query = st.text_input("Ask something...")

# # # if query:
# # #     response = bot.ask(query)
# # #     st.write(response)



# # # # streamlit run dashboard/chatbot_ui.py
# # # #  streamlit run dashboard/chatbot_ui.py




# # import sys
# # import os
# # import streamlit as st

# # # -------------------------------
# # # FIX: Add project root to path
# # # -------------------------------
# # ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# # if ROOT_DIR not in sys.path:
# #     sys.path.insert(0, ROOT_DIR)

# # # -------------------------------
# # # Import your chatbot
# # # -------------------------------
# # from rag.chatbot import SurveillanceRAG

# # # -------------------------------
# # # Initialize bot (only once)
# # # -------------------------------
# # @st.cache_resource
# # def load_bot():
# #     return SurveillanceRAG()

# # bot = load_bot()

# # # -------------------------------
# # # Streamlit UI
# # # -------------------------------
# # st.set_page_config(page_title="Surveillance Chatbot", layout="wide")

# # st.title("🤖 AI Surveillance Chatbot")
# # st.write("Ask anything about surveillance logs, events, or risk analysis.")

# # # -------------------------------
# # # Chat history
# # # -------------------------------
# # if "messages" not in st.session_state:
# #     st.session_state.messages = []

# # # Display previous messages
# # for msg in st.session_state.messages:
# #     with st.chat_message(msg["role"]):
# #         st.markdown(msg["content"])

# # # -------------------------------
# # # User input
# # # -------------------------------
# # query = st.chat_input("Ask your question...")

# # if query:
# #     # Show user message
# #     st.session_state.messages.append({"role": "user", "content": query})
# #     with st.chat_message("user"):
# #         st.markdown(query)

# #     # Get bot response
# #     with st.chat_message("assistant"):
# #         with st.spinner("Thinking..."):
# #             try:
# #                 response = bot.ask(query)
# #             except Exception as e:
# #                 response = f"❌ Error: {str(e)}"

# #             st.markdown(response)

# #     # Save response
# #     st.session_state.messages.append({"role": "assistant", "content": response})







# import streamlit as st

# # ✅ MUST BE FIRST STREAMLIT COMMAND
# st.set_page_config(page_title="Surveillance Chatbot", layout="wide")

# # باقي imports
# import sqlite3
# import pandas as pd
# from rag.chatbot import SurveillanceRAG  # make sure this path is correct

# # ---------------- INIT BOT ----------------
# @st.cache_resource
# def load_bot():
#     return SurveillanceRAG()

# bot = load_bot()

# # ---------------- TITLE ----------------
# st.title("🤖 Smart Surveillance Chatbot")

# st.markdown("Ask questions about surveillance events, risks, or activity logs.")

# # ---------------- DB CONNECTION ----------------
# conn = sqlite3.connect("surveillance.db", check_same_thread=False)

# # ---------------- LOAD DATA ----------------
# query = "SELECT * FROM events ORDER BY id DESC LIMIT 100"
# df = pd.read_sql_query(query, conn)

# # ---------------- SIDEBAR ----------------
# st.sidebar.header("📊 Quick Insights")

# if not df.empty:
#     st.sidebar.metric("Total Events", len(df))
#     st.sidebar.metric("High Risk", len(df[df["risk"] == "HIGH"]))
#     st.sidebar.metric("Medical", len(df[df["risk"] == "MEDICAL"]))
# else:
#     st.sidebar.warning("No data available")

# # ---------------- CHAT HISTORY ----------------
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # ---------------- DISPLAY CHAT ----------------
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # ---------------- USER INPUT ----------------
# user_input = st.chat_input("Ask something like: Who is high risk?")

# if user_input:
#     # Show user message
#     st.chat_message("user").markdown(user_input)
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     # Get bot response
#     try:
#         response = bot.ask(user_input)
#     except Exception as e:
#         response = f"⚠️ Error: {str(e)}"

#     # Show bot message
#     with st.chat_message("assistant"):
#         st.markdown(response)

#     st.session_state.messages.append({"role": "assistant", "content": response})

# # ---------------- OPTIONAL: SHOW DATA ----------------
# with st.expander("📋 View Recent Events"):
#     if not df.empty:
#         st.dataframe(df, use_container_width=True)
#     else:
#         st.info("No events found.")

# ---------------- PATH FIX (VERY IMPORTANT) ----------------
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ---------------- STREAMLIT FIRST ----------------
import streamlit as st

st.set_page_config(page_title="Surveillance Chatbot", layout="wide")

# ---------------- OTHER IMPORTS ----------------
import sqlite3
import pandas as pd

# ✅ Import AFTER path fix
from rag.chatbot import SurveillanceRAG


# ---------------- LOAD CHATBOT ----------------
@st.cache_resource
def load_bot():
    return SurveillanceRAG()

bot = load_bot()


# ---------------- TITLE ----------------
st.title("🤖 Smart AI Surveillance Chatbot")
st.markdown("Ask anything about events, risks, people, or alerts.")


# ---------------- DATABASE ----------------
conn = sqlite3.connect("surveillance.db", check_same_thread=False)

query = "SELECT * FROM events ORDER BY id DESC LIMIT 100"
df = pd.read_sql_query(query, conn)


# ---------------- SIDEBAR ----------------
st.sidebar.header("📊 Live Overview")

if not df.empty:
    st.sidebar.metric("Total Events", len(df))
    st.sidebar.metric("High Risk", len(df[df["risk"] == "HIGH"]))
    st.sidebar.metric("Medical Alerts", len(df[df["risk"] == "MEDICAL"]))
else:
    st.sidebar.warning("No data available yet")


# ---------------- ALERT SYSTEM ----------------
if not df.empty:
    latest = df.iloc[0]

    if latest["risk"] == "HIGH":
        st.error(f"🚨 HIGH RISK: {latest['person']} detected!")
    elif latest["risk"] == "MEDICAL":
        st.warning(f"⚠️ MEDICAL ALERT: {latest['person']} may need help!")


# ---------------- CHAT MEMORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ---------------- USER INPUT ----------------
user_input = st.chat_input("Ask: Who is high risk? / Show latest alerts")

if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get bot response
    try:
        response = bot.ask(user_input)
    except Exception as e:
        response = f"⚠️ Error: {str(e)}"

    # Show bot message
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})


# ---------------- DATA VIEW ----------------
with st.expander("📋 View Recent Events"):
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No events found.")


# ---------------- QUICK ACTIONS ----------------
st.subheader("⚡ Quick Queries")

col1, col2, col3 = st.columns(3)

if col1.button("🚨 High Risk People"):
    question = "Who are high risk people?"
elif col2.button("⚠️ Medical Cases"):
    question = "Show medical alerts"
elif col3.button("🕒 Latest Event"):
    question = "What is the latest event?"
else:
    question = None

if question:
    st.chat_message("user").markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

    try:
        response = bot.ask(question)
    except Exception as e:
        response = f"⚠️ Error: {str(e)}"

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})