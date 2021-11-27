import requests
import telebot
from telebot import types
import datetime
import math

import config
import rates


bot = telebot.TeleBot(config.TOKEN)

date = datetime.datetime.today()


@bot.message_handler(commands=["start"])
def start(m):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ["Купить ТАКА"]])
    keyboard.add(
        *[
            types.KeyboardButton(name)
            for name in ["Узнать курс на сегодня", "Связаться с нами"]
        ]
    )
    bot.send_message(
        m.chat.id,
        "Привет! Я помогу тебе поменять деньги! Выбери действие в меню",
        reply_markup=keyboard,
    )


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    if message.text == "Узнать курс на сегодня":
        taka = str(rates.load_exchange())
        time_now = date.strftime("%d-%m-%Y")
        times = str(rates.time_update())
        bot.send_message(
            message.from_user.id,
            "Сегодня, " + time_now + " курс Бангладешской таки - " + taka + " к рублю, "
            "последнее обновление курса в " + times,
        )

    elif message.text == "Купить ТАКА":
        if (
            int(date.strftime("%H%M")) >= config.tmaxx
            or int(date.strftime("%H%M")) <= config.tmin
        ):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ["Купить ТАКА"]])
            keyboard.add(
                *[
                    types.KeyboardButton(name)
                    for name in ["Узнать курс на сегодня", "Связаться с нами"]
                ]
            )
            bot.send_message(
                message.chat.id,
                str(message.from_user.first_name)
                + ", sorry, бот сейчас отдыхает, он проснется в восемь утра!",
                reply_markup=keyboard,
            )
        else:
            taka = str(rates.load_exchange())
            bot.send_message(
                message.from_user.id, "Текущий курс таки " + taka + " к рублю"
            )
            send = bot.send_message(message.from_user.id, "Сколько ты хочешь купить?")
            bot.register_next_step_handler(send, exchange)

    elif message.text == "ДА! Покупаю!":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[
                types.KeyboardButton(name)
                for name in ["Приду за деньгами", "Заказать доставку"]
            ]
        )
        keyboard.add(
            *[
                types.KeyboardButton(name)
                for name in ["Узнать курс на сегодня", "Связаться с нами"]
            ]
        )
        bot.send_message(
            message.from_user.id,
            "Как ты хочешь получить деньги?",
            reply_markup=keyboard,
        )

    elif message.text == "Нет, в другой раз":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["Купить ТАКА"]])
        keyboard.add(
            *[
                types.KeyboardButton(name)
                for name in ["Узнать курс на сегодня", "Связаться с нами"]
            ]
        )
        bot.send_message(
            message.from_user.id,
            "Очень жаль, пиши если нужны будут ТАКА!",
            reply_markup=keyboard,
        )
    elif message.text == "Заказать доставку":
        send = bot.send_message(message.from_user.id, "Напиши куда доставить деньги")
        bot.register_next_step_handler(send, delivery)

    elif message.text == "Приду за деньгами":
        global summa
        mess = (
            str(message.from_user.first_name)
            + " ник "
            + str(message.from_user.username)
            + " хочет купить "
            + str(summa)
            + " така, заберет сам, нужно с ним связаться"
        )
        requests.get(config.URL + mess)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["Купить ТАКА"]])
        keyboard.add(
            *[
                types.KeyboardButton(name)
                for name in ["Узнать курс на сегодня", "Связаться с нами"]
            ]
        )
        if (
            int(date.strftime("%H%M")) >= config.tmin
            and int(date.strftime("%H%M")) <= config.tmax
        ):
            bot.send_message(
                message.chat.id,
                str(message.from_user.first_name)
                + ", мы приняли твой заказ, забрать ТАКА можно на площадке, в офисе 1.1, предварительно свяжись с нами по телефону +88 013 13 408 417!",
                reply_markup=keyboard,
            )
        elif (
            int(date.strftime("%H%M")) >= config.tmax
            and int(date.strftime("%H%M")) <= config.tmaxx
        ):
            bot.send_message(
                message.chat.id,
                str(message.from_user.first_name)
                + ", мы приняли твой заказ, забрать ТАКА можно в Грин Сити, дом №13, предварительно свяжись с нами по телефону +88 013 13 408 417!",
                reply_markup=keyboard,
            )

    elif message.text == "Связаться с нами":
        if (
            int(date.strftime("%H%M")) >= config.tmaxx
            or int(date.strftime("%H%M")) <= config.tmin
        ):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ["Купить ТАКА"]])
            keyboard.add(
                *[
                    types.KeyboardButton(name)
                    for name in ["Узнать курс на сегодня", "Связаться с нами"]
                ]
            )
            bot.send_message(
                message.chat.id,
                str(message.from_user.first_name)
                + ", sorry, бот сейчас отдыхает, он проснется в восемь утра!",
                reply_markup=keyboard,
            )
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ["Купить ТАКА"]])
            keyboard.add(
                *[
                    types.KeyboardButton(name)
                    for name in ["Узнать курс на сегодня", "Связаться с нами"]
                ]
            )

            messcl = bot.send_message(
                message.chat.id,
                str(message.from_user.first_name)
                + ", укажи как с тобой связаться, напиши номер телефона или ник в телеграм",
                reply_markup=keyboard,
            )
            bot.register_next_step_handler(messcl, contact)

    elif message.text == "/time":
        bot.send_message(message.from_user.id, date.strftime("%H:%M"))

    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /start.")


def contact(message):
    if (
        message.text != "Узнать курс на сегодня"
        and message.text != "Купить ТАКА"
        and message.text != "Связаться с нами"
    ):
        mess = (
            str(message.from_user.first_name)
            + " хочет связаться, его контакты: "
            + str(message.text)
        )
        requests.get(config.URL + mess)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["Купить ТАКА"]])
        keyboard.add(
            *[
                types.KeyboardButton(name)
                for name in ["Узнать курс на сегодня", "Связаться с нами"]
            ]
        )
        bot.send_message(
            message.chat.id,
            str(message.from_user.first_name)
            + ", мы тебя услышали, сейчас с тобой свяжемся!",
            reply_markup=keyboard,
        )


def exchange(message):
    global summa
    summa = message.text
    try:
        summa = int(message.text)
    except ValueError:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["Купить ТАКА"]])
        keyboard.add(
            *[
                types.KeyboardButton(name)
                for name in ["Узнать курс на сегодня", "Связаться с нами"]
            ]
        )
        bot.send_message(
            message.from_user.id,
            'Похоже ты ввел не цифры, нажми кнопку "Купить ТАКА" снова!',
        )

    else:
        exc = int(message.text) * rates.load_exchange()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[
                types.KeyboardButton(name)
                for name in ["Нет, в другой раз", "ДА! Покупаю!"]
            ]
        )
        keyboard.add(
            *[
                types.KeyboardButton(name)
                for name in ["Узнать курс на сегодня", "Связаться с нами"]
            ]
        )
        bot.send_message(
            message.from_user.id,
            "Чтобы купить "
            + str(message.text)
            + " BDT"
            + " нужно "
            + str(math.ceil(exc))
            + " рублей. Готовы купить?",
            reply_markup=keyboard,
        )
        return exc


def delivery(message):
    global summa
    mess = (
        str(message.from_user.first_name)
        + " ник "
        + str(message.from_user.username)
        + " хочет купить "
        + str(summa)
        + " така, доставка в "
        + message.text
    )
    requests.get(config.URL + mess)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ["Купить ТАКА"]])
    keyboard.add(
        *[
            types.KeyboardButton(name)
            for name in ["Узнать курс на сегодня", "Связаться с нами"]
        ]
    )
    bot.send_message(
        message.chat.id,
        str(message.from_user.first_name)
        + ", мы приняли твой заказ, если есть вопросы свяжись с нами по телефону +88 013 13 408 417!",
        reply_markup=keyboard,
    )


bot.polling(none_stop=True)
