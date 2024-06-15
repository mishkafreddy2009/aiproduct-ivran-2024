import telebot
from time import sleep
from config import *
import requests
from telebot_calendar import Calendar, RUSSIAN_LANGUAGE, CallbackData
import datetime
from telebot.types import CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup

from model import send_to_gpt

calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1 = CallbackData("calendar_1", "action", "year", "month", "day")
calendar_2 = CallbackData("calendar_2", "action", "year", "month", "day")

bot = telebot.TeleBot('7046388530:AAFfosL3ANMOOWkwPVBp95YLU8yrMwGenZ0')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f"""Привет, @{message.from_user.username}\nГотов представить тебе актуальную информацию. Сначала выбери дату, а потом введи свой запрос""")
    global keyboard
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton("Выбрать начальную дату", callback_data="get-date-1"),
        telebot.types.InlineKeyboardButton("Выбрать конечную дату", callback_data="get-date-2"),
    )
    msg = bot.send_message(
        message.chat.id, "Выберите интересующий вас запрос:", reply_markup=keyboard
    )

def send_answer(message, date_start, date_end):
    bot.reply_to(message, f"Запрос принят в обработку.\nВременной промежуток от {str(date_start)} до {str(date_end)}")
    try:
        result = send_to_gpt(message.text, date_start, date_end)
        bot.reply_to(message, result)
    except:
        bot.reply_to(message, "Произошла ошибка при обработке запроса.")


@bot.message_handler(commands=["help"])
def send_help(message):
    bot.reply_to(message, f"""Список доступных комманд:\n\t/start - запустить бота\n\t/help - вызвать список доступных комманд""")


@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1.prefix) or call.data.startswith(calendar_2.prefix))
def callback_inline(call: CallbackQuery):
    """
    Processing inline callback requests for a calendar


    :param call:
    :return:
    """
    name, action, year, month, day = call.data.split(calendar_1.sep)
    date = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    if call.data.startswith(calendar_1.prefix):
        if action == "DAY":
            global date_strf_1
            date_strf_1 = date.strftime('%d.%m.%Y')
            bot.send_message(
                chat_id=call.from_user.id,
                text=f"Вы выбрали начальную дату: {date_strf_1}",
                reply_markup=keyboard,
            )
            print(f"{calendar_1}: Day: {date_strf_1}")
        elif action == "CANCEL":
            bot.send_message(
                chat_id=call.from_user.id,
                text="Отмена",
                reply_markup=ReplyKeyboardRemove(),
            )
            print(f"{calendar_1}: Отмена")
    else:
        if action == "DAY":
            global date_strf_2
            date_strf_2 = date.strftime('%d.%m.%Y')
            bot.send_message(
                chat_id=call.from_user.id,
                text=f"Вы выбрали начальную дату: {date_strf_1}\nВы выбрали конечную дату: {date_strf_2}",
                reply_markup=ReplyKeyboardRemove(),
            )
            print(f"{calendar_1}: Day: {date_strf_2}")
            msg = bot.send_message(chat_id=call.from_user.id, text="Теперь введите интересующий вас вопрос")
            bot.register_next_step_handler(msg, send_answer, date_strf_1, date_strf_2)
        elif action == "CANCEL":
            bot.send_message(
                chat_id=call.from_user.id,
                text="Отмена",
                reply_markup=ReplyKeyboardRemove(),
            )
            print(f"{calendar_1}: Отмена")


@bot.callback_query_handler(func=lambda call: call.data.startswith("get-date"))
def callback_inline(call: CallbackQuery):
    if call.data == "get-date-1":
        now = datetime.datetime.now()
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выберите дату начала",
            reply_markup=calendar.create_calendar(
                name=calendar_1.prefix,
                year=now.year,
                month=now.month,
            ),
        )

    if call.data == "get-date-2":
        now = datetime.datetime.now()
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выберите дату конца",
            reply_markup=calendar.create_calendar(
                name=calendar_2.prefix,
                year=now.year,
                month=now.month,
            ),
        )


bot.polling()
