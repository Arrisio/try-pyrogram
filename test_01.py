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
    client = Client("my_account", settings.API_ID, settings.API_HASH)
    await client.start()
    yield client
    await client.stop()


@pytest.fixture(scope="module")
async def controller(client):
    c = BotController(
        client=client,
        peer="@BotListBot",
        max_wait=10.0,
        wait_consecutive=0.8,
    )
    await c.initialize(start_client=False)
    yield c


async def test_start(controller, client):
    async with controller.collect(count=3) as res:  # type: Response
        await controller.send_command("/start")

    assert res.num_messages == 3
    assert res[0].sticker  # First message is a sticker


async def test_ping(controller, client):
    assert await controller.ping_bot()

