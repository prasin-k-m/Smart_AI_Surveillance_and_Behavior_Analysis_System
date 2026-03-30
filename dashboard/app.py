# import streamlit as st
# import sqlite3
# import pandas as pd

# # ---------------- DB ----------------
# conn = sqlite3.connect("surveillance.db")

# # ---------------- TITLE ----------------
# st.title("🚀 Smart AI Surveillance Dashboard")

# # ---------------- LOAD DATA ----------------
# query = "SELECT * FROM events ORDER BY id DESC"
# df = pd.read_sql_query(query, conn)

# # ---------------- METRICS ----------------
# st.subheader("📊 Overview")

# col1, col2, col3 = st.columns(3)

# col1.metric("Total Events", len(df))
# col2.metric("High Risk", len(df[df["risk"] == "HIGH"]))
# col3.metric("Medical Alerts", len(df[df["risk"] == "MEDICAL"]))

# # ---------------- FILTER ----------------
# st.subheader("🔍 Filter")

# person_filter = st.selectbox("Select Person", ["All"] + list(df["person"].unique()))

# if person_filter != "All":
#     df = df[df["person"] == person_filter]

# # ---------------- TABLE ----------------
# st.subheader("📋 Event Logs")
# st.dataframe(df, use_container_width=True)

# # ---------------- CHART ----------------
# st.subheader("📈 Risk Distribution")

# risk_counts = df["risk"].value_counts()
# st.bar_chart(risk_counts)




# # streamlit run dashboard/app.py



import streamlit as st
import sqlite3
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# ---------------- AUTO REFRESH ----------------
# refresh every 3 seconds (3000 ms)
st_autorefresh(interval=3000, key="datarefresh")

# ---------------- DB ----------------
conn = sqlite3.connect("surveillance.db", check_same_thread=False)

# ---------------- TITLE ----------------
st.title("🚀 Smart AI Surveillance Dashboard")

# ---------------- LOAD DATA ----------------
query = "SELECT * FROM events ORDER BY id DESC LIMIT 100"
df = pd.read_sql_query(query, conn)

# ---------------- EMPTY CHECK ----------------
if df.empty:
    st.warning("⚠️ No events found yet")
    st.stop()

# ---------------- METRICS ----------------
st.subheader("📊 Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Events", len(df))
col2.metric("High Risk", len(df[df["risk"] == "HIGH"]))
col3.metric("Medical Alerts", len(df[df["risk"] == "MEDICAL"]))

# ---------------- FILTER ----------------
st.subheader("🔍 Filter")

person_filter = st.selectbox("Select Person", ["All"] + list(df["person"].unique()))

if person_filter != "All":
    df = df[df["person"] == person_filter]

# ---------------- ALERT BOX ----------------
# Show latest critical alert
latest_event = df.iloc[0]

if latest_event["risk"] == "HIGH":
    st.error(f"🚨 HIGH RISK ALERT: {latest_event['person']} detected!")
elif latest_event["risk"] == "MEDICAL":
    st.warning(f"⚠️ MEDICAL ALERT: {latest_event['person']} may need help!")

# ---------------- TABLE ----------------
st.subheader("📋 Event Logs")
st.dataframe(df, use_container_width=True)

# ---------------- CHART ----------------
st.subheader("📈 Risk Distribution")

risk_counts = df["risk"].value_counts()
st.bar_chart(risk_counts)


# # streamlit run dashboard/app.py