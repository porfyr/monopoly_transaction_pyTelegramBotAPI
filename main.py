import telebot
from telebot import types
bot = telebot.TeleBot('<TOKEN>')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Є контакт")


@bot.message_handler(commands=['newgame'])
def command_help(m):
    global cid
    cid = m.chat.id
    keyboard = types.InlineKeyboardMarkup()
    kb1 = types.InlineKeyboardButton(text="Приєднатися до гри", callback_data="дата кнопки приєднатись")
    keyboard.add(kb1)
    global players_passports
    players_passports = []
    global msg
    msg = bot.send_message(cid, "Всьо гатово і все в зборє", reply_markup=keyboard)       #All is ready to play

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
                          text='Гра почалась, грають:\n' + ", ".join(i.first_name for i in players_passports))       #Game has started, here are playing ...
    global players
    players = {}
    for i in players_passports:
        players[i.username] = int(1500)
    bot.send_message(m.chat.id, "Всім видано по 1500 гривнів, удачі")            #Everyone got 1500, good luck
    bot.send_message(cid, "Щоб здійснити транзакцію, потрібно написати в чат за таким шаблоном:\n@<нікнейм отримувача> <cума гривнів>") #To make transaction, pls type @<username> <quantity of money>
    bot.send_message(m.chat.id, "\n".join(i + " – " + str(players[i]) for i in players))

@bot.message_handler(commands=['leavegame'])
def leave_game(m):
    print("Получилось")
    del players[m.from_user.username]
    bot.send_message(cid, f" {m.from_user.first_name} лівнув")                #Some player left
    if len(players) == 0:
        bot.send_message(cid, "Кунець")                             #The end

@bot.message_handler(content_types='text')
def payment(m):
    if m.text[0] == "@" and " " in m.text:
        try:
            players[m.text[1:m.text.find(" ")]] += int(m.text[m.text.rfind(" "):])
            players[m.from_user.username] -= int(m.text[m.text.rfind(" "):])
            bot.send_message(m.chat.id, "\n".join(i+" – "+str(players[i]) for i in players))
        except ValueError:
            bot.send_message(cid, "Неправильний формат написання суми транзакції")        #Non correct format of writing the sum of money
        except KeyError:
            bot.send_message(cid, "Неправильний формат написання нікнейму, або власник ніку не грає")         #Non correct format of writing the username
    elif m.text.isdigit() or m.text[0] == "-" and m.text[1:].isdigit():
        if m.from_user.username in players:
            try:
                if m.text.isdigit():
                    players[m.from_user.username] += int(m.text)
                    bot.send_message(m.chat.id, "\n".join(i + " – " + str(players[i]) for i in players))
                elif m.text[0] == "-" and m.text[1:].isdigit():
                    players[m.from_user.username] -= int(m.text[1:])
                    bot.send_message(m.chat.id, "\n".join(i + " – " + str(players[i]) for i in players))
            except ValueError:
                bot.send_message(cid, "Неправильний формат написання суми транзакції")             #Non correct format of writing the sum of money
        else:
            bot.send_message(cid, "Ти не в грі, не мішай людям грати")               #You are not in the game






bot.infinity_polling()