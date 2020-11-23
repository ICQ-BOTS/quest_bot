from random import randint
from tarantool_utils import *
from config import *
import json
import sys
import os
import asyncio


async def default_command(bot, event):
	user = User(user_id=event.data['from']['userId'])
	# Если админ создаёт новый квест
	if user.type_action == 'add_new_quest':
		await add_new_quest(bot, event, is_callback=False)
	# Если чел в главном меню
	elif user.type_action == 'edit_text':
		await edit_text(bot, event)
	elif user.type_action == 'add_button':
		await add_button(bot, event)
	elif user.type_action == 'go_message':
		await go_message(bot, event)
	elif user.type_action == 'binding_button' or user.type_action == 'ID_button':
		await binding_button(bot, event)
	elif user.type_action == 'add_button_sleep' or user.type_action == 'sleep_button':
		await add_button_sleep(bot, event)
	elif user.type_action == 'add_message_sleep':
		await add_message_sleep(bot, event)
	elif user.type_action == 'add_message_binding':
		await add_message_binding(bot, event)
	elif user.type_action == 'mailing':
		await mailing(bot, event)
	elif user.message_id == 0:
		inline_keyboard_markup = []
		# Перебор всех квестов
		for c in space_quest_button.select():
			if c[1]:
				inline_keyboard_markup.append([{"text": c[2], "callbackData": c[3]}])
			elif user.user[0][5]:
				inline_keyboard_markup.append([{"text": c[2], "callbackData": c[3], "style": "primary"}])
				inline_keyboard_markup.append([{"text": "Опубликовать "+ c[2], "callbackData": "public_"+ str(c[0]), "style": "attention"}])
		# Админские команды
		if user.user[0][5]:
			for c in new_quest_list:
				inline_keyboard_markup.append(c)
		await send_mes(bot, event, 
			chat_id=event.data['from']['userId'], 
			text="Привет! Это текстовые квесты, выбирай сюжет.", 
			inline_keyboard_markup=json.dumps(inline_keyboard_markup) if len(inline_keyboard_markup) >= 1 else None, 
			user=user
		)
	else:
		# Иначе выдаём им его квест
		mes = space_message.select(user.message_id)[0]
		await send_type_text(bot, event, mes, user=user)


async def mailing(bot, event):
	user_id = event.data['from']['userId']
	user = User(user_id=user_id)	
	if event.type.value == 'callbackQuery':
		await bot.answer_callback_query(query_id=event.data['queryId'])
		# Если админ нажал кнопку
		#end_id_send_message
		user.user[0][3]	= 0	
		#type_action
		user.user[0][4] = 'mailing'
		await bot.send_text(
			chat_id=user_id,
			text="Напишите текст, для рассылки"
		)
		user.save()
	else:
		users = space_user.select()
		time_mailing = float(len(users)) + (float(len(users)) * 0.15)
		await bot.send_text(
			chat_id=user_id,
			text=f"Начинаю рассылку, примерное время рассылки - {round(time_mailing, 5)} сек."
		)
		user.user[0][4] = 'None'
		user.save()
		for c in users:
			await bot.send_text(
				chat_id=c[0],
				text=event.text
			)
			await asyncio.sleep(1)
		await bot.send_text(
			chat_id=user_id,
			text="Закончил рассылку"
		)			

async def message_quest(bot, event, select_id=None, user=None):
	user_id = event.data['from']['userId']
	if user is None:
		user = User(user_id=user_id)
	#Проверка, событие кнопка или новое сообщение
	if select_id is None:
		await bot.answer_callback_query(query_id=event.data['queryId'])
		args = event.data['callbackData'].split('_')
		if user.quest_id == 0 and user.message_id == 0 and user.user[0][7].get(int(args[1])):		
			select_id = user.user[0][7][int(args[1])]
		else:
			select_id = int(args[2])
	mes = space_message.select(int(select_id))[0]
	inline_keyboard_markup = list(mes[4]) if len(mes[4]) >= 1 else []
	for c in standard_button_list:
		inline_keyboard_markup.append(c)
	if mes[2] == 'final' and not user.user[0][5]:
		pass
	if user.user[0][5]:
		for c in message_quest_list:
			inline_keyboard_markup.append(c)
		mes[3] = f"message ID: {mes[0]}\n{mes[3]}"
	#quest_id
	user.user[0][1] = mes[1]
	user.user[0][2] = mes[0]
	user.save()
	await send_mes(bot, event, 
			chat_id=user_id, 
			text=mes[3], 
			inline_keyboard_markup=json.dumps(inline_keyboard_markup), 
			user=user
		)


