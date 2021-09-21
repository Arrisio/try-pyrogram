import sys

from loguru import logger

from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.filters import Regexp
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData
from more_itertools import chunked

from typing import List

from settings import settings

bot = Bot(settings.TG_BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


class ApplicationState(StatesGroup):
    WAITING_EMAIL = State()


@dp.message_handler(CommandStart(), state="*")
async def handle_start(message: types.Message, state: FSMContext):
    logger.debug("handle_start", text=message.text)
    await message.answer(f"you said: {message.text}")


@dp.message_handler(commands=["testPoll"], state="*")
async def handle_start(message: types.Message, state: FSMContext):
    logger.debug("testPoll")
    await bot.send_poll(
        chat_id=message.chat.id,
        question="Poll question",
        is_anonymous=False,
        options=["answer1", "answer2"],
    )


@dp.message_handler(commands=["testModifyInlineKeyboard"], state="*")
async def handle_start_testing_inline_kb(
    message: types.Message, state: FSMContext
):
    logger.debug("testInlineKeyboard")
    outgoing_message = await message.answer(
        "test modification inline keyboard",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="#previous_kb", callback_data="#previous_kb"
                    )
                ]
            ],
        ),
    )


@dp.callback_query_handler(text="#previous_kb", state="*")
async def receive_inline(call: CallbackQuery):
    logger.debug("receive_inline")
    await call.answer()

    await call.message.edit_reply_markup(
        InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="#new_kb", callback_data="#new_kb")]
            ],
        )
    )


async def on_startup(dp):
    await dp.bot.send_message(
        settings.TG_BOT_ADMIN_ID, "Бот Запущен и готов к работе!"
    )


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
    logger.info("telegram service started")
    executor.start_polling(dp, on_startup=on_startup)
    logger.info("service service stopped")
