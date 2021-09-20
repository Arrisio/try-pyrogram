from pyrogram import Client

from settings import settings

with Client("my_account", settings.API_ID, settings.API_HASH) as app:
    app.send_message("me", "Greetings from **Pyrogram**!")

app2 =  Client("my_account", settings.API_ID, settings.API_HASH)
with app2:
    app2.send_message("me", "Greetings from **Pyrogram**!#2")