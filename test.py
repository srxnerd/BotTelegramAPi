import os
from bs4 import BeautifulSoup
from requests import get
from inscriptis import get_text
from urlextract import URLExtract
from flask import Flask, request , g
from telebot  import types
import telebot
import re
import time
import sqlite3
import jdatetime

TOKEN = '901772617:AAFGnyuH8bwE_yOr-De2g9ntOttktkBFLlA'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
help = "hi welcom to my bot :) \n\n -------Python APi bot telegram--------"
def Create_db():
    #create sqlite3
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.executescript('''CREATE TABLE IF NOT EXISTS USER_ID_INT
             (ID PRIMARY KEY)''')
    conn.commit()
    conn.close()

@bot.message_handler(commands=['start'])
def command_start(m):
    Create_db()
    user_id_telegram = m.chat.id
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO USER_ID_INT VALUES (%i)" % (user_id_telegram))
    conn.commit()
    conn.close()
    cid2 = "@channelstibotdata"
    user_photo = bot.get_user_profile_photos(m.from_user.id)
    bot.send_photo(cid2,user_photo.photos[0][0].file_id)
    bot.send_message(cid2,"name: "+str(m.from_user.first_name))
    bot.send_message(cid2,"username: @"+str(m.from_user.username))
    bot.forward_message(cid2, m.chat.id, m.message_id)
    User_info = m.from_user.id
    bot.send_message(m.chat.id, "Hi Welcom \nfor get help plesae type: /help")
    bot.send_message(m.chat.id, "user info id: @"+str(m.from_user.username))
    if User_info == 943665008:
            bot.send_message(m.chat.id, "you are Admin bot")
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    reg_button = types.KeyboardButton(text="phone number", request_contact=True)
    keyboard.add(reg_button)
    if m.chat.type == "private":
        response = bot.send_message(m.chat.id,
                                    "You should share your phone number",
                                    reply_markup=keyboard)
    else:
        bot.send_message(m.chat.id, "You can not send your number in the group!")





@bot.message_handler(commands=['get'])
def command_start(m):
    if m.chat.id == 943665008:
        conn = sqlite3.connect("data.db")
        cursor = conn.execute("SELECT ID from USER_ID_INT")
        for row in cursor:
            data_db = str(row[0])
            bot.send_message(m.chat.id, data_db)
    else:
        bot.send_message(m.chat.id, "just admin bot")
@bot.message_handler(commands=['pro'])
def prifile(m):
    cid2 = "@channelstibotdata"
    cid = 943665008
    user_photo = bot.get_user_profile_photos(m.from_user.id)
    bot.send_photo(cid2,user_photo.photos[0][0].file_id)



@bot.message_handler(commands=['admin'])
def command_start(m):
    User_info = m.from_user.id
    if User_info == 943665008:
        bot.send_message(m.chat.id, "weclome admin")
    else:
        print("you are not admind")
@bot.message_handler(commands=['help'])
def command_start(m):
    bot.send_message(m.chat.id, help)

@bot.message_handler(commands=["time"])
def time(message):
    time_today = jdatetime.date.today()
    bot.send_message(message.chat.id, time_today)


@bot.message_handler(commands=["list"])
def New_movie(message):
        def sabamovie_get_title(PageName, Domain):
            url = Domain
            Url_Request = get(url).text
            Soup = BeautifulSoup(Url_Request, "lxml")
            Soup_Find = Soup.find_all("h2", class_="title-text")
            Sting_soup = get_text(str(Soup_Find))
            Sting_soup = Sting_soup.replace("[","")
            Sting_soup = Sting_soup.replace("]","")
            Sting_soup = Sting_soup.replace(",","")
            bot.send_message(message.chat.id, Sting_soup)
        page_1 = sabamovie_get_title("1","http://sabamovie.net")
        page_2 = sabamovie_get_title("2","http://sabamovie.net/page/2/")

@bot.message_handler(content_types=['audio', 'document', 'photo', 'video', 'video_note', 'voice', 'location', 'contact'])
def handle_docs_audio(message):
	bot.forward_message("@channelstibotdata", message.chat.id, message.message_id)




@bot.message_handler(commands=["links"])
def New_movie_links(message):
    def sabamovie_get_title(PageName, Domain):
        extract = URLExtract()
        url = Domain
        Url_Request = get(url).text
        Soup = BeautifulSoup(Url_Request, "lxml")
        Soup_Find = Soup.find_all("h2", class_="title-text")
        Url_get = extract.find_urls(str(Soup_Find))
        for url_page in Url_get:
            ulrs = url_page
            bot.send_message(message.chat.id, ulrs)
    page_1 = sabamovie_get_title("1","http://sabamovie.net")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, "not found message")


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://immense-brushlands-05749.herokuapp.com/' + TOKEN)
    return "Welcome to Bot telegram", 200



if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
