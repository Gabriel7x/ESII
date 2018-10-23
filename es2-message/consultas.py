import psycopg2

from data import DATA, USER, PASS, HOST, PORT, SSL

class Consulta:
	def __init__(self):
		self.conn = psycopg2.connect(database=DATA, user=USER, password=PASS, host=HOST, port=PORT, sslmode=SSL)			

	def addMessage(self, user_id, message):
		cursor = self.conn.cursor()
		sql = "INSERT INTO messages (user_id, message) VALUES ({}, '{}')".format(user_id, message)
		cursor.execute(sql)
		self.conn.commit()
		return ""


	def getMessageByID(self, message_id):
		cursor = self.conn.cursor()
		sql = "SELECT * FROM messages WHERE message_id = {}".format(message_id)
		cursor.execute(sql)
		records = cursor.fetchall()
		if len(records) == 0:
			return ""
		else:
			return records


	def getMessageByUserID(self, message_id):
		cursor = self.conn.cursor()
		sql = "SELECT json_agg(message) FROM messages WHERE user_id = {}".format(message_id)
		cursor.execute(sql)
		records = cursor.fetchall()
		if len(records) == 0:
			return ""
		else:
			return records[0][0]


#auxiliares

	def messages(self):
		cursor = self.conn.cursor()
		sql = "SELECT * FROM messages"
		cursor.execute(sql)
		records = cursor.fetchall()
		return str(records)