import psycopg2

from data import DATA, USER, PASS, HOST, PORT, SSL

class Consulta:
	def __init__(self):
		self.conn = psycopg2.connect(database=DATA, user=USER, password=PASS, host=HOST, port=PORT, sslmode=SSL)			

	def getUser(self, identificador):
		cursor = self.conn.cursor()
		sql = "SELECT * FROM users WHERE id = {}".format(identificador)
		cursor.execute(sql)
		records = cursor.fetchall()
		if len(records) == 0:
			return ""
		else:
			return records[0]

	def getId(self, login, name, bio):
		cursor = self.conn.cursor()
		sql = "SELECT id FROM users WHERE login = '{}' and name = '{}' and bio = '{}'".format(login, name, bio)
		cursor.execute(sql)
		records = cursor.fetchall()
		return records[0]

	def cadastrar(self, login, name, bio):
		cursor = self.conn.cursor()
		sql = "INSERT INTO users (login, name, bio) VALUES ('{}', '{}', '{}')".format(login, name, bio)
		cursor.execute(sql)
		self.conn.commit()
		

	def remover(self, identificador):
		cursor = self.conn.cursor()
		sql = "DELETE FROM users WHERE id = {}".format(identificador)
		cursor.execute(sql)
		self.conn.commit()


	def follow(self, follower, followed):
		cursor = self.conn.cursor()
		sql = "INSERT INTO follows VALUES ({}, {}) ON CONFLICT (follower, followed) DO NOTHING".format(follower, followed)
		cursor.execute(sql)
		self.conn.commit()
		

	def unfollow(self, follower, followed):
		cursor = self.conn.cursor()
		sql = "DELETE FROM follows WHERE follower = {} AND followed = {}".format(follower, followed)
		cursor.execute(sql)
		self.conn.commit()


	def getFollowers(self, followed):
		cursor = self.conn.cursor()
		sql = "SELECT json_agg(follower) FROM follows WHERE followed = {}".format(followed)
		cursor.execute(sql)
		records = cursor.fetchall()
		if len(records) == 0:
			return ""
		else:
			return records[0][0]


	def getFollowed(self, follower):
		cursor = self.conn.cursor()
		sql = "SELECT json_agg(followed) FROM follows WHERE follower = {}".format(follower)
		cursor.execute(sql)
		records = cursor.fetchall()
		if len(records) == 0:
			return ""
		else:
			return records[0][0]


#auxiliares

	def users(self):
		cursor = self.conn.cursor()
		sql = "SELECT * FROM users"
		cursor.execute(sql)
		records = cursor.fetchall()
		return str(records)

	def follows(self):
		cursor = self.conn.cursor()
		sql = "SELECT * FROM follows"
		cursor.execute(sql)
		records = cursor.fetchall()
		return records