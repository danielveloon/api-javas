from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle
import pandas as pd

app = Flask(__name__)
CORS(app)

# Carregando modelo e encoder
modelo, encoder = pickle.load(open('covid_model.pkl', 'rb'))
print("Modelo e encoder carregados")
print(encoder.categories_)


@app.route("/predict_covid", methods=['POST'])
def predict_covid():
    dados = request.get_json()

    colunas_esperadas = [
        "Problema Respiratório", "Febre", "Tosse Seca", "Dor de Garganta",
        "Coriza", "Asma", "Doença Pulmonar Crônica", "Dor de Cabeça",
        "Doença Cardíaca", "Diabetes", "Hipertensão", "Fadiga",
        "Problemas Gastrointestinais", "Viagem ao Exterior",
        "Contato com Paciente COVID", "Participou de Multidão",
        "Visitou Locais Públicos", "Familiar em Local Público"
    ]

    for coluna in colunas_esperadas:
        if coluna not in dados:
            return jsonify({"erro": f"Campo '{coluna}' está ausente."}), 400

    entrada = pd.DataFrame([dados])
    entrada = entrada.astype(str)  # conversão para string, necessária para o encoder

    entrada_transformada = encoder.transform(entrada).toarray()
    resultado = modelo.predict(entrada_transformada)

    mapa_previsao = {
        'Sim': 1,
        'Não': 0
    }

    previsao_str = resultado[0]

    if previsao_str in mapa_previsao:
        previsao = mapa_previsao[previsao_str]
    else:
        return jsonify({"erro": f"Valor inesperado na predição: {previsao_str}"}), 500

    return jsonify({
        "previsao": previsao,
        "resultado": "Positivo para COVID" if previsao == 1 else "Negativo para COVID"
    })

if __name__ == "__main__":
    app.run(debug=True)
