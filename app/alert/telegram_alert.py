# # from twilio.rest import Client

# # class WhatsAppAlert:
# #     def __init__(self, sid, token, from_number, to_number):
# #         self.client = Client(sid, token)
# #         self.from_number = from_number
# #         self.to_number = to_number

# #     def send(self, message):
# #         try:
# #             self.client.messages.create(
# #                 body=message,
# #                 from_=self.from_number,
# #                 to=self.to_number
# #             )
# #             print("📲 WhatsApp alert sent!")
# #         except Exception as e:
# #             print("❌ WhatsApp error:", e)



# import requests

# class TelegramAlert:
#     def __init__(self, bot_token, chat_id):
#         self.bot_token = bot_token
#         self.chat_id = chat_id

#     def send(self, message, image_path=None):
#         try:
#             if image_path:
#                 url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"

#                 with open(image_path, "rb") as photo:
#                     requests.post(
#                         url,
#                         data={
#                             "chat_id": self.chat_id,
#                             "caption": message
#                         },
#                         files={"photo": photo}
#                     )
#             else:
#                 url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

#                 requests.post(
#                     url,
#                     data={
#                         "chat_id": self.chat_id,
#                         "text": message
#                     }
#                 )

#             print("📲 Telegram alert sent!")

#         except Exception as e:
#             print("❌ Telegram error:", e)









import requests

class TelegramAlert:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def send(self, message, image_path=None):
        try:
            if image_path:
                url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"

                with open(image_path, "rb") as photo:
                    response = requests.post(
                        url,
                        data={"chat_id": self.chat_id, "caption": message},
                        files={"photo": photo}
                    )
            else:
                url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

                response = requests.post(
                    url,
                    data={"chat_id": self.chat_id, "text": message}
                )

            print("📲 Telegram response:", response.text)

        except Exception as e:
            print("❌ Telegram error:", e)