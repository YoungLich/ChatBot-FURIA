from flask import Flask, render_template, request, jsonify
import json
import os
import re
import difflib

# Diga ao Flask onde estão seus static e templates (esses são os padrões, mas explicito aqui)
app = Flask(
    __name__,
    static_folder='static',       # para /static/...
    template_folder='templates'   # para render_template
)

# Carrega o JSON uma única vez
FAQ_PATH = os.path.join(os.path.dirname(__file__), 'data', 'faq_furia.json')
with open(FAQ_PATH, encoding='utf-8') as f:
    base_conhecimento = json.load(f)

def normalizar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto.strip()

def encontrar_resposta(pergunta_usuario):
    p_norm = normalizar_texto(pergunta_usuario)
    perguntas = [normalizar_texto(item['pergunta']) for item in base_conhecimento]
    match = difflib.get_close_matches(p_norm, perguntas, n=1, cutoff=0.6)
    if match:
        idx = perguntas.index(match[0])
        return base_conhecimento[idx]['resposta']
    return "Desculpe, ainda não sei a resposta para isso. Tente perguntar de outra forma."

# ——— ROTA PRINCIPAL: entrega seu HTML + CSS + JS ———
@app.route('/')
def index():
    return render_template('index.html')

# ——— ROTA DA API: recebe a pergunta e devolve JSON ———
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    msg = data.get('mensagem', '')
    resposta = encontrar_resposta(msg)
    return jsonify({'resposta': resposta})

if __name__ == '__main__':
    app.run(debug=True)
