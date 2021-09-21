from loguru import logger
from pyrogram import Client
from tgintegration import BotController
import pytest
import asyncio

from settings import settings

pytestmark = pytest.mark.asyncio


@pytest.yield_fixture(scope="session", autouse=True)
def event_loop(request):
    """ Create an instance of the default event loop for the session. """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client() -> Client:
    # noinspection PyCallingNonCallable
    client = Client(
        "my_account", settings.TG_APP_API_ID, settings.TG_APP_API_HASH
    )
    await client.start()
    yield client
    await client.stop()


@pytest.fixture(scope="module")
async def controller(client):
    c = BotController(
        client=client,
        peer="@dvmn_arrisio_bot",
        max_wait=10.0,
        wait_consecutive=0.8,
    )
    await c.initialize(start_client=False)
    yield c

async def test_ping(controller, client):
    assert await controller.ping_bot()



async def test_start(controller, client):
    async with controller.collect() as res:  # type: Response
        await controller.send_command("start")

    assert res.num_messages == 1
    assert res[0]['text'] == "you said: /start@dvmn_arrisio_bot"



async def test_poll(controller, client):
    async with controller.collect() as res:  # type: Response
        await controller.send_command("/testPoll")

    assert res.num_messages == 1

    poll = res[0].poll

    assert poll
    assert poll['options'][0]['text'] == 'answer1'
    assert poll['options'][1]['text'] == 'answer2'
    assert len(poll['options']) == 2


async def test_modify_kb(controller, client):
    async with controller.collect() as res:  # type: Response
        await controller.send_command("/testModifyInlineKeyboard")

    inline_keyboard = res.inline_keyboards[0]
    assert inline_keyboard
    assert len(inline_keyboard.rows[0]) == 1

    fresh_data = await inline_keyboard.click(index=0)
    inline_keyboards = fresh_data.inline_keyboards #['inline_keyboards']
    button = inline_keyboards[0].rows[0][0]
    assert button.callback_data == '#new_kb'
    assert button.text == '#new_kb'
