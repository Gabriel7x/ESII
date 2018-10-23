import os, requests
from flask import Flask, request, json, render_template, redirect, url_for
import psycopg2

app = Flask(__name__)
usuarioLogado = None

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/cadastro')
def cadastro():
	return render_template('cadastro.html')

@app.route('/deletar')
def deletar():
	requests.get('http://es2-usr.herokuapp.com/remover/{0}'
		.format(usuarioLogado))

	return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
	global usuarioLogado
	usuarioLogado = request.form['login']

	return redirect(url_for('getMensagensUsuario', usuario = usuarioLogado))

@app.route('/realizarCadastro', methods=['POST'])
def realizarCadastro():
	novoUsuario = requests.get('http://es2-usr.herokuapp.com/cadastrar/{0}&{1}&{2}'
		.format(request.form['login'],request.form['nome'], request.form['bio']))

	print(novoUsuario.text)
	return render_template('resposta.html', user=novoUsuario.text)

@app.route('/postarMensagem', methods=['POST'])
def postarMensagem():
	requests.get('http://es2-message.herokuapp.com/addmessage/{0}&{1}'
		.format(usuarioLogado, request.form['mensagem']))

	return redirect(url_for('getMensagensUsuario', usuario = usuarioLogado))

@app.route('/seguir', methods=['POST'])
def seguir():
	requests.get('http://es2-usr.herokuapp.com/follow/{0}&{1}'
		.format(usuarioLogado,request.form['idUsuarioSeguir']))

	return redirect(url_for('getListaDeSeguidos', usuario = usuarioLogado))

@app.route('/pararDeSeguir', methods=['POST'])
def pararDeSeguir():
	requests.get('http://es2-usr.herokuapp.com/unfollow/{0}&{1}'
		.format(usuarioLogado,request.form['idUsuarioParar']))

	return redirect(url_for('getListaDeSeguidos', usuario = usuarioLogado))

# requisita ao modulo de Usuarios os usuarios seguidos por um determinado usuario
# auxiliar da funcao debaixo
def getSeguidos(usuario):
	seguidos = requests.get('http://es2-usr.herokuapp.com/getfollowed/{}'
		.format(usuario)).json()[usuario]

	return seguidos

def getMensagensDoUsuario(usuario):
	mensagens = requests.get('http://es2-message.herokuapp.com/getmessagebyuserid/{}'
		.format(usuario)).json()[usuario]

	return mensagens

#requisita ao modulo de mensagens as mensagens dos seguidos de um determinado usuario
@app.route('/home/<usuario>')
def getMensagensSeguidos(usuario):
	mensagens = []

	try:
		mensagens = [(usuario,mensagem) for mensagem in getMensagensDoUsuario(usuario)]
	except TypeError:
		pass

	try:
		for seguido in getSeguidos(usuario):
			mensagens_seguido = (requests.get('http://es2-message.herokuapp.com/getmessagebyuserid/{}'
				.format(seguido)).json())
			if mensagens_seguido[str(seguido)] is not None:
				mensagens += [(seguido, mensagem) for mensagem in mensagens_seguido[str(seguido)]]
	except TypeError:
		pass

	if len(mensagens) == 0:
		return render_template('msgSeguidosErro.html', user=usuario)

	return render_template('msgSeguidos.html', post=mensagens, user=usuario)

#requisita ao modulo de mensagens de um determinado usuario
@app.route('/posts/<usuario>')
def getMensagensUsuario(usuario):
	mensagens = getMensagensDoUsuario(usuario)
	if mensagens == None:
		return render_template('msgUserErro.html', user=usuario)

	return render_template('msgUser.html', post=mensagens, user=usuario)

@app.route('/seguidos/<usuario>')
def getListaDeSeguidos(usuario):
	mensagem = getSeguidos(usuario)
	if mensagem == None:
		return render_template('seguindoErro.html', user = usuario)

	return render_template('seguindo.html', post=mensagem, user=usuario)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)