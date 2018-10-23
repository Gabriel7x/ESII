import os
from flask import Flask, render_template, request, Response, json, jsonify
import psycopg2
from consultas import Consulta
import data

app = Flask(__name__)

@app.route('/messages/')
def messages():
	records = Consulta().messages()
	return str(records)

@app.route('/addmessage/<user_id>&<message>')
def addMessage(user_id, message):
	records = Consulta().addMessage(user_id, message)
	return str(records)


#retorna a mensagem pelo message_id
@app.route('/getmessagebyid/<message_id>', methods=['GET'])
def getMessageByID(message_id):
	data = {
		message_id : Consulta().getMessageByID(message_id)
	}
	js = json.dumps(data)
	response = Response(response=js, status=200, mimetype='application/json')
	return render_template('msgByID.html', msg=response)
	#return response  


#retorna as mensagens pelo user_id
@app.route('/getmessagebyuserid/<user_id>', methods=['GET'])
def getMessageByUserID(user_id):
	data = {
		user_id : Consulta().getMessageByUserID(user_id)
	}
	js = json.dumps(data)
	response = Response(response=js, status=200, mimetype='application/json')
	#return render_template('msgByUserID.html', msg=response)
	return response



@app.route('/')
def home():
	return "<h1 style='color: blue'>Light Twitter</h1> <h2>Modulo de Mensagens - Gabriel Almeida, Gabriel Soares, Henrique Fonseca e Sadallo Andere</h2>"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
