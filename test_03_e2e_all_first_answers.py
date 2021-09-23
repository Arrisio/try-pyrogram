from typing import Union

from loguru import logger
from pyrogram import Client
from tgintegration import BotController, InvalidResponseError
import pytest
import asyncio

from settings import settings

pytestmark = pytest.mark.asyncio


async def test_ping(controller, client):
    assert await controller.ping_bot()


async def test_start(controller, client):
    await controller.clear_chat()
    async with controller.collect() as res:  # type: Response
        await controller.send_command("start")

    assert res.num_messages > 0


async def test_scenario01(controller, client):
    await controller.clear_chat()

    res = await step01_start(controller, client)
    res = await step02_will_tak_part(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step03_run_1_mile(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step04_my_first_start(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step05_if_agree(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step06_i_want_to_know_about_stress(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step07_about_stress_why_run(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )


async def step01_start(controller, client):
    expected_msgs_number = 4
    msgs1_keywords = ["Привет", "марафон"]
    msgs2_keywords = ["помогу", "марафон"]
    msgs3_keywords = ["участвовать", "HONOR", "полезен"]

    async with controller.collect(
        count=expected_msgs_number
    ) as res:  # type: Response
        await controller.send_command("start")

    assert res.messages[0].photo
    assert 400 <= res.messages[0].photo.width <= 800

    verify_keywords_in_msg(res.messages, msgs1_keywords, msg_idx=[1, 2])
    verify_keywords_in_msg(res.messages, msgs2_keywords, msg_idx=[1, 2, 3])
    verify_keywords_in_msg(res.messages, msgs3_keywords, msg_idx=[2, 3])

    kb = res.inline_keyboards[0]
    assert kb.num_buttons == 2
    button1, button2 = kb.rows[0]

    assert button1.text == "Буду участвовать"
    assert button2.text == "Не в этот раз"

    return res


async def step02_will_tak_part(controller, client, clicking_kb):
    clicking_button_idx = 0  # кнопка буду участвовать

    expected_msgs_number = (
        2  # 1ое сообщение - изменяемая клава. 2е - само сообщение
    )
    msgs1_keywords = ["Отлично", "дистанцию", "км"]

    res = await click(
        clicking_kb, expected_msgs_number, clicking_button_idx, controller
    )

    verify_keywords_in_msg(res.messages, msgs1_keywords, msg_idx=1)
    verify_numeric_kb_is_valid(res.inline_keyboards[-1], num_buttons=5)

    verify_clicked_button_was_marked(
        new_kb=res.inline_keyboards[0],
        prev_kb=clicking_kb,
        clicked_button_idx=clicking_button_idx,
    )
    return res


async def step03_run_1_mile(controller, client, clicking_kb):
    clicking_button_idx = 0  # кнопка 1

    expected_msgs_number = 2
    msgs1_keywords = ["опыт", "спортсмен"]

    res = await click(
        clicking_kb, expected_msgs_number, clicking_button_idx, controller
    )

    verify_keywords_in_msg(res.messages, msgs1_keywords, msg_idx=1)
    verify_numeric_kb_is_valid(res.inline_keyboards[-1], num_buttons=6)
    verify_clicked_button_was_marked(
        prev_kb=clicking_kb,
        new_kb=res.inline_keyboards[0],
        clicked_button_idx=clicking_button_idx,
    )

    return res


async def step04_my_first_start(controller, client, clicking_kb):
    clicking_button_idx = 0  # кнопка 1

    expected_msgs_number = 5
    msgs1_keywords = []
    msgs2_keywords = ["согласие"]
    msgs4_keywords = ["прочли", "согласны"]

    res = await click(
        clicking_kb, expected_msgs_number, clicking_button_idx, controller
    )

    verify_keywords_in_msg(res.messages, msgs1_keywords, msg_idx=[1, 2])
    verify_keywords_in_msg(res.messages, msgs2_keywords, msg_idx=[2, 3])
    verify_keywords_in_msg(res.messages, msgs4_keywords, msg_idx=4)

    verify_clicked_button_was_marked(
        prev_kb=clicking_kb,
        new_kb=res.inline_keyboards[0],
        clicked_button_idx=clicking_button_idx,
    )

    return res


async def step05_if_agree(controller, client, clicking_kb):
    clicking_button_idx = 0  # кнопка 1

    expected_msgs_number = 6
    msgs1_keywords = ["начнем"]
    msgs2_keywords = ["соревнования", "справляться"]
    msgs3_keywords = ["https"]
    msgs4_keywords = ["коротко"]
    msgs5_keywords = ["хотите", "узнать"]

    res = await click(
        clicking_kb, expected_msgs_number, clicking_button_idx, controller
    )

    verify_keywords_in_msg(res.messages, msgs1_keywords, msg_idx=1)
    verify_keywords_in_msg(res.messages, msgs2_keywords, msg_idx=[2, 3])
    verify_keywords_in_msg(res.messages, msgs3_keywords, msg_idx=[2, 3])
    verify_keywords_in_msg(res.messages, msgs4_keywords, msg_idx=[4, 5])
    verify_keywords_in_msg(res.messages, msgs5_keywords, msg_idx=[4, 5])

    verify_clicked_button_was_marked(
        prev_kb=clicking_kb,
        new_kb=res.inline_keyboards[0],
        clicked_button_idx=clicking_button_idx,
    )

    return res


async def step06_i_want_to_know_about_stress(controller, client, clicking_kb):
    clicking_button_idx = 0  # кнопка 1

    expected_msgs_number = 5
    msgs1_keywords = ["Отлично"]
    msgs2_keywords = ["https"]
    msgs3_keywords = ["Важный", "шаг"]
    msgs4_keywords = ["Почему", "занимаетесь"]

    res = await click(
        clicking_kb, expected_msgs_number, clicking_button_idx, controller
    )

    verify_keywords_in_msg(res.messages, msgs1_keywords, msg_idx=1)
    verify_keywords_in_msg(res.messages, msgs2_keywords, msg_idx=2)
    verify_keywords_in_msg(res.messages, msgs3_keywords, msg_idx=3)
    verify_keywords_in_msg(res.messages, msgs4_keywords, msg_idx=4)

    verify_clicked_button_was_marked(
        prev_kb=clicking_kb,
        new_kb=res.inline_keyboards[0],
        clicked_button_idx=clicking_button_idx,
    )
    verify_numeric_kb_is_valid(res.inline_keyboards[-1], num_buttons=6)

    return res


async def step07_about_stress_why_run(controller, client, clicking_kb):
    clicking_button_idx = 0  # кнопка 1

    expected_msgs_number = 2
    msgs1_keywords = ["Какая", "цель"]

    # res = await click(
    #     clicking_kb, expected_msgs_number, clicking_button_idx, controller
    # )

    # async with controller.collect(count=1) as res:
    await asyncio.sleep(1)
    res = await clicking_kb.click(index=clicking_button_idx)

    verify_keywords_in_msg(res.messages, msgs1_keywords, msg_idx=1)

    verify_clicked_button_was_marked(
        prev_kb=clicking_kb,
        new_kb=res.inline_keyboards[0],
        clicked_button_idx=clicking_button_idx,
    )

    return res


class IncorrectPresButtonResultException(Exception):
    pass


async def click(kb, expected_msgs_number, clicking_button_idx, controller):
    try:
        async with controller.collect(count=expected_msgs_number) as res:
            await kb.click(index=clicking_button_idx)

        # надо перепроверить, но, похоже, бессмысленный assert
        assert (
            res.num_messages == expected_msgs_number
        ), "Не получено ожидаемое число сообщений"

    except (InvalidResponseError, TimeoutError):
        raise IncorrectPresButtonResultException(
            "Не получено ожидаемое число сообщений"
        )

    return res


def verify_keywords_in_msg(
    all_messages, keywords, msg_idx: Union[int, list[int]]
):
    """

    :param all_messages:
    :param keywords:
    :param msg_idx:  может быть списком, т.к. порядок сообщений не всегда соблюдается
    :return:
    """

    if isinstance(msg_idx, list):
        msgs_text = " ".join(
            all_messages[msg_idx_].text.lower()
            for msg_idx_ in msg_idx
            if all_messages[msg_idx_].text
        )
    elif isinstance(msg_idx, int):
        msgs_text = all_messages[msg_idx].text.lower()
    else:
        raise TabError("msg_idx must be INT or List of INT")

    for keyword in keywords:
        assert (
            keyword.lower() in msgs_text
        ), f'В сообщении {msg_idx} отсутствует ключевое слово "{keyword}"'


def verify_clicked_button_was_marked(new_kb, prev_kb, clicked_button_idx):
    assert (
        new_kb.rows[0][clicked_button_idx].text
        == "✔" + prev_kb.rows[0][clicked_button_idx].text
    ), "Нажатая кнопка не помечена"


def verify_numeric_kb_is_valid(kb, num_buttons):
    assert kb.num_buttons == num_buttons
    assert kb.rows[0][0].text == "1"
    assert kb.rows[0][num_buttons - 1].text == str(num_buttons)


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
