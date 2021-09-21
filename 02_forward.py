from pyrogram import Client

from settings import settings


app = Client("my_account", settings.TG_APP_API_ID, settings.TG_APP_API_HASH)


@app.on_message()
def my_handler(client, message):
    message.forward("me")


app.run()
