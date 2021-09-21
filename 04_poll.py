import sys

from pyrogram import Client
from loguru import logger
from settings import settings

app = Client("my_account", settings.TG_APP_API_ID, settings.TG_APP_API_HASH)


@app.on_poll()
def handle_poll(client, poll):
    logger.debug(poll)
    print("1!")


@app.on_inline_query()
def handle_on_inline_query(client, inline_query):
    logger.debug('on_inline_query')
    print("inline_query")


@app.on_message()
def my_handler(client, message):
    if message.poll:
        logger.debug("Poll included", n_option=len(message.poll.options))
        for option in message.poll.options:
            logger.debug(
                "option",
            )

        client.vote_poll(
            chat_id=message.chat.id,
            message_id=message.message_id,
            options=[0],
        )

    logger.debug('on_message')


if __name__ == "__main__":

    logger.configure(
        **{
            "handlers": [
                {
                    "sink": sys.stdout,
                    # "level": log_level,
                    "format": (
                        "<level>{level: <8} {time:YYYY-MM-DD HH:mm:ss}</level>|"
                        "<cyan>{name:<12}</cyan>:<cyan>{function:<24}</cyan>:"
                        "<cyan>{line}</cyan> - <level>{message:>32}</level>|{extra}"
                    ),
                },
            ],
        }
    )
    app.run()
