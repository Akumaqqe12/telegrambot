import sqlite3
import telebot
from telebot import types
from dotenv import dotenv_values
import datetime

config = dotenv_values(".env")
bot = telebot.TeleBot(config.get("TOKEN"))


def executeAll(request):
    connection = sqlite3.connect(config.get('DB_NAME'))
    cursor = connection.cursor()
    cursor.execute(request)
    data = cursor.fetchall()
    connection.close()
    return data

def executeOne(request):
    connection = sqlite3.connect(config.get('DB_NAME'))
    cursor = connection.cursor()
    cursor.execute(request)
    data = cursor.fetchone()
    connection.close()
    return data

print("Работает, пока без ошибок")

# стартуем
@bot.message_handler(commands = ["start", "zxc"])
def zxc(message):
    user_id = message.from_user.id
    balance = 0
    connection = sqlite3.connect(config.get("DB_NAME"))
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user_exists = cursor.fetchone()
    
    if not user_exists:
        cursor.execute("INSERT INTO users (id, balance) VALUES (?, ?)", (user_id, balance))
    connection.commit()
    connection.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Менюшка", callback_data = "menu"))
    markup.add(types.InlineKeyboardButton("Всё то на что ты всрал бабки", callback_data = "history"))
    markup.add(types.InlineKeyboardButton("Чекни баланс", callback_data = "balance"))
    markup.add(types.InlineKeyboardButton("Закинь балик", callback_data = "addbal"))
    bot.send_photo(message.chat.id, photo=open("./zxcat.png",  "rb"), caption=f"Привет, {message.chat.first_name}\nТы попал в лучший магазин дед инсайд шмоток в РФ zxclavka!",reply_markup=markup)

# Менюшка йоу
@bot.callback_query_handler(func = lambda call: call.data == "menu")
def qwe(call):
   if call.data == "menu":
       markup = types.InlineKeyboardMarkup()
       markup.add(types.InlineKeyboardButton("Наша ,база", url = "https://clck.ru/379ZNK"))
       markup.add(types.InlineKeyboardButton("Деньги отправлять сюда", callback_data = "rec"))
       markup.add(types.InlineKeyboardButton("Бэкаем бро", callback_data = "nazad"))
       markup.add(types.InlineKeyboardButton("Наши шмотки", callback_data = "shmot"))
       bot.send_message(call.message.chat.id, parse_mode = "html", text = "Хотел меню, на те меню, делай че хочешь", reply_markup=markup)

# Голда на балике
@bot.callback_query_handler(func=lambda call: call.data == "balance")
def qqe(call):
    if call.data == "balance":
        result = executeAll(f"SELECT balance FROM users WHERE id = {call.message.chat.id}")
        if result:
            balance = result[0]
            bot.send_message(call.message.chat.id, "Твои бабки: {}".format(balance))

# Закидываем голду на балик
@bot.callback_query_handler(func=lambda call: call.data == "addbal")
def wwq(call):
   if call.data == "addbal":
        connection = sqlite3.connect(config.get("DB_NAME"))
        cursor = connection.cursor()
        user_id = call.from_user.id
        cursor.execute(f"SELECT balance FROM users WHERE id = {user_id}")
        result = cursor.fetchone()
        if result:
            balance = result[0]
            bot.send_message(call.message.chat.id, "У тя щас вот сток голды: {}".format(balance))
            bot.send_message(call.message.chat.id, "А мама не наругает, бабки сливаешь:")
            bot.register_next_step_handler(call.message, eew)

def eew(message):
        cash = int(message.text)
        user_id = message.from_user.id
        connection = sqlite3.connect(config.get("DB_NAME"))
        cursor = connection.cursor()
        cursor.execute(f"SELECT balance FROM users WHERE id = {user_id}")
        result = cursor.fetchone()
        if result:
            balance = result[0]
            if cash > 0:
                ybal = balance + cash
                cursor.execute(f"UPDATE users SET balance = {ybal} WHERE id = {user_id}")
                connection.commit()
                connection.close()
                bot.send_message(message.chat.id, "Охх бл мать точно по жопе за такое даст бро, ты слил нам: {}".format(ybal))

