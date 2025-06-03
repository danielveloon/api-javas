from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle
import pandas as pd

app = Flask(__name__)
CORS(app)

# Carregando modelo e encoder
modelo, encoder = pickle.load(open('covid_model.pkl', 'rb'))
print("Modelo e encoder carregados")


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

    # Preparando os dados
    entrada = pd.DataFrame([dados])
    entrada = entrada.astype(str)  # encoder espera strings

    try:
        entrada_transformada = encoder.transform(entrada).toarray()
    except Exception as e:
        return jsonify({"erro": f"Erro ao transformar os dados: {str(e)}"}), 500

    try:
        # Predição e probabilidade
        probas = modelo.predict_proba(entrada_transformada)
        probabilidade_covid = probas[0][1]  # índice 1 = classe "Positivo"
        previsao = int(probabilidade_covid >= 0.5)
    except Exception as e:
        return jsonify({"erro": f"Erro ao realizar a predição: {str(e)}"}), 500

    return jsonify({
        "previsao": previsao,
        "resultado": "Positivo para COVID" if previsao == 1 else "Negativo para COVID",
        "probabilidade": round(probabilidade_covid * 100, 2)  # em porcentagem
    })


if __name__ == "__main__":
    app.run(debug=True)
