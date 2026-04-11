
import sqlite3
import pandas as pd
import ollama


class SurveillanceRAG:
    def __init__(self, db_path="surveillance.db"):
        self.db_path = db_path

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def load_data(self):
        conn = self.get_connection()
        df = pd.read_sql_query(
            "SELECT * FROM events ORDER BY id DESC LIMIT 50",
            conn )
        
        conn.close()
        return df

    def ask(self, question):
        try:
            print("🔍 Loading data...")
            df = self.load_data()

            if df.empty:
                return "No data available."

            print("Data ready")

            # Reduce load for low RAM system

            context = df.head(3).to_string(index=False)

            prompt = f"""
You are an intelligent AI surveillance assistant.

Analyze the data and answer clearly.

DATA:
{context}

QUESTION:
{question}

Give short, clear, and accurate answers.
"""

            print("Calling Ollama...")

            response = ollama.chat(
                model="tinyllama",
                messages=[
                    {"role": "user", "content": prompt}])

            print("Response received")

            return response["message"]["content"]

        except Exception as e:
            print("ERROR:", e)
            return f"Error: {str(e)}"