# История как история че бухтеть то
@bot.callback_query_handler(func=lambda call: call.data == "history")
def qqw(call):
    if call.data == "history":
        user_id = call.from_user.id
        connection = sqlite3.connect(config.get("DB_NAME"))
        cursor = connection.cursor()
        cursor.execute("SELECT * from bills WHERE user_id=?", (user_id,))
        bills = cursor.fetchall()
        zxz = "Ты прикупил:\n"
        for bill in bills:
            zxz += "Ты: {user_id}, Шмотка: {item_id}, Времечко: {date}\n".format(user_id=user_id, item_id=bill[1], date=bill[2])
        cursor.close()
        connection.close()
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("ВЕРНИСЬ ФРОДО", callback_data="nazad1")
        markup.add(btn1)
        bot.send_message(call.message.chat.id, zxz, reply_markup=markup)

# Бэк на старт
@bot.callback_query_handler(func=lambda call: call.data == "nazad")
def qqq(call):
   if call.data == "nazad":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Менюшка", callback_data = "menu"))
        markup.add(types.InlineKeyboardButton("Всё то на что ты всрал бабки", callback_data = "history"))
        markup.add(types.InlineKeyboardButton("Чекни баланс", callback_data = "balance"))
        markup.add(types.InlineKeyboardButton("Закинь балик", callback_data = "addbal"))
        bot.send_photo(call.message.chat.id, photo=open("./zxcat.png",  "rb"), caption=f"Привет, {call.message.chat.first_name}\nТы попал в лучший магазин дед инсайд шмоток в РФ zxclavka!",reply_markup=markup)

# Товарчики бананчикиии
@bot.callback_query_handler(func=lambda call: call.data == "shmot")
def eeq(call):
    connection = sqlite3.connect(config.get("DB_NAME"))
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM categories")
    data = cursor.fetchall()
    connection.close()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("ВЕРНИСЬ ФРОДО", callback_data="nazad2"))
    for item in data:
        id, type = item
        markup.add(types.InlineKeyboardButton(type, callback_data=f"category_{id}"))
    bot.send_message(call.message.chat.id, text = "Че смотреть будем?:", reply_markup=markup)

# бЕЖИМ В КАТЕГОРИЮ
@bot.callback_query_handler(func=lambda call: call.data.startswith("category_"))
def asdw(call):
    category_id = call.data.split("_")[1]
    connection = sqlite3.connect(config.get("DB_NAME"))
    cursor = connection.cursor()
    query = f"""
               SELECT items.id, items.name
               FROM items
               INNER JOIN categories ON items.category_id = categories.id
               WHERE categories.id = {category_id}
               """
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("ВЕРНИСЬ ФРОДО", callback_data="back"))
    for item in data:
        item_id, item_name = item
        markup.add(types.InlineKeyboardButton(item_name, callback_data=f"item_{item_id}"))

    bot.send_message(call.message.chat.id, text = "Выбирай в чем позориться будешь:", reply_markup = markup)   

# СМОТРИМ ТОВАР БЛЯТЬ Я ЗАЕБАЛСЯ ПОМОГИТЕ
@bot.callback_query_handler(func=lambda call: call.data.startswith("item_"))
def lalala(call):
    connection = sqlite3.connect(config.get("DB_NAME"))
    cursor = connection.cursor()
    item_id = call.data.split("_")[1]
    query = f"""
            SELECT name, price, photo
            FROM items
            WHERE id = {item_id}
            """
    cursor.execute(query)
    data = cursor.fetchone()
    item_name, item_price, item_photo = data
    bot.send_photo(call.message.chat.id, photo=open(f"{item_photo}.jpg  ", "rb"), caption=f"Имя шмотки: {item_name}\nЦенник: {item_price}")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("ВЕРНИСЬ ФРОДО", callback_data="nazad"))
    markup.add(types.InlineKeyboardButton("Бай итем", callback_data=f"buy_{item_id}"))
    bot.send_message(call.message.chat.id, "Отвечаю мать прихлопнет, ПОКУПАЙ))):", reply_markup=markup)

