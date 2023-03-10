from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from config import bot, ADMINS
from keyboards.client_kb import start_markup
from database.bot_db import sql_command_random, sql_command_delete
from parser.news import parser


# @dp.message_handler(commands=['start', 'help'])
async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Салалекум хозяин {message.from_user.first_name}",
                           reply_markup=start_markup)
    # await message.answer("This is an answer method")
    # await message.reply("This is a reply method")
    # CRUD

async def info_handler(message: types.Message):
    await message.answer("Сам разбирайся!")


# @dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("NEXT", callback_data='button_call_1')
    markup.add(button_call_1)

    question = "Какое пиво ты любишь?"
    answers = [
        "Svetloe",
        "Svetloe no filter",
        "Svetloe filter",
        "Temnoe",
        "Temnoe no filter",
        "Temnoe filter",
    ]
    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=5,
        explanation="оно вкусное",
        open_period=60,
        reply_markup=markup
    )


async def get_random_user(message: types.Message):
    random_user = await sql_command_random()
    markup = None
    if message.from_user.id in ADMINS:
        markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton(f"delete {random_user[2]}",
                                 callback_data=f"delete {random_user[0]}"))
    await message.answer_photo(
        random_user[-1],
        caption=f"{random_user[2]} {random_user[3]} {random_user[4]} "
                f"{random_user[5]}\n\n{random_user[1]}",
        reply_markup=markup)


async def complete_delete(call: types.CallbackQuery):
    await sql_command_delete(call.data.replace("delete ", ""))
    await bot.send_message(call.data.replace("delete ", ""), "Ваша анкета удалена!")
    await call.answer(text="Deleted!", show_alert=True)
    await bot.delete_message(call.from_user.id, call.message.message_id)


async def get_news(message: types.Message):
    news = parser()
    for i in news:
        await message.answer(
            f"{i['link']}\n\n"
            f"<b><a href='{i['link']}'>{i['title']}</a></b>\n"
            f"{i['description']}\n"
            f"{i['date_from_html']}\n",
            parse_mode=ParseMode.HTML
        )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start', 'help'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(info_handler, commands=['info'])
    dp.register_message_handler(get_random_user, commands=['get'])
    dp.register_callback_query_handler(complete_delete,
                                       lambda call: call.data and call.data.startswith("delete "))
    dp.register_message_handler(get_news, commands=['news'])
