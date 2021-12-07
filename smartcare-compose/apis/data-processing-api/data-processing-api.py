from flask import Flask
import json
import os
import psycopg2
import requests

conn = None

try:
    
    db_host = os.getenv("DB_HOST", "")
    db_user = os.getenv("DB_USER", "")
    db_name = os.getenv("DB_NAME", "")
    db_pass = os.getenv("DB_PASS", "")

    if db_host != "" and db_user != "" and db_name != "" and db_pass != "":

        conn = psycopg2.connect(f"dbname={db_name} user={db_user} password={db_pass} host={db_host}")

        print("IOT-API - Conectada ao banco de dados!")

except:

    conn = None

    print("DATA-PROCESSING-API - Não pôde se conectar ao banco de dados!")

IotApi = Flask(__name__)

@IotApi.route("/")
def Home():

    Data = [{"msg": "Esta é a DATA-PROCESSING-API, um servidor flask dedicado à camada DATA-PROCESSING do projeto Smartcare!"}]

    return json.dumps({"success": True, "errors": [], "data": Data})

@IotApi.route("/medicao/<DataInicio>/<DataFim>")
def Medicao(DataInicio, DataFim):

    try:

        if conn != None:

            Medicao = []

            cur = conn.cursor()
            cur.execute(f"SELECT * FROM PUBLIC.USP_BUSCA_MEDICAO('{DataInicio}','{DataFim}');")
            row_headers = [x[0] for x in cur.description]
            rv = cur.fetchall()
            conn.commit()

            for result in rv:

                medicao = list(result)
                medicao[2] = str(medicao[2])

                Medicao.append(dict(zip(row_headers, medicao)))

            return json.dumps({"success": True, "errors": [], "data": Medicao})

        else:

            print("DATA-PROCESSING-API - Sem conexão com o banco de dados!")

            return json.dumps({"success": False, "errors": [{"msg":"Sem conexão com o banco de dados!"}], "data": []})

    except Exception as ex:

        Errors = []
        Errors.append({"msg": str(ex)})

        return json.dumps({"success": False, "errors": Errors, "data": []})

@IotApi.route("/medicao/tratada/<DataInicio>/<DataFim>")
def MedicaoTratada(DataInicio, DataFim):

    try:

        request = requests.get(f"http://172.21.0.7:5000/caminhos_hora/{DataInicio}/{DataFim}")

        Medicao = request.json()

        return json.dumps({"success": True, "errors": [], "data": Medicao["data"]})

    except Exception as ex:

        Errors = []
        Errors.append({"msg": str(ex)})

        return json.dumps({"success": False, "errors": Errors, "data": []})

if __name__ == "__main__":
    
    IotApi.run(host="0.0.0.0", port=8083, debug=True)

conn.close()
