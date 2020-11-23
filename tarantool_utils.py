import tarantool

connection = tarantool.connect("localhost", 3305)

space_user = connection.space('user')

space_message = connection.space('message')

space_quest_button = connection.space('quest_button')
		

def add_message(quest_id, type_mes='message', text='Текст', buttons=[]):
		return space_message.insert((None, int(quest_id), type_mes, text, buttons))[0]

class User:
	def __init__(self, user_id):
		self.user = space_user.select(user_id)
		if not self.user:
			self.user = space_user.insert((user_id, 0, 0, 0, 'None', False, '', {}))
		self.user_id = user_id
		self.quest_id = self.user[0][1]
		self.message_id = self.user[0][2]
		self.end_id_send_message = self.user[0][3]
		self.type_action = self.user[0][4]
		self.is_admin = self.user[0][5]
		self.hash_string = self.user[0][6]
		self.history = self.user[0][7]

	def save(self):
		space_user.replace(self.user[0])
		