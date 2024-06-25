import nltk
from nltk.stem import WordNetLemmatizer
import Levenshtein
from flask import Flask, request, render_template

# Certifique-se de ter os pacotes necessários do nltk
nltk.download('wordnet')
nltk.download('omw-1.4')

app = Flask(__name__)

def carregar_perguntas(arquivo):
    perguntas_respostas = {}
    with open(arquivo, "r") as f:
        for linha in f:
            pergunta, resposta = linha.strip().split("|")
            perguntas_respostas[pergunta.lower()] = resposta
    return perguntas_respostas

def lematizar_frase(frase):
    lemmatizer = WordNetLemmatizer()
    palavras = frase.split()
    palavras_lematizadas = [lemmatizer.lemmatize(palavra) for palavra in palavras]
    return ' '.join(palavras_lematizadas)

def encontrar_resposta(pergunta, perguntas_respostas, limiar_distancia=5):
    pergunta_lematizada = lematizar_frase(pergunta)
    menor_distancia = float("inf")
    melhor_resposta = ""

    for p, r in perguntas_respostas.items():
        p_lematizada = lematizar_frase(p)
        if pergunta_lematizada in p_lematizada:
            return r
        distancia = Levenshtein.distance(pergunta_lematizada, p_lematizada)
        if distancia < menor_distancia:
            menor_distancia = distancia
            melhor_resposta = r
    if menor_distancia <= limiar_distancia:
        return melhor_resposta
    else:
        return "Pergunta não encontrada."

# Carregar perguntas e respostas
perguntas_respostas = carregar_perguntas("perguntas.txt")

@app.route("/", methods=["GET", "POST"])
def index():
    resposta = ""
    if request.method == "POST":
        pergunta = request.form["pergunta"].lower()
        limiar_distancia = int(request.form["limiar_distancia"])
        resposta = encontrar_resposta(pergunta, perguntas_respostas, limiar_distancia)
    return render_template("index.html", resposta=resposta)

if __name__ == "__main__":
    app.run(debug=True)