# БАЙ ИТЕМ
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def pupuuu(call):
    connection = sqlite3.connect(config.get("DB_NAME"))
    cursor = connection.cursor()
    user_id = call.from_user.id
    item_id = call.data.split("_")[1]
    
    item_query = """
            SELECT name, price
            FROM items
            WHERE id = ?"""
    cursor.execute(item_query, (item_id,))
    item_data = cursor.fetchone()
    item_name, item_price_str = item_data
    item_price = int(item_price_str)
    
    balance_query = """
            SELECT balance
            FROM users
            WHERE id = ?"""
    cursor.execute(balance_query, (user_id,))
    user_balance = cursor.fetchone()[0]
    
    if user_balance >= item_price:
        new_balance = user_balance - item_price
        update_query = """
                   UPDATE users
                   SET balance = ?
                   WHERE id = ?"""
        cursor.execute(update_query, (new_balance, user_id))

        insert_query = """
                   INSERT INTO bills (user_id, item_id, date)
                   VALUES (?, ?, CURRENT_TIMESTAMP)"""
        cursor.execute(insert_query, (user_id, item_id))

        connection.commit()

        bot.send_message(call.message.chat.id, "Молодец дебил ты просрал мамины деньги, гордись собой")
    else:
        bot.send_message(call.message.chat.id, "МАТЬ ОБОКРАЛ ТАК ЕЩЁ И НЕ ХВАТАЕТ")

# бэк из меню на базу
@bot.callback_query_handler(func=lambda call: call.data == "zazaza")
def pupa(call):
    if call.data == "zazaza":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Наша ,база", url = "https://clck.ru/379ZNK"))
        markup.add(types.InlineKeyboardButton("Деньги отправлять сюда", callback_data = "rec"))
        markup.add(types.InlineKeyboardButton("Бэкаем бро", callback_data = "nazad"))
        markup.add(types.InlineKeyboardButton("Наши шмотки", callback_data = "shmot"))
        bot.send_message(call.message.chat.id, parse_mode = "html", text = "Хотел меню, на те меню, делай че хочешь", reply_markup=markup)

# бэк из товаров в меню
@bot.callback_query_handler(func=lambda call: call.data == "lopll")
def sasaa(call):
   if call.data == "lopll":
       markup = types.InlineKeyboardMarkup()
       markup.add(types.InlineKeyboardButton("Наша ,база", url = "https://clck.ru/379ZNK"))
       markup.add(types.InlineKeyboardButton("Деньги отправлять сюда", callback_data = "rec"))
       markup.add(types.InlineKeyboardButton("Бэкаем бро", callback_data = "nazad"))
       markup.add(types.InlineKeyboardButton("Наши шмотки", callback_data = "shmot"))
       bot.send_message(call.message.chat.id, parse_mode = "html", text = "Хотел меню, на те меню, делай че хочешь", reply_markup=markup)

# реквезиты так сказать
@bot.callback_query_handler(func=lambda call: call.data == "rec")
def akumaqqe(call):
   if call.data == "rec":
       markup = types.InlineKeyboardMarkup()
       btn2 = types.InlineKeyboardButton("ВЕРНИСЬ ФРОДО", callback_data="zxckid")
       markup.add(btn2)
       bot.send_message(call.message.chat.id, text = "Ну а че ты хотел это тестовый бот тут\nТут нет реквезитов", reply_markup = markup)

# с реков в меню
@bot.callback_query_handler(func=lambda call: call.data == "zxckid")
def zxcmama(call):
   if call.data == "zxckid":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Наша ,база", url = "https://clck.ru/379ZNK"))
        markup.add(types.InlineKeyboardButton("Деньги отправлять сюда", callback_data = "rec"))
        markup.add(types.InlineKeyboardButton("Бэкаем бро", callback_data = "nazad"))
        markup.add(types.InlineKeyboardButton("Наши шмотки", callback_data = "shmot"))
        bot.send_message(call.message.chat.id, parse_mode = "html", text = "Хотел меню, на те меню, делай че хочешь", reply_markup=markup)


@bot.message_handler()
def send_text(message):
    bot.send_message(message.chat.id, "Больной? Давай без твоих пошлостей")
       
bot.polling(none_stop=True, interval=0)
