from pyrogram import Client

from settings import settings


app = Client("my_account", settings.API_ID, settings.API_HASH)


@app.on_message()
def my_handler(client, message):
    message.forward("me")


app.run()
