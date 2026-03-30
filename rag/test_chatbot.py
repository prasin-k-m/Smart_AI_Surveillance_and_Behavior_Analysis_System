from rag.chatbot import SurveillanceRAG

bot = SurveillanceRAG()

print("\n🤖 Surveillance Chatbot Ready!\n")

while True:
    q = input("You: ")

    if q.lower() in ["exit", "quit"]:
        break

    answer = bot.ask(q)

    print("\nBot:", answer, "\n")



# python rag/test_chatbot.py



# python -m rag.test_chatbot