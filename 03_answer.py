from pyrogram import Client

from settings import settings

app = Client("my_account", settings.TG_APP_API_ID, settings.TG_APP_API_HASH)


@app.on_message()
def my_handler(client, message):
    # Вариант 1
    message.reply(message.text + "1!")

    # Вариант 2 - работает правильонее
    client.send_message(
        chat_id=message.chat.id,
        text=message.text + "2!",
        reply_to_message_id=message.message_id,
    )


app.run()
