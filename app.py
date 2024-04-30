from flask import Flask, jsonify, render_template
from source.backend.api_tmdb import API_TMDb

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trending')
def catalogo():
    tmdb_api = API_TMDb(api_key="API Read Access Token")
    filmes = tmdb_api.buscar_filmes_trending()
    if filmes:
        return render_template('trending.html', filmes=filmes)
    else:
        return "Erro ao obter filmes do TMDB"

if __name__ == '__main__':
    app.run(debug=True)