async def start_quest(bot, event):
	#Возращаем человека в начало сюжета
	await bot.answer_callback_query(query_id=event.data['queryId'])
	user = User(user_id=event.data['from']['userId'])
	quest_button = space_quest_button.select(user.user[0][1])
	user.user[0][7].pop(user.quest_id, None)
	user.user[0][2] = quest_button[0][3].split('_')[-1]
	await message_quest(bot, event, select_id=quest_button[0][3].split('_')[-1], user=user)


async def main(bot, event):
	#Возращаем человека в главное меню
	await bot.answer_callback_query(query_id=event.data['queryId'])
	user = User(user_id=event.data['from']['userId'])
	#message_id
	user.user[0][7][user.quest_id] = user.message_id
	user.user[0][1] = 0
	user.user[0][2] = 0
	user.save()
	await default_command(bot, event)


async def public_quest(bot, event):
	args = event.data['callbackData'].split('_')
	space_quest_button.update(int(args[1]), [('=', 1, True)])
	await bot.answer_callback_query(query_id=event.data['queryId'], text="Опубликовал!", show_alert=True)
	await default_command(bot, event)


async def sleep_message(bot, event, select_id=None, user=None):
	user_id = event.data['from']['userId']
	if user is None:
		user = User(user_id=user_id)
	#Проверка, событие кнопка или новое сообщение
	if select_id is None:
		await bot.answer_callback_query(query_id=event.data['queryId'])
		args = event.data['callbackData'].split('_')
		mes = space_message.select(int(args[2]))[0]
	else:
		mes = space_message.select(int(select_id))[0]
	inline_keyboard_markup = []
	if user.user[0][5]:
		for c in sleep_message_quest_list:
			inline_keyboard_markup.append(c)
		mes[3] = f"message ID: {mes[0]}\n{mes[3]}"	
	user.user[0][1] = mes[1]
	user.user[0][2] = mes[0]
	await send_mes(bot, event, 
			chat_id=user_id, 
			text=mes[3], 
			inline_keyboard_markup=json.dumps(inline_keyboard_markup) if len(inline_keyboard_markup) >= 1 else None, 
			user=user
		)
	if mes[4][0]['sleep'] >= 1 and not user.user[0][5]:
		await asyncio.sleep(mes[4][0]['sleep'])
	if not (mes[4][0]['transfer'] is None) and not user.user[0][5]:
		mes = space_message.select(int(mes[4][0]['transfer']))[0]
		await send_type_text(bot, event, mes, user=user)
		user.user[0][1] = mes[1]
		user.user[0][2] = mes[0]
	user.save()


async def send_type_text(bot, event, mes, user=None):
	if mes[2] == 'message' or mes[2] == 'final':
		await message_quest(bot, event, select_id=mes[0], user=user)
	elif mes[2] == 'sleep':
		await sleep_message(bot, event, select_id=mes[0], user=user)


async def add_message_sleep(bot, event):
	user_id = event.data['from']['userId']
	user = User(user_id=user_id)	
	if event.type.value == 'callbackQuery':
		await bot.answer_callback_query(query_id=event.data['queryId'])
		# Если админ нажал кнопку
		#end_id_send_message
		user.user[0][3]	= 0	
		#type_action
		user.user[0][4] = 'add_message_sleep'
		await bot.send_text(
			chat_id=user_id,
			text="Напишите задержку в секундах"
		)
		user.save()
	else:
		if event.text.isdigit():
			mes = space_message.select(user.user[0][2])[0]
			mes[4][0]['transfer'] = add_message(
					quest_id=mes[1], 
					type_mes='sleep',
					buttons=[{'sleep': int(event.text), 'transfer': None}]
				)[0]
			space_message.replace(mes)
			user.user[0][4] = 'None'
			await message_quest(bot, event, select_id=mes[4][0]['transfer'], user=user)	
		else:
			await bot.send_text(
					chat_id=user_id,
					text="Напишите цифрами)"
				)		
		

async def add_message_binding(bot, event):
	user_id = event.data['from']['userId']
	user = User(user_id=user_id)	
	if event.type.value == 'callbackQuery':
		await bot.answer_callback_query(query_id=event.data['queryId'])
		# Если админ нажал кнопку
		#end_id_send_message
		user.user[0][3]	= 0	
		#type_action
		user.user[0][4] = 'add_message_binding'
		await bot.send_text(
			chat_id=user_id,
			text="Напишите messge ID"
		)
		user.save()
	else:
		if event.text.isdigit():
			mes = space_message.select(user.user[0][2])[0]
			if len(mes) >= 1:
				mes[4][0]['transfer'] = int(event.text)
				space_message.replace(mes)
				mes2 = space_message.select(mes[4][0]['transfer'])[0]
				await send_type_text(bot, event, mes2, user=user)			
			else:
				await bot.send_text(
					chat_id=user_id,
					text="Message ID не существует!"
				)
		else:
			await bot.send_text(
					chat_id=user_id,
					text="Напишите цифрами)"
				)	


