from datetime import date

import telebot

import config
import database

bot = telebot.TeleBot(config.data["token"])

# User registration in databse

@bot.message_handler(commands=["start"])
def start(message):
	keyboard = telebot.types.InlineKeyboardMarkup()
	button_yes = telebot.types.InlineKeyboardButton(text="Yes", callback_data="yes_reg")
	button_no = telebot.types.InlineKeyboardButton(text="No", callback_data="no_reg")
	keyboard.add(button_yes, button_no)
	bot.send_message(chat_id=message.chat.id, text="Hi, you want to register?", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "yes_reg")
def user_registration(call):
	users_in_bd = database.get_all_users()
	print(users_in_bd)
	if users_in_bd == []:
		user = (call.from_user.username, call.from_user.id, None, True)
		success = database.add_user(user)
	else:
		user = (call.from_user.username, call.from_user.id, None, False)
		success = database.add_user(user)
	if success == True:
		bot.send_message(chat_id=call.message.chat.id, text="You succes registered")
	elif success == False:
		bot.send_message(chat_id=call.message.chat.id, text="You are already registered")
	else:
		bot.send_message(chat_id=call.message.chat.id, text="Unknown error")


@bot.callback_query_handler(func=lambda call: call.data == "no_reg")
def not_registration(call):
	bot.send_message(chat_id=call.message.chat.id, text="Okey, for registration send '/start' again")

def check_admin(message):
	admins = database.get_admins()
	print(admins)
	if message.from_user.id in admins[0]:
		return True
	else:
		return False

# Add gym in database

@bot.message_handler(commands=["add_gym"])
def get_gym_info(message):
	if check_admin(message) == True:
		bot.send_message(chat_id=message.chat.id, text="Input name and count at the same time reservations for gym(name:count)")
		bot.register_next_step_handler(message, info_confirm)
	elif check_admin(message) == False:
		bot.send_message(chat_id=message.chat.id, text="Sorry, it's function can execute only user with status 'administrator'")

def info_confirm(message):
	list_info = message.text.split(":")
	info_str = f"Name GYM: {list_info[0]}\nCount reservations: {list_info[1]}"

	keyboard = telebot.types.InlineKeyboardMarkup()
	button_yes = telebot.types.InlineKeyboardButton(text="Yes", callback_data=f"yes_info:{list_info[0]}:{list_info[1]}")
	button_no = telebot.types.InlineKeyboardButton(text="No", callback_data="no_info")
	keyboard.add(button_yes, button_no)

	bot.send_message(chat_id=message.chat.id, text=info_str, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: "yes_info" in call.data)
def add_gym_in_database(call):
	name = call.data.split(":")[1]
	count_reservations = call.data.split(":")[2]

	gym = ( None, name, count_reservations, None,)

	success = database.add_gym(gym)

	if success == True:
		bot.send_message(chat_id=call.message.chat.id, text=f"Gym {name} with {count_reservations} reservations success added in database")
	else:
		bot.send_message(chat_id=call.message.chat.id, text="Unknown error")

#View all gyms

@bot.message_handler(commands=["all_gyms"])
def view_all_gyms(message):
	gyms_list = database.get_all_gyms()
	output = []
	for i in gyms_list:
		gym_id = f"ID: {i[0]}"
		gym_name = f"Name: {i[1]}"
		count_reserv = f"Count reservations: {i[2]}"
		all_reserv = f"Reservarions:\n {i[3]}\n\n"
		output.append("\n".join([gym_id, gym_name, count_reserv, all_reserv]))
	keyboard = telebot.types.InlineKeyboardMarkup()
	keyboard.add()
	bot.send_message(chat_id=message.chat.id, text="\n".join(output))

# View all users

@bot.message_handler(commands=["view_users"])
def view_all_user(message):
	print(check_admin(message))
	if check_admin(message) == True:
		user_list = database.get_all_users()
		output = []
		for i in user_list:
			user_id = f"ID: {i[1]}"
			username = f"User: {i[0]}"
			count_reserv = f"Count reservations: {i[2]}"
			is_admin = f"Admin: {i[3]}"
			output.append("\n".join([user_id, username, is_admin]))
		bot.send_message(chat_id=message.chat.id, text="\n".join(output))
	elif check_admin(message) == False:
		bot.send_message(chat_id=message.chat.id, text="Sorry, it's function can execute only user with status 'administrator'") 
bot.infinity_polling()