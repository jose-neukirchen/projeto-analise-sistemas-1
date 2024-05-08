from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from source.backend.api_tmdb import API_TMDb
from source.backend.usuario import Usuario
from source.backend.filme import Filme
from source.backend.resenha import Resenha
from source.backend.database import Database
from os import environ

tmdb_token = environ["TMDB_TOKEN"]


# Criar uma instância da classe Database
db = Database()

# Chama o método para criar o banco de dados e as tabelas
db.criar_banco_dados()

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'teste123'

@app.route('/')
def catalogo():
    tmdb_api = API_TMDb(api_key=tmdb_token)
    filmes = tmdb_api.buscar_filmes_trending()
    if filmes:
        return render_template('index.html', filmes=filmes)
    else:
        return "Erro ao obter filmes do TMDB"

@app.route('/cadastro')
def cadastro():
    # Verifica se há uma sessão ativa de usuário
    if 'usuario_id' in session:
        # Se houver uma sessão ativa, redireciona o usuário para outra rota
        return redirect(url_for('usuario'))
    else:
        # Se não houver uma sessão ativa, renderiza a página de cadastro
        return render_template('cadastro.html')

    
@app.route('/search')
def busca():
    movie_title = request.args.get('filme')  # Obtém o valor do argumento 'filme' da URL
    if movie_title:
        tmdb_api = API_TMDb(api_key=tmdb_token)
        filmes = tmdb_api.buscar_filme(movie_title)
        if filmes:
            return render_template('search.html', filmes=filmes)
    return "Erro ao obter filmes do TMDB"
    
    
# @app.route('/filme/<int:id>', methods=['GET'])  # Define a rota para o filme com base no ID
# def filme(id):
#     tmdb_api = API_TMDb(api_key=tmdb_token)
#     filme = tmdb_api.buscar_detalhes_filme(id)
#     if filme:
#         # Verifica se há um usuário na sessão
#         if 'usuario_id' in session:
#             # Obtém o usuário da sessão
#             usuario = db.obter_usuario_pelo_nome(nome=session['usuario_id'])
#             if usuario:
#                 # Obtém a resenha e a nota do usuário para o filme atual
#                 resenha, nota = usuario.obter_resenha_e_nota(id)
#                 return render_template('filme.html', filme=filme, resenha=resenha, nota=nota)
#         # Se não houver usuário na sessão, renderize a página sem resenha e nota
#         return render_template('filme.html', filme=filme)
#     else:
#         return "Filme não encontrado"