async def add_message_bot(bot, event):
	user_id = event.data['from']['userId']
	user = User(user_id=user_id)	
	mes = space_message.select(user.user[0][2])[0]
	mes[4][0]['transfer'] = add_message(quest_id=mes[1])[0]	
	space_message.replace(mes)
	await message_quest(bot, event, select_id=mes[4][0]['transfer'], user=user)


async def further(bot, event):
	user = User(user_id=event.data['from']['userId'])
	mes = space_message.select(user.user[0][2])[0]
	mes = space_message.select(mes[4][0]['transfer'])[0]
	await send_type_text(bot, event, mes, user=user)


async def add_button_sleep(bot, event):
	user_id = event.data['from']['userId']
	user = User(user_id=user_id)	
	if event.type.value == 'callbackQuery':
		await bot.answer_callback_query(query_id=event.data['queryId'])
		# Если админ нажал кнопку
		#end_id_send_message
		user.user[0][3]	= 0	
		#type_action
		user.user[0][4] = 'sleep_button'
		await bot.send_text(
			chat_id=user_id,
			text="Напишите задержку в секундах"
		)
		user.save()
	else:
		if user.user[0][4] == 'sleep_button':
			if event.text.isdigit():
				user.user[0][6] = event.text
				user.user[0][4] = 'add_button_sleep'
				await bot.send_text(
					chat_id=user_id,
					text="Напишите название кнопки"
				)	
				user.save()				
			else:
				await bot.send_text(
						chat_id=user_id,
						text="Напишите цифрами)"
					)			
		else:
			mes = space_message.select(user.user[0][2])[0]
			new_mes = add_message(
					quest_id=mes[1], 
					type_mes='sleep',
					buttons=[{'sleep': int(user.user[0][6]), 'transfer': None}]
				)[0]
			mes[4].append([{"text": event.text, "callbackData": f"sleepMessage_{mes[1]}_{new_mes}"}])
			space_message.replace(mes)
			user.user[0][4] = 'None'
			user.user[0][6] = ''
			await message_quest(bot, event, select_id=mes[0], user=user)


async def go_message(bot, event):
	user_id = event.data['from']['userId']
	user = User(user_id=user_id)	
	if event.type.value == 'callbackQuery':
		await bot.answer_callback_query(query_id=event.data['queryId'])
		# Если админ нажал кнопку
		#end_id_send_message
		user.user[0][3]	= 0	
		#type_action
		user.user[0][4] = 'go_message'
		await bot.send_text(
			chat_id=user_id,
			text="Напишите message ID"
		)
		user.save()
	else:
		if event.text.isdigit():
			mes = space_message.select(int(event.text))
			if len(mes) >= 1:
				user.user[0][4] = 'None'
				await send_type_text(bot, event, mes[0], user=user)
			else:
				await bot.send_text(
					chat_id=user_id,
					text="Message ID не существует!"
				)
		else:
			await bot.send_text(
					chat_id=user_id,
					text="Напишите цифрами)"
				)						


async def binding_button(bot, event):
	user_id = event.data['from']['userId']
	user = User(user_id=user_id)	
	if event.type.value == 'callbackQuery':
		await bot.answer_callback_query(query_id=event.data['queryId'])
		# Если админ нажал кнопку
		#end_id_send_message
		user.user[0][3]	= 0	
		#type_action
		user.user[0][4] = 'ID_button'
		await bot.send_text(
			chat_id=user_id,
			text="Напишите message ID"
		)
		user.save()
	else:
		if user.user[0][4] == 'ID_button':
			if event.text.isdigit():
				mes = space_message.select(int(event.text))
				if len(mes) >= 1:
					user.user[0][6] = event.text
					user.user[0][4] = 'binding_button'
					await bot.send_text(
						chat_id=user_id,
						text="Напишите название кнопки"
					)	
					user.save()				
				else:
					await bot.send_text(
						chat_id=user_id,
						text="Message ID не существует!"
					)
			else:
				await bot.send_text(
						chat_id=user_id,
						text="Напишите цифрами)"
					)
		else:
			mes = space_message.select(user.user[0][2])[0]
			mes[4].append([{"text": event.text, "callbackData": f"message_{mes[1]}_{int(user.user[0][6])}"}])
			space_message.replace(mes)
			user.user[0][4] = 'None'
			user.user[0][6] = ''
			await message_quest(bot, event, select_id=mes[0], user=user)


async def del_button(bot, event):
	await bot.answer_callback_query(query_id=event.data['queryId'])
	user_id = event.data['from']['userId']
	user = User(user_id=user_id)
	mes = space_message.select(user.user[0][2])[0]
	for c in mes[4]:
		space_message.delete(int(c[0]["callbackData"].split('_')[-1]))
	mes[4] = []
	space_message.replace(mes)
	await message_quest(bot, event, select_id=mes[0], user=user)


async def add_button(bot, event):
	user_id = event.data['from']['userId']
	user = User(user_id=user_id)	
	if event.type.value == 'callbackQuery':
		await bot.answer_callback_query(query_id=event.data['queryId'])
		# Если админ нажал кнопку
		#end_id_send_message
		user.user[0][3]	= 0	
		#type_action
		user.user[0][4] = 'add_button'
		await bot.send_text(
			chat_id=user_id,
			text="Напишите название кнопки"
		)
		user.save()
	else:
		mes = space_message.select(user.user[0][2])[0]
		new_mes = add_message(quest_id=mes[1])[0]
		mes[4].append([{"text": event.text, "callbackData": f"message_{mes[1]}_{new_mes}"}])
		space_message.replace(mes)
		user.user[0][4] = 'None'
		await message_quest(bot, event, select_id=mes[0], user=user)


async def add_new_quest(bot, event, is_callback=True):
	user_id = event.data['from']['userId']
	user = User(user_id=user_id)
	if is_callback:
		await bot.answer_callback_query(query_id=event.data['queryId'])
		# Если админ нажал кнопку
		#end_id_send_message
		user.user[0][3]	= 0	
		#type_action
		user.user[0][4] = 'add_new_quest'
		await bot.send_text(
			chat_id=user_id,
			text="Напишите имя квеста"
		)
		user.save()
	else:
		end_id = connection.call('box.sequence.quest_S:current', ()).data[0]
		#Создание нового сообщения
		mes = add_message(quest_id=int(end_id) + 1)
		#message_ид | квеста | ид сообщения к которому необходимо перейти
		quest_button = space_quest_button.insert((None, False, event.text, f"message_{int(end_id) + 1}_{mes[0]}"))
		#type_action
		user.user[0][4] = 'None'
		#message_id
		user.user[0][2] = mes[0]
		#quest_id
		user.user[0][1] = int(end_id) + 1
		#Выдаём админу, начальное сообщение квеста
		await message_quest(bot, event, select_id=mes[0], user=user)


async def edit_text(bot, event):
	user_id = event.data['from']['userId']
	user = User(user_id=user_id)
	if event.type.value == 'callbackQuery':
		await bot.answer_callback_query(query_id=event.data['queryId'])
		# Если админ нажал кнопку
		#end_id_send_message
		user.user[0][3]	= 0	
		#type_action
		user.user[0][4] = 'edit_text'
		await bot.send_text(
			chat_id=user_id,
			text="Напишите новый текст"
		)
		user.save()
	else:
		mes = space_message.select(user.user[0][2])[0]
		if event.text.split()[0].lower() == '/финал':	
			space_message.update(mes[0], [('=', 2, 'final'), ('=', 3, ' '.join(event.text.split()[1:]))])
		else:
			space_message.update(mes[0], [('=', 3, event.text)])
		user.user[0][4] = 'None'
		await send_type_text(bot, event, mes, user=user)


async def admin(bot, event):
	if event.data['from']['userId'] in ADMINS:
		user = User(user_id=event.data['from']['userId'])
		user.user[0][5] = not user.user[0][5]
		user.save()				


async def send_mes(bot, event, chat_id, text, inline_keyboard_markup, user):
	if user.end_id_send_message == 0 or event.type.value == 'newMessage':
		# Если, человек не разу не писал
		answer = await bot.send_text(
			chat_id=chat_id,
			text=text,
			inline_keyboard_markup=inline_keyboard_markup
		)
		#end_id_send_message
		user.user[0][3] = int(answer['msgId'])
		user.save()
	else:
		await bot.edit_text(
			msg_id=user.end_id_send_message,
			chat_id=chat_id,
			text=text,
			inline_keyboard_markup=inline_keyboard_markup
		)
