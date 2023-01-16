from aiogram import types, Dispatcher
from config import bot, dp


# @dp.callback_query_handler(text="button_call_1")
async def quiz_2(call: types.CallbackQuery):
    question = "АТВИЧАЙ!"
    answers = [
        '[4]',
        '[8]',
        '[4, 6]',
        '[2, 4]',
        '[5]',
    ]

    photo = open("media/problem1.jpg", 'rb')
    await bot.send_photo(call.message.chat.id, photo=photo)

    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=3,
        explanation="оно вкусное",
        open_period=60,
    )


def register_handlers_callback(dp: Dispatcher):
    dp.register_callback_query_handler(quiz_2, text="button_call_1")
