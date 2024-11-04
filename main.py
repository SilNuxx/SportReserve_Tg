from datetime import date

import telebot

import config
import database

bot = telebot.TeleBot(config.data["token"])

# User registration in databse
@bot.message_handler(commands=["start"])
def start(message):
	keyboard = telebot.types.InlineKeyboardMarkup()
	button_yes = telebot.types.InlineKeyboardButton(text="Yes", callback_data="yes")
	button_no = telebot.types.InlineKeyboardButton(text="No", callback_data="no")
	keyboard.add(button_yes, button_no)
	bot.send_message(chat_id=message.chat.id, text="Hi, you want to register?", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "yes")
def user_registration(call):
	user = (call.from_user.username, call.from_user.id, str(date.today()))
	succes = database.add_user(user)
	if succes == True:
		bot.send_message(chat_id=call.message.chat.id, text="You succes registered")
	elif succes == False:
		bot.send_message(chat_id=call.message.chat.id, text="You failure registered")
	else:
		bot.send_message(chat_id=call.message.chat.id, text="Unknown error")

@bot.callback_query_handler(func=lambda call: call.data == "no")
def not_registration(call):
	bot.send_message(chat_id=call.message.chat.id, text="Okey, for registration send '/start' again")

# View available gym

bot.infinity_polling()