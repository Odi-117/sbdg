import os
import time
import random
import json

class WorkWithSession:

	characters = "1234567890ABCDEFGHIKLMNOPQRSTVXYZ-1234567890ABCDEFGHIKLMNOPQRSTVXYZ-1234567890ABCDEFGHIKLMNOPQRSTVXY"

	def __init__(self, key):	
		self.key = key
		self.format_file = "json"
		pass

	def create_key(self):
		key = ""
		for i in range(0, 15):
			key += self.characters[random.randint(0,32)]

		return key

	def create_key_session(self):
		translate_key_int = ""
		for i in range(len(self.key)):
			translate_key_int += str(ord(self.key[i]))
	 
		seconds = time.time()
		session_key_int = pow(int(translate_key_int)*int(seconds), 2)
		session_key_int = str(session_key_int)
		session_key = ""
		for i in range(0, len(session_key_int), 2):
			session_key += self.characters[int(session_key_int[i:i+2:])]

		return session_key

	def part_to_file(self, key_session):
		return "session/{}.{}".format(key_session, self.format_file)

	def create_file_session(self, key_session):
		if not self.check_session(key_session):
			f = open(self.part_to_file(key_session), "w")
			f.close()
			
			return True

		else:
			return False

	def delete_file_session(self, key_session):
		try:
			os.remove(self.part_to_file(key_session))
			return True

		except OSError:
			return False


	def chekc_session_updata_time(self, key_session, max_time_update):
		time_update = os.path.getmtime(self.part_to_file(key_session))
		now_time = time.time()
		if (time_update+max_time_update) > now_time:	
			return True

		else:
			return False

	def check_session(self, key_session):
		try:
			if self.chekc_session_updata_time(key_session, 600):
				os.system("touch {}".format(self.part_to_file(key_session)))
				return True

			else:
				self.delete_file_session(key_session)
				return False

		except OSError:
			return False


	def create_session(self):
		return_key = self.create_key_session()
		if not self.check_session(return_key):
			if self.create_file_session(return_key):
				return return_key

			else:
				return False

		else:
			return False

	def write_in_session(self, key_session, text):
		if self.check_session(key_session):
			file_session = open(self.part_to_file(key_session), "w") 
			file_session.write(json.dumps(text))
			file_session.close()
			return True


	def read_from_session(self, key_session):
		if self.check_session(key_session):
			file_session = open(self.part_to_file(key_session), "r")
			text = file_session.read()
			file_session.close()
			return json.loads(text)
		else:
			return False


