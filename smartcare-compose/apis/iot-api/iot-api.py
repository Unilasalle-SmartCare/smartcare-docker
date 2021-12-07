from flask import Flask
import json
import os
import psycopg2

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

    print("IOT-API - Não pôde se conectar ao banco de dados!")

IotApi = Flask(__name__)

@IotApi.route("/")
def Home():

    Data = [{"msg": "Esta é a IOT API, um servidor flask dedicado à camada IOT do projeto Smartcare!"}]

    return json.dumps({"success": True, "errors": [], "data": Data})

@IotApi.route("/alert")
def GetAlert():

    try:

        if conn != None:

            cur = conn.cursor()
            cur.execute(f"SELECT BIT_ALERTA FROM PACIENTE")
            rv = cur.fetchone()[0]
            conn.commit()

            Data = [{"alert": rv}]

            return json.dumps({"success": True, "errors": [], "data": Data})
        
        else:

            Errors = [{"msg": "IOT-API - Sem conexão com o banco de dados!"}]

            return json.dumps({"success": False, "errors": Errors, "data": []})

    except:
        
        Errors = [{"msg": "IOT-API - Erro ao ler alertas do paciente!"}]

        return json.dumps({"success": False, "errors": Errors, "data": []})

@IotApi.route("/insert/measurement/<CodigoDispositivo>/<DataHora>/<Valor>")
def InsertMeasurement(CodigoDispositivo, DataHora, Valor):

    try:

        if conn != None:

            cur = conn.cursor()
            cur.execute(f"CALL PUBLIC.USP_INSERE_MEDICAO ('{CodigoDispositivo}','{DataHora}','{Valor}','Null')")
            conn.commit()

            return json.dumps({"success": True, "errors": [], "data": []})

        else:

            Errors = [{"msg": "IOT-API - Sem conexão com o banco de dados!"}]

            return json.dumps({"success": False, "errors": Errors, "data": []})

    except Exception as ex:

        Errors = [{"msg": str(ex)}]

        return json.dumps({"success": False, "errors": Errors, "data": []})

if __name__ == "__main__":
    
    IotApi.run(host="0.0.0.0", port=8082, debug=True)

conn.close()