@app.route('/filme/<int:id>', methods=['GET'])  # Define a rota para o filme com base no ID
def filme(id):
    tmdb_api = API_TMDb(api_key=tmdb_token)
    filme = tmdb_api.buscar_detalhes_filme(id)
    if filme:
        # Inicializa as variáveis de verificação
        na_watchlist = False
        nos_favoritos = False

        # Verifica se há um usuário na sessão
        if 'usuario_id' in session:
            # Obtém o usuário da sessão
            usuario = db.obter_usuario_pelo_nome(nome=session['usuario_id'])
            if usuario:
                # Verifica se o filme está na watchlist do usuário
                if str(filme.id) in usuario.watchlist:
                    na_watchlist = True
                # Verifica se o filme está nos favoritos do usuário
                if str(filme.id) in usuario.favoritos:
                    nos_favoritos = True

                # Obtém a resenha e a nota do usuário para o filme atual
                resenha, nota = usuario.obter_resenha_e_nota(id)
                return render_template('filme.html', filme=filme, resenha=resenha, nota=nota, na_watchlist=na_watchlist, nos_favoritos=nos_favoritos)
        # Se não houver usuário na sessão, renderize a página sem resenha e nota
        return render_template('filme.html', filme=filme)
    else:
        return "Filme não encontrado"

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['username']
        senha = request.form['password']
        idade = request.form['idade']
        nacionalidade = request.form['nacionalidade']
        genero = request.form['genero']
        email = request.form['email']
        usuario = Usuario(nome, senha, email, idade, genero, nacionalidade)
        # Adiciona o usuário ao banco de dados
        db.adicionar_usuario(usuario)
        # Redireciona para a página de login
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario_id' in session:
        # Se houver uma sessão ativa, redireciona o usuário para outra rota
        return redirect(url_for('usuario'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verifica se o usuário está no banco de dados e a senha está correta
        if db.validar_login(username, password):
            # Armazenar o ID do usuário na sessão
            usuario = db.obter_usuario_pelo_nome(nome=username)
            session['usuario_id'] = usuario.get_nome()
            # Redireciona para a página de catálogo se o login for bem-sucedido
            return redirect(url_for('catalogo'))
        else:
            # Se o login falhar, recarrega a página de login com uma mensagem de erro
            error_message = "Usuário ou senha incorretos. Tente novamente."
            return render_template('login.html', error_message=error_message)
    
    # Se a requisição for GET, simplesmente renderiza a página de login
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Remove o ID do usuário da sessão
    session.pop('usuario_id', None)
    # Redireciona para a página de login
    return redirect(url_for('login'))

@app.route('/resenha', methods=['GET'])
def resenha():
    if request.method == 'GET':
        filme_id = request.args.get('id')
        tmdb_api = API_TMDb(api_key=tmdb_token)
        filme = tmdb_api.buscar_detalhes_filme(filme_id)
        if filme:
            return render_template('resenha.html', filme=filme)
        else:
            return "Filme não encontrado"

@app.route('/salvar_resenha', methods=['POST'])
def salvar_resenha():
    if request.method == 'POST':
        nota = request.form['nota']
        texto = request.form['texto']
        movie_id = request.form['movie_id']
        
        # Criar um objeto Resenha com os dados do formulário
        resenha = Resenha(movie_id=movie_id, nota=nota, texto=texto)
        
        usuario_atual = db.obter_usuario_pelo_nome(nome=session.get('usuario_id'))
        if usuario_atual:
            usuario_atual.adicionar_resenha(db, resenha)
            # Redirecionar para a página do filme após salvar a resenha
            return redirect(url_for('filme', id=movie_id))
        else:
            return "Erro ao salvar a resenha"

@app.route('/watchlist', methods=['GET'])
def watchlist():
    if request.method == 'GET':
        usuario_atual = db.obter_usuario_pelo_nome(nome=session.get('usuario_id'))
        filmes_ids = usuario_atual.get_watchlist()
        tmdb_api = API_TMDb(api_key=tmdb_token)
        filmes_obj = []
        for filme_id in filmes_ids:
            filme = tmdb_api.buscar_filme_por_id(filme_id)
            filmes_obj.append(filme)
        return render_template('watchlist.html', filmes=filmes_obj)
    
@app.route('/adicionar_watchlist', methods=['POST'])
def adicionar_watchlist():
    if request.method == 'POST':
        movie_id = request.form['movie_id']
        usuario_atual = db.obter_usuario_pelo_nome(nome=session.get('usuario_id'))
        if usuario_atual:
            usuario_atual.adicionar_filme_watchlist(db, movie_id)
            # Redirecionar para a página de watchlist
            return redirect(url_for('watchlist'))
        else:
            return "Erro ao adicionar à watchlist"
        
@app.route('/adicionar_favoritos', methods=['POST'])
def adicionar_favoritos():
    if request.method == 'POST':
        movie_id = request.form['movie_id']
        usuario_atual = db.obter_usuario_pelo_nome(nome=session.get('usuario_id'))
        if usuario_atual:
            usuario_atual.adicionar_filme_favoritos(db, movie_id)
            # Redirecionar para a página de watchlist
            return redirect(url_for('usuario'))
        else:
            return "Erro ao adicionar aos favoritos"
        
@app.route('/remover_watchlist', methods=['POST'])
def remover_watchlist():
    if request.method == 'POST':
        movie_id = request.form['movie_id']
        usuario_atual = db.obter_usuario_pelo_nome(nome=session.get('usuario_id'))
        if usuario_atual:
            usuario_atual.remover_filme_watchlist(db, movie_id)
            # Redirecionar para a página de watchlist
            return redirect(url_for('watchlist'))
        else:
            return "Erro ao remover da watchlist"
        
@app.route('/remover_favoritos', methods=['POST'])
def remover_favoritos():
    if request.method == 'POST':
        movie_id = request.form['movie_id']
        usuario_atual = db.obter_usuario_pelo_nome(nome=session.get('usuario_id'))
        if usuario_atual:
            usuario_atual.remover_filme_favoritos(db, movie_id)
            # Redirecionar para a página de watchlist
            return redirect(url_for('usuario'))
        else:
            return "Erro ao remover dos favoritos"
        
@app.route('/adicionar_biografia', methods=['POST'])
def adicionar_biografia():
    if request.method == 'POST':
        bio = request.form['biografia']
        usuario_atual = db.obter_usuario_pelo_nome(nome=session.get('usuario_id'))
        if usuario_atual:
            usuario_atual.adicionar_bio(db, bio)
            # Redirecionar para a página de watchlist
            return redirect(url_for('usuario'))
        else:
            return "Erro ao adicionar biografia"
        
@app.route('/usuario', methods=['GET'])
def usuario():
    if request.method == 'GET':
        # Obtém o usuário da sessão
        usuario = db.obter_usuario_pelo_nome(nome=session['usuario_id'])
        filmes_ids = usuario.get_favoritos()
        tmdb_api = API_TMDb(api_key=tmdb_token)
        filmes_obj = []
        for filme_id in filmes_ids:
            filme = tmdb_api.buscar_filme_por_id(filme_id)
            filmes_obj.append(filme)
        return render_template('usuario.html', usuario=usuario, filmes=filmes_obj)
    
@app.route('/resenhas/<int:id>')
def ver_resenhas(id):
    tmdb_api = API_TMDb(api_key=tmdb_token)
    filme = tmdb_api.buscar_detalhes_filme(id)
    
    resenhas = db.obter_resenhas_por_id_do_filme(id)
    
    return render_template('resenhas.html', filme=filme, resenhas=resenhas)

if __name__ == '__main__':
    app.run(debug=True)