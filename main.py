# Here's so much govnocode but I've fok it's mouth and nose changing all of it.

import telebot
from telebot import types, TeleBot
import time

bot: TeleBot = telebot.TeleBot(
    '<TOKEN>')          # If you don't know what to do with that, read https://core.telegram.org/bots


@bot.message_handler(commands=['start'])  # Start op bot
def send_welcome(message):
    bot.send_message(message.chat.id, "Є контакт")       # It works


@bot.message_handler(commands=['newgame'])
def command_help(m):
    global cid
    cid = m.chat.id
    global players_passports
    players_passports = []
    keyboard = types.InlineKeyboardMarkup()
    kb1 = types.InlineKeyboardButton(text="Приєднатися до гри", callback_data="дата кнопки приєднатись")
    keyboard.add(kb1)
    global msg
    msg = bot.send_message(cid, "Всьо гатово і все в зборє", reply_markup=keyboard)  # All is ready to play


@bot.callback_query_handler(func=lambda c: True)
def ans(c):
    keyboard = types.InlineKeyboardMarkup()
    if c.data == "дата кнопки приєднатись":
        mona = True
        for i in players_passports:
            if c.from_user.id == i.id:
                mona = False
        if mona:
            bot.send_message(cid, f"+   {c.from_user.first_name}", reply_markup=keyboard)
            players_passports.append(c.from_user)


@bot.message_handler(commands=['startgame'])
def command_help(m):
    bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id,
                          text='Гра почалась, грають:\n' + ", ".join(
                              i.first_name for i in players_passports))  # Game has started, here are playing ...
    global players
    players = {}
    for i in players_passports:
        players[i.username] = 0
    bot.send_message(cid,
                     f"Всім видано по 0 гривнів\nСума звичайно вас не влаштовує, тож нехай кожен гравець сам зробить собі стартерпак")  # Everyone got 0 coins, so let every player make his own starterpack
    bot.send_message(cid,
                     "<b>Важно!</b>\n\nЩоб здійснити транзакцію, потрібно написати в чат за таким шаблоном:\n    @\"нікнейм отримувача\" \"cума гривнів\"\nМожна просто в банку взяти певну суму, написавши її сюди без ніків (той же стартерпак)\n  навіть штраф, поставивши перед сумою мінус.\nЯкщо діло дойшло до програшу, пиши команду /leavegame (не тицяй на неї блядь)", parse_mode="html")  # To make transaction, type @<username> <quantity of money> or just <quantity of money> optional with minus before -<quantity of money> pay fine
    bot.send_message(m.chat.id, "\n".join(i + " – " + str(players[i]) for i in players) + "\n\nУдачі")


@bot.message_handler(commands=['leavegame'])
def leave_game(m):
    print("Получилось")
    del players[m.from_user.username]
    bot.send_message(cid, f" {m.from_user.first_name} лівнув")  # Some player left
    if len(players) == 0:
        bot.send_message(cid, "Всі вийшли")
        bot.send_message(cid, "Кунець")                 # The end of the game


@bot.message_handler(content_types='text')
def payment(m):
    if m.from_user.username in players:
        if m.text[0] == "@" and " " in m.text and players[m.from_user.username] >= int(m.text[m.text.rfind(" "):]):
            try:
                players[m.text[1:m.text.find(" ")]] += int(m.text[m.text.rfind(" "):])
                players[m.from_user.username] -= int(m.text[m.text.rfind(" "):])
                bot.send_message(cid, "\n".join(i + " – " + str(players[i]) for i in players))
            except ValueError:
                bot.reply_to(m, "Неправильний формат написання суми транзакції")  # Non correct format of writing the sum of money
            except KeyError:
                bot.reply_to(m, "Неправильний формат написання нікнейму, або власник ніку не грає")  # Non correct format of writing the username
        elif m.text.isdigit() or m.text[0] == "-" and m.text[1:].isdigit():
            if m.from_user.username in players:
                try:
                    if m.text.isdigit():
                        players[m.from_user.username] += int(m.text)
                        bot.send_message(cid, "\n".join(i + " – " + str(players[i]) for i in players))
                    elif m.text[0] == "-" and m.text[1:].isdigit():
                        players[m.from_user.username] -= int(m.text[1:])
                        bot.send_message(cid, "\n".join(i + " – " + str(players[i]) for i in players))
                except ValueError:
                    bot.reply_to(m, "Неправильний формат написання суми транзакції")  # Non correct format of writing the sum of money
        elif players[m.from_user.username] <= int(m.text[m.text.rfind(" "):]):
            bot.reply_to(m, "Кредити в грі не передбачені")                 # No credits, player haven't enough money
    else:
        bot.reply_to(m, "Ти не в грі, не мішай людям грати")  # You are not in the game






bot.infinity_polling()
