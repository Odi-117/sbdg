import os
import time
import random

class WorkWithSession:

	characters = "1234567890ABCDEFGHIKLMNOPQRSTVXYZ-1234567890ABCDEFGHIKLMNOPQRSTVXYZ-1234567890ABCDEFGHIKLMNOPQRSTVXY"

	def __init__(self, key):	
		self.key = key
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

	def create_file_session(self, key_session):
		if not self.check_session(key_session):
			f = open("session/{}.txt".format(key_session), "w")
			f.close()
			
			return True

		else:
			return False

	def delete_file_session(self, key_session):
		if self.check_session(key_session):
			os.remove("session/{}.txt".format(key_session))
			
			return True

		else:
			return False

	def create_session(self):
		return_key = self.create_key_session()
		if not self.check_session(return_key):
			if self.create_file_session(return_key):
				return return_key

			else:
				return "Didn`t create session"

		else:
			return False

	def chekc_session_updata_time(self, key_session, max_time_update):
		time_update = os.path.getmtime("session/{}.txt".format(key_session))
		now_time = time.time()
		if (time_update+max_time_update) > now_time:	
			return True

		else:
			return False

	def check_session(self, key_session):
		try:
			if self.chekc_session_updata_time(key_session, 600):
				os.system("touch session/{}.txt".format(key_session)) 
				return True

			else:
				os.remove("session/{}.txt".format(key_session))
				return False

		except FileNotFoundError:
			return False



if __name__ == "__main__":

	c = WorkWithSession("None")
	print(c.create_key())