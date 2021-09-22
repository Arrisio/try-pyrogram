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
        peer=f"@{settings.BOT_UNDER_TEST}",
        max_wait=10.0,
        wait_consecutive=0.8,
    )
    await c.initialize(start_client=False)
    yield c


async def test_ping(controller, client):
    assert await controller.ping_bot()


async def test_start(controller, client):
    await controller.clear_chat()
    async with controller.collect(count=5) as res:  # type: Response
        await controller.send_command("start")

    assert res.num_messages == 5
    assert res.messages[0].photo
    assert res.messages[0].photo.width == 700
    assert (
        res.messages[1].text
        == """Привет!
    Я Виртуальный Тренер по психологической подготовке к старту.     Я создан для развития навыка управления предстартовым состоянием."""
    )
    assert (
        res.messages[2].text
        == """Я помогу тебе:
 - протестировать текущее состояние
 - поставить цель подготовки
 - подобрать инструменты саморегуляции
 - построить график ментальных тренировок
 - составить индивидуальный план действий перед стартом
 - провести анализ выступления"""
    )
    # assert res.messages[3].text == "Ты сможешь настроить свою предстартовую психологическую подготовку, подходящую именно тебе,         прослушать лекции про стресс, изучить практические упражнения, которыми пользуются топовые спортсмены,         увидеть результаты своего тестирования, получить поддержку от спортивного психолога."
    # assert res.messages[4].text == "Вы будете участвовать в марафоне?"

    clicked_inline_kb = res.inline_keyboards[0]
    assert clicked_inline_kb.num_buttons == 2
    button1, button2 = clicked_inline_kb.rows[0]
    assert button1.text == "Да"
    assert button2.text == "Не в этот раз"

    # Нажали на кнопку "Да"
    async with controller.collect(count=2) as res:
        await clicked_inline_kb.click(pattern=r"Да")

    assert res.num_messages == 2

    clicked_inline_kb = res.inline_keyboards[0]
    assert clicked_inline_kb.num_buttons == 2
    button1, button2 = clicked_inline_kb.rows[0]
    assert button1.text == "✔Да"
    assert button2.text == "Не в этот раз"

    assert (
        res.messages[1].text
        == """Отлично! Выберите, пожалуйста, свою дистанцию
1. миля
2. 5 км
3. 10 км
4. 21 км
5. 42 км"""
    )

    inline_kb = res.inline_keyboards[1]
    assert inline_kb.num_buttons == 5
    assert inline_kb.rows[0][0].text == "1"
    assert inline_kb.rows[0][4].text == "5"
