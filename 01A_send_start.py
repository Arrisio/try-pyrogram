from pyrogram import Client

from settings import settings

with Client("01_send", settings.TG_APP_API_ID, settings.TG_APP_API_HASH, phone_number=settings.PHONE_NUMBER, password=settings.TG_2FA_PASSWORD ) as app:
    app.send_message("dvmn_arrisio_bot", "/start")

