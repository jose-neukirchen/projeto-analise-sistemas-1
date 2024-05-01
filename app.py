from flask import Flask, jsonify, render_template, request, redirect, url_for
from source.backend.api_tmdb import API_TMDb
from source.backend.usuario import Usuario
from os import environ

tmdb_token = environ["TMDB_TOKEN"]


Usuario.criar_banco_dados()

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trending')
def catalogo():
    tmdb_api = API_TMDb(api_key=tmdb_token)
    filmes = tmdb_api.buscar_filmes_trending()
    if filmes:
        return render_template('trending.html', filmes=filmes)
    else:
        return "Erro ao obter filmes do TMDB"
    
@app.route('/filme/<int:id>', methods=['GET'])  # Define a rota para o filme com base no ID
def filme(id):
    # Aqui você pode adicionar lógica para recuperar as informações do filme com base no ID
    # e passá-las para o template da página de informações do filme
    tmdb_api = API_TMDb(api_key=tmdb_token)
    filme = tmdb_api.buscar_detalhes_filme(id)
    if filme:
        return render_template('filme.html', filme=filme)
    else:
        return "Filme não encontrado"
    
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['username']
        senha = request.form['password']
        # Adiciona o usuário ao banco de dados
        print("Ok")
        Usuario.adicionar_usuario(nome, senha)
        # Redireciona para a página de login
        return redirect(url_for('login'))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verifica se o usuário está no banco de dados e a senha está correta
        print("verifica")
        if Usuario.validar_login(username, password):
            # Redireciona para a página de catálogo se o login for bem-sucedido
            return redirect(url_for('catalogo'))
        else:
            # Se o login falhar, recarrega a página de login com uma mensagem de erro
            error_message = "Usuário ou senha incorretos. Tente novamente."
            return render_template('login.html', error_message=error_message)
    
    # Se a requisição for GET, simplesmente renderiza a página de login
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)