from flask import Flask
import json
import os
import psycopg2

app = Flask(__name__)
    
@app.route("/caminhos_hora")

def caminhos_hora (dataHora = None):

    try:

        db_host = os.getenv("DB_HOST", "")
        db_user = os.getenv("DB_USER", "")
        db_name = os.getenv("DB_NAME", "")
        db_pass = os.getenv("DB_PASS", "")

        print(db_host)

        if db_host != "" and db_user != "" and db_name != "" and db_pass != "":

            print("tem os dados")

            conn = psycopg2.connect(f"dbname={db_name} user={db_user} password={db_pass} host={db_host}")
            print(conn)
            cursor = conn.cursor()
            qstr = "select A.DataHora , A.Valor , B.CodigoDispositivo , B.Eixo_X , B.Eixo_y , B.Orientacao case when B.Orientacao = '+X' then x = B.Eixo_X - (A.Valor * 0.5) and y = B.Eixo_y END when B.Orientacao = '+Y' then y = B.Eixo_y - (A.Valor * 0.5) and x = B.Eixo_X END when B.Orientacao = '-X' then x = B.Eixo_X + (A.Valor * 0.5) and y = B.Eixo_y END when B.Orientacao = '-Y' then y = B.Eixo_y + (A.Valor * 0.5) and x = B.Eixo_X END from Medicao A, Dispositivo B where A.IdDispositivo = B.IdDispositivo like A.DataHora =\'"+dataHora+"\'"
            print (qstr)
            query = cursor.execute(qstr)
            row_headers=[x[0] for x in cursor.description]
            records = cursor.fetchall()
            print (records)
            result = [dict(zip(tuple (row_headers) ,i)) for i in records]
            print (result)
            jret = json.dumps({"msg":result})
            print (jret)
            conn.close()
            return jret
        
        else:

            return json.dumps({"msg":"Erro ao ler dados do banco!"})
    
    except:

        return json.dumps({"msg":"Erro na rota!"})

app.run()
