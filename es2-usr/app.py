import os
from flask import Flask, request, Response, json, jsonify
import psycopg2
from consultas import Consulta
import data

app = Flask(__name__)

@app.route('/getuser/<identificador>')
def getuser(identificador):
	data = {
		identificador : Consulta().getUser(identificador)
	}
	js = json.dumps(data)
	response = Response(response=js, status=200, mimetype='application/json')
	return response

@app.route('/cadastrar/<login>&<name>&<bio>')
def cadastrar(login, name, bio):
	Consulta().cadastrar(login, name, bio)
	return "{0}".format(Consulta().getId(login, name, bio)[0])


@app.route('/remover/<identificador>')
def remover(identificador):
	Consulta().remover(identificador)
	return ""


@app.route('/follow/<follower>&<followed>')
def follow(follower, followed):
	Consulta().follow(follower, followed)
	return ""


@app.route('/unfollow/<follower>&<followed>')
def unfollow(follower, followed):
	Consulta().unfollow(follower, followed)
	return ""


@app.route('/users/')
def users():
	records = Consulta().users()
	return records


@app.route('/follows/')
def follows():
	records = Consulta().follows()
	return str(records)


# retorna os seguidores de follower
@app.route('/getfollowers/<followed>')
def followers(followed):
	data = {
		followed : Consulta().getFollowers(followed)
	}
	js = json.dumps(data)
	response = Response(response=js, status=200, mimetype='application/json')
	return response


# retorna os usuarios seguidos por follower em forma de json
@app.route('/getfollowed/<follower>', methods=['GET'])
def followed(follower):
	data = {
		follower : Consulta().getFollowed(follower)
	}
	js = json.dumps(data)
	response = Response(response=js, status=200, mimetype='application/json')
	return response


@app.route('/')
def home():
	return "Light Twitter - Modulo de Usuarios - Gabriel Almeida, Gabriel Soares, Henrique Fonseca e Sadallo Andere"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
