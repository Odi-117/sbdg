import os

import psycopg2

class DBConnect:

	def __init__(self, DATABASE_URL, table:str):

		self.table = table 
		
		if type(DATABASE_URL) == str:
			self.DB_URL = DATABASE_URL

		elif type(DATABASE_URL) == dict:
			self.dbname = DATABASE_URL["dbname"]
			self.user = DATABASE_URL["user"]
			self.password = DATABASE_URL["password"]
			self.host = DATABASE_URL["host"]

		else:         
			raise TypeError("arument DATABASE_URL is`t dict or str.")

	def connect_db(self):
		try:        
			return psycopg2.connect(self.DB_URL)

		except AttributeError:
			return psycopg2.connect(dbname=self.dbname, user=self.user,
			password=self.password, host=self.host)

	def req_select_db(self, select_columns:str, select_where:str):
		conn = self.connect_db()
		cursor = conn.cursor()
		if select_where != "": 
			select_where = "where {}".format(select_where)

		sql_request = "select {} from {} {}".format(select_columns,
				self.table, select_where)
		cursor.execute(sql_request)
		records = cursor.fetchall()
		cursor.close()
		conn.close()

		return records


	def req_insert_db(self, values:str, into:str="into"):
		conn = self.connect_db()
		cursor = conn.cursor()
		sql_request = "insert {} {} values({})".format(into,
				self.table, values)
		cursor.execute(sql_request)
		conn.commit()
		cursor.close()
		conn.close()

	def req_update_db(self, set_value:str,
			where_update:str):
		conn = self.connect_db()
		cursor = conn.cursor()
		sql_request = "update {} set {} where {}".format(self.table,
				set_value, where_update)
		cursor.execute(sql_request)
		conn.commit()
		cursor.close()
		conn.close()        

	pass

	def req_delete_db(self, where_request:str):
		conn = self.connect_db()
		cursor = conn.cursor()
		sql_request = "delete from {} where {}".format(self.table,
				where_request)
		cursor.execute(sql_request)
		conn.commit()
		cursor.close()
		conn.close()