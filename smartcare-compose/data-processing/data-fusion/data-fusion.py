import ast
from flask import Flask
import json
import requests

DataFusion = Flask(__name__)

@DataFusion.route("/caminhos_hora/<DataInicio>/<DataFim>")
def caminhos_hora (DataInicio, DataFim):

    try:

        request = requests.get(f"http://172.21.0.6:8083/medicao/{DataInicio}/{DataFim}")

        Medicao = request.json()

        return json.dumps(Medicao)

    except:

        return json.dumps({"msg":"Erro na rota!"})

if __name__ == "__main__":

    DataFusion.run(host="0.0.0.0", port=5000, debug=True)