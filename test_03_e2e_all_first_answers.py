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

    res = await step00_start(controller, client)
    res = await step01_will_tak_part(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step02_run_1_mile(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step03_my_first_start(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step04_about_work_format_continue(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step05_give_agreement(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )

async def test_scenario02(controller, client):
    await controller.clear_chat()

    res = await step00_start(controller, client)
    res = await step01_will_tak_part(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step02_run_1_mile(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step03_my_first_start(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step04_about_work_format_continue(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step05_give_agreement(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step06_continue(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step07_stress_works_like_this_continue(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step08_want_to_know_more_about_stress(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step09_finish_with_stress_continue(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )

async def test_scenario03(controller, client):
    await controller.clear_chat()

    res = await step00_start(controller, client)
    res = await step01_will_tak_part(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step02_run_1_mile(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step03_my_first_start(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step04_about_work_format_continue(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step05_give_agreement(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step06_continue(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step07_stress_works_like_this_continue(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step08_want_to_know_more_about_stress(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step09_finish_with_stress_continue(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step10_qiuz1(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step11_qiuz2(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step12_qiuz3(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )
    res = await step13_qiuz4(
        controller, client, clicking_kb=res.inline_keyboards[-1]
    )




async def step00_start(controller, client):
    expected_msgs_number = 4
    keywords = [
        ["Привет", "марафон"],
        ["помогу", "марафон"],
        ["участвовать", "HONOR", "полезен"]
    ]

    async with controller.collect(
        count=expected_msgs_number
    ) as res:  # type: Response
        await controller.send_command("start")

    assert res.messages[0].photo
    assert 400 <= res.messages[0].photo.width <= 800

    verify_keywords_in_msg(res.messages, keywords)

    kb = res.inline_keyboards[0]
    assert kb.num_buttons == 2
    button1, button2 = kb.rows[0]

    assert button1.text == "Буду участвовать"
    assert button2.text == "Не в этот раз"

    return res


async def step01_will_tak_part(controller, client, clicking_kb):
    """Сообщ. с нажимаемой кнопкой: Вы будете участвовать в марафоне HONOR Сочи 20"""

    clicking_button_idx = 0  # кнопка буду участвовать

    expected_msgs_number = (
        2  # 1ое сообщение - изменяемая клава. 2е - само сообщение
    )
    msgs_keywords = [["Отлично", "дистанцию", "км"]]

    async with controller.collect(count=expected_msgs_number) as res:
        await clicking_kb.click(index=clicking_button_idx)

    verify_keywords_in_msg(res.messages, msgs_keywords)
    verify_numeric_kb_is_valid(res.inline_keyboards[-1], num_buttons=5)

    verify_clicked_button_was_marked(
        new_kb=res.inline_keyboards[0],
        prev_kb=clicking_kb,
        clicked_button_idx=clicking_button_idx,
    )
    return res


async def step02_run_1_mile(controller, client, clicking_kb):
    """Сообщ. с нажимаемой кнопкой: Какую дистанцию вы побежите на марафоне?"""
    clicking_button_idx = 0  # кнопка 1

    expected_msgs_number = 2
    msgs_keywords = [["опыт", "спортсмен"]]

    async with controller.collect(count=expected_msgs_number) as res:
        await clicking_kb.click(index=clicking_button_idx)

    verify_keywords_in_msg(res.messages, msgs_keywords)
    verify_numeric_kb_is_valid(res.inline_keyboards[-1], num_buttons=6)
    verify_clicked_button_was_marked(
        prev_kb=clicking_kb,
        new_kb=res.inline_keyboards[0],
        clicked_button_idx=clicking_button_idx,
    )

    return res


async def step03_my_first_start(controller, client, clicking_kb):
    """Сообщ. с нажимаемой кнопкой: Ваш соревновательный опыт"""
    clicking_button_idx = 0  # кнопка 1

    expected_msgs_number = 2
    msgs_keywords = [
        [],
    ]

    async with controller.collect(count=expected_msgs_number) as res:
        await clicking_kb.click(index=clicking_button_idx)

    verify_keywords_in_msg(res.messages, msgs_keywords)

    verify_clicked_button_was_marked(
        prev_kb=clicking_kb,
        new_kb=res.inline_keyboards[0],
        clicked_button_idx=clicking_button_idx,
    )

    return res


async def step04_about_work_format_continue(controller, client, clicking_kb):
    """Сообщ. с нажимаемой кнопкой: [текст про формат работы]"""

    clicking_button_idx = 0  # кнопка 1

    expected_msgs_number = 4
    msgs_keywords = [
        ["Прежде",'прочитайте'],
        ["прочли", "важно", "согласны"],
    ]

    async with controller.collect(count=expected_msgs_number) as res:
        await clicking_kb.click(index=clicking_button_idx)

    verify_keywords_in_msg(res.messages, msgs_keywords)

    verify_clicked_button_was_marked(
        prev_kb=clicking_kb,
        new_kb=res.inline_keyboards[0],
        clicked_button_idx=clicking_button_idx,
    )

    return res


async def step05_give_agreement(controller, client, clicking_kb):
    """Сообщ. с нажимаемой кнопкой: Вы прочли его? Это важно"""

    clicking_button_idx = 0

    expected_msgs_number = 3
    msgs_keywords = [
        ["Отлично", "начнем"],
        ["Старты", "стрессом"],
    ]

    async with controller.collect(count=expected_msgs_number) as res:
        await clicking_kb.click(index=clicking_button_idx)

    verify_keywords_in_msg(res.messages, msgs_keywords)
    verify_clicked_button_was_marked(
        prev_kb=clicking_kb,
        new_kb=res.inline_keyboards[0],
        clicked_button_idx=clicking_button_idx,
    )


    return res


async def step06_continue(controller, client, clicking_kb):
    """Сообщ. с нажимаемой кнопкой: Старты и соревнования часто являются стрессом дл"""

    clicking_button_idx = 0
    expected_msgs_number = 3
    msgs_keywords = [
        ["youtube"],
        ["стресс"],
    ]

    async with controller.collect(count=expected_msgs_number) as res:
        await clicking_kb.click(index=clicking_button_idx)

    verify_keywords_in_msg(res.messages, msgs_keywords)
    verify_clicked_button_was_marked(
        prev_kb=clicking_kb,
        new_kb=res.inline_keyboards[0],
        clicked_button_idx=clicking_button_idx,
    )

    return res

async def step07_stress_works_like_this_continue(controller, client, clicking_kb):
    """Сообщ. с нажимаемой кнопкой: Если коротко, стресс действует так:"""

    clicking_button_idx = 0

    expected_msgs_number = 2
    msgs_keywords = [
        ["Хотите", "узнать"],
    ]


    async with controller.collect(count=expected_msgs_number) as res:
        await clicking_kb.click(index=clicking_button_idx)

    verify_keywords_in_msg(res.messages, msgs_keywords)
    verify_clicked_button_was_marked(
        prev_kb=clicking_kb,
        new_kb=res.inline_keyboards[0],
        clicked_button_idx=clicking_button_idx,
    )

    return res


async def step08_want_to_know_more_about_stress(controller, client, clicking_kb):
    """Сообщ. с нажимаемой кнопкой: Хотите больше узнать про стресс, и то, как он влияет на вас?"""
    clicking_button_idx = 0

    expected_msgs_number = 4
    msgs_keywords = [
        ["Отлично", "лекция"],
        ["youtube"],
        ["стрессом","разобрались"],
    ]


    async with controller.collect(count=expected_msgs_number) as res:
        await clicking_kb.click(index=clicking_button_idx)


    verify_keywords_in_msg(res.messages, msgs_keywords)
    verify_clicked_button_was_marked(
        prev_kb=clicking_kb,
        new_kb=res.inline_keyboards[0],
        clicked_button_idx=clicking_button_idx,
    )

    return res


async def step09_finish_with_stress_continue(controller, client, clicking_kb):
    """Сообщ. с нажимаемой кнопкой: Cо стрессом мы разобрались!"""
    clicking_button_idx = 0

    expected_msgs_number = 3
    msgs_keywords = [
        ["Важный", "шаг", "на пути "],
        ["Почему", "занимаетесь"],
    ]


    async with controller.collect(count=expected_msgs_number) as res:
        await clicking_kb.click(index=clicking_button_idx)


    verify_keywords_in_msg(res.messages, msgs_keywords)
    verify_clicked_button_was_marked(
        prev_kb=clicking_kb,
        new_kb=res.inline_keyboards[0],
        clicked_button_idx=clicking_button_idx,
    )

    return res

async def step10_qiuz1(controller, client, clicking_kb):
    """Сообщ. с нажимаемой кнопкой: Почему Вы занимаетесь бегом?"""

    expected_msgs_number = 2
    msgs_keywords = [
        ["Какая", "цель"]
    ]


    await click_all_buttons(kb=clicking_kb)
    async with controller.collect(count=expected_msgs_number) as res:
        await clicking_kb.click(index=-1)
        # await clicking_kb.click(x=0, y=1)

    verify_keywords_in_msg(res.messages, msgs_keywords)

    for button_idx in range(clicking_kb.num_buttons-1): #-1 т.к. кнопка подтвердить исчезает
        verify_clicked_button_was_marked(
            prev_kb=clicking_kb,
            new_kb=res.inline_keyboards[0],
            clicked_button_idx=button_idx,
        )

    return res


async def step11_qiuz2(controller, client, clicking_kb):
    """Сообщ. с нажимаемой кнопкой: Какая у тебя цель на ближайший забег?"""

    expected_msgs_number = 2
    msgs_keywords = [
        ["Какие", "стресс-фактор"]
    ]


    await click_all_buttons(kb=clicking_kb)
    async with controller.collect(count=expected_msgs_number) as res:
        await clicking_kb.click(index=-1)

    verify_keywords_in_msg(res.messages, msgs_keywords)

    for button_idx in range(clicking_kb.num_buttons-1):
        verify_clicked_button_was_marked(
            prev_kb=clicking_kb,
            new_kb=res.inline_keyboards[0],
            clicked_button_idx=button_idx,
        )

    return res


async def step12_qiuz3(controller, client, clicking_kb):
    """Сообщ. с нажимаемой кнопкой: Какие стресс-факторы тебя могут отвлечь от хорошего настроя на старт?"""

    expected_msgs_number = 4
    msgs_keywords = [
        ["Ситуации", "напряжение"],
        ["Второй","шаг","диагностике",],
        ["Что","испытываете",],
    ]


    await click_all_buttons(kb=clicking_kb)
    async with controller.collect(count=expected_msgs_number) as res:
        await clicking_kb.click(index=-1)

    verify_keywords_in_msg(res.messages, msgs_keywords)

    for button_idx in range(clicking_kb.num_buttons-1):
        verify_clicked_button_was_marked(
            prev_kb=clicking_kb,
            new_kb=res.inline_keyboards[0],
            clicked_button_idx=button_idx,
        )

    return res


async def step13_qiuz4(controller, client, clicking_kb):
    """Сообщ. с нажимаемой кнопкой: Что чаще всего Вы испытываете перед стартом?"""

    expected_msgs_number = 5
    msgs_keywords = [
        ["Третий", "шаг"],
        ["Предлагаю", "найти", "состояние"],
        ["Вспомни", "выступление"],
        ["Когда", "наилучшем", "состоянии"],
    ]


    await click_all_buttons(kb=clicking_kb)
    async with controller.collect(count=expected_msgs_number) as res:
        await clicking_kb.click(index=-1)
        # await clicking_kb.click(x=0, y=1)

    verify_keywords_in_msg(res.messages, msgs_keywords)

    for button_idx in range(clicking_kb.num_buttons-1):
        verify_clicked_button_was_marked(
            prev_kb=clicking_kb,
            new_kb=res.inline_keyboards[0],
            clicked_button_idx=button_idx,
        )


    return res


class IncorrectPresButtonResultException(AssertionError):
    pass


async def click_all_buttons(kb):
    for button_idx, button in enumerate(kb.rows[0]):
        res = await kb.click(index=button_idx)
        verify_clicked_button_was_marked(
            prev_kb=kb,
            new_kb=res.inline_keyboards[0],
            clicked_button_idx=button_idx,
            mark="✓"
        )
        kb=res.inline_keyboards[0]


def verify_keywords_in_msg(all_messages, keywords_in_all_messages: list):
    for keywords_in_one_message in keywords_in_all_messages:
        for message in all_messages:

            if not message.text:
                continue
            for keyword in keywords_in_one_message:
                if keyword.lower() not in message.text.lower():
                    break
            else:
                break
        else:
            raise AssertionError(
                f'Набор слов {keywords_in_one_message} не всречается ни в одном сообщении')


def verify_clicked_button_was_marked(new_kb, prev_kb, clicked_button_idx, mark='✔'):
    assert (
        new_kb.find_button(index=clicked_button_idx).text
        == mark + prev_kb.find_button(index=clicked_button_idx).text
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
        max_wait=20.0,
        # wait_consecutive=0.8,
        wait_consecutive=10,
    )
    await c.initialize(start_client=False)
    yield c
