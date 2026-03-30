# import sqlite3
# import pandas as pd

# class SurveillanceRAG:
#     def __init__(self, db_path="surveillance.db"):
#         self.conn = sqlite3.connect(db_path)

#     def query_db(self, question):
#         df = pd.read_sql_query("SELECT * FROM events", self.conn)

#         question = question.lower()

#         if "weapon" in question:
#             return df[df["status"] == "ARMED"]

#         elif "fall" in question:
#             return df[df["posture"] == "FALLEN"]

#         elif "high" in question:
#             return df[df["risk"] == "HIGH"]

#         elif "today" in question:
#             return df.tail(10)

#         return df.tail(5)

#     def generate_answer(self, df, question):
#         if df.empty:
#             return "No relevant events found."

#         results = []

#         for _, row in df.iterrows():
#             results.append(
#                 f"{row['person']} was {row['status']} with {row['risk']} risk at {row['timestamp']}"
#             )

#         return "\n".join(results)

#     def ask(self, question):
#         df = self.query_db(question)
#         return self.generate_answer(df, question)





import sqlite3
import pandas as pd


class SurveillanceRAG:
    def __init__(self, db_path="surveillance.db"):
        self.db_path = db_path  # ✅ store path only (NOT connection)

    # ---------------- SAFE CONNECTION ----------------
    def get_connection(self):
        return sqlite3.connect(self.db_path)

    # ---------------- QUERY LOGIC ----------------
    def query_db(self, question):
        question = question.lower()

        # Default query
        query = "SELECT * FROM events ORDER BY id DESC LIMIT 20"

        if "weapon" in question or "armed" in question:
            query = """
                SELECT * FROM events 
                WHERE status='ARMED' 
                ORDER BY id DESC LIMIT 10
            """

        elif "fall" in question or "fallen" in question:
            query = """
                SELECT * FROM events 
                WHERE posture='FALLEN' 
                ORDER BY id DESC LIMIT 10
            """

        elif "high" in question:
            query = """
                SELECT * FROM events 
                WHERE risk='HIGH' 
                ORDER BY id DESC LIMIT 10
            """

        elif "medical" in question:
            query = """
                SELECT * FROM events 
                WHERE risk='MEDICAL' 
                ORDER BY id DESC LIMIT 10
            """

        elif "latest" in question:
            query = """
                SELECT * FROM events 
                ORDER BY id DESC LIMIT 1
            """

        elif "today" in question:
            query = """
                SELECT * FROM events 
                ORDER BY id DESC LIMIT 10
            """

        # ---------------- EXECUTE QUERY ----------------
        with self.get_connection() as conn:
            df = pd.read_sql_query(query, conn)

        return df

    # ---------------- RESPONSE GENERATION ----------------
    def generate_answer(self, df, question):
        if df.empty:
            return "❌ No relevant events found."

        question = question.lower()

        # ---------------- SPECIAL CASES ----------------
        if "latest" in question:
            row = df.iloc[0]
            return (
                f"🕒 Latest Event:\n"
                f"👤 Person: {row['person']}\n"
                f"⚠️ Risk: {row['risk']}\n"
                f"🧍 Posture: {row['posture']}\n"
                f"📅 Time: {row['timestamp']}"
            )

        if "how many" in question or "count" in question:
            return f"📊 Total matching events: {len(df)}"

        # ---------------- NORMAL RESPONSE ----------------
        results = []

        for _, row in df.iterrows():
            results.append(
                f"👤 {row['person']} | "
                f"Status: {row['status']} | "
                f"Risk: {row['risk']} | "
                f"Posture: {row['posture']} | "
                f"Time: {row['timestamp']}"
            )

        return "\n\n".join(results)

    # ---------------- MAIN FUNCTION ----------------
    def ask(self, question):
        try:
            df = self.query_db(question)
            return self.generate_answer(df, question)
        except Exception as e:
            return f"⚠️ Error: {str(e)}"