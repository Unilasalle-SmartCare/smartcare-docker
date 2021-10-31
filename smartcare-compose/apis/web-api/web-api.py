import psycopg2
import json
import os
from bottle import Bottle, request
from urllib.parse import parse_qs

class PageError():

    def error400(error):

        return json.dumps({"sucess": False, "error": [{"msg": "400 Bad Request"}], "data": [{}]})

    def error401(error):

        return json.dumps({"sucess": False, "error": [{"msg": "401 Unauthorised"}], "data": [{}]})

    def error403(error):

        return json.dumps({"sucess": False, "error": [{"msg": "403 Forbidden"}], "data": [{}]})

    def error404(error):

        # Se em algum momento for usar html como resposta de erro
        # import codecs

        # file = codecs.open("./error-pages/404.html", "r", "utf-8")
        # HTML = file.read()
        # file.close()

        return json.dumps({"sucess": False, "errors": [{"msg": "404 Not Found"}], "data": [{}]})

    def error405(error):

        return json.dumps({"sucess": False, "errors": [{"msg": "405 Method Not Allowed"}], "data": [{}]})

    def error408(error):

        return json.dumps({"sucess": False, "errors": [{"msg": "408 Request Time-Out"}], "data": [{}]})

    def error500(error):

        return json.dumps({"sucess": False, "errors": [{"msg": "500 Internal Server Error"}], "data": [{}]})

    def error501(error):

        return json.dumps({"sucess": False, "errors": [{"msg": "501 Not Implemented"}], "data": [{}]})

    def error502(error):

        return json.dumps({"sucess": False, "errors": [{"msg": "502 Service Temporarily Overloaded"}], "data": [{}]})

    def error503(error):

        return json.dumps({"sucess": False, "errors": [{"msg": "503 Service Unavailable"}], "data": [{}]})

class StringHandling():

    def AddColumns(columns, str):

        if columns > 0:

            return str + ","

        else:

            return str

    def isnumber(string):

        try:
            float(string)
            return True
        except:
            return False

class UrlHandling():

    def FindGetVars(varsearch):

        Sucess  = True
        Errors  = []
        Data    = []

        try:

            params  = parse_qs(request.query_string)
            search  = 0
            repeats = 0

            for i in params:

                if i == varsearch:

                    for j in params[i]:

                        search = j
                        repeats = repeats + 1
                        
            params2 = request.query.keys()

            for i in params2:

                if i == varsearch:

                    values = request.query.values()

                    for j in values:

                        if j != search:
                            
                            search = j
                            repeats = repeats + 1

            if repeats > 1:

                Sucess = False
                Errors.append({"msg": "A variável buscada foi passada mais de uma vez!"})

            elif repeats == 0:

                Sucess = False
                Errors.append({"msg": "A variável buscada não foi passada!"})

            else:

                Data.append({varsearch: search})

        except:

            Sucess = False
            Errors.append({"msg": "Erro ao tratar as variáveis da requisição!"})

        finally:

            return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

    def OpenGetValues(varsearch, typereturn):

        Sucess  = True
        Errors  = []
        Data    = []

        try:

            variavel = json.loads(UrlHandling.FindGetVars(varsearch))

            if list(variavel.values())[0] == True:

                dataList = list(variavel.values())[2]

                for data in dataList:

                    Data.append({f"{varsearch}": list(data.values())[0]})

            else:

                Sucess = False
                errorList = list(variavel.values())[1]

                for error in errorList:

                    Errors.append({"msg": f"{list(error.values())[0]}"})

        except:

            Sucess = False
            Errors.append({"msg": "Erro extrair valores das variáveis do formulário!"})

        finally:

            if typereturn == 1:

                return Sucess, Errors, Data

            else:

                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

class Env():

    def DataBase():

        Sucess  = True
        Errors  = []
        Data    = []

        try:

            db_host = os.getenv("DB_HOST", "")
            db_user = os.getenv("DB_USER", "")
            db_name = os.getenv("DB_NAME", "")

            if db_host != "" and db_user != "" and db_name != "":

                Data.append({"data": f"dbname={db_name} user={db_user} host={db_host}"})

            else:

                Sucess = False
                Errors.append({"msg": "Não foi possivel resolver os dados de conexão da base de dados!"})

        except:

            Sucess = False
            Errors.append({"msg": "Erro interno na api - Tradução de dados de conexão da base de dados!"})

        finally:

            return json.dumps({"Sucess": Sucess, "errors": Errors, "data": Data})

class ConnectDataBase():

    def Connection(WebApi):

        Sucess  = True
        Errors  = []
        Data    = []

        try:

            dsn                 = json.loads(Env.DataBase())
            connectionStatus    = list(dsn.values())[0]
            connectionErrors    = list(dsn.values())[1]
            connectionData      = list(dsn.values())[2]

            if connectionStatus == True:
                try:
                    
                    connect = psycopg2.connect(list(list(connectionData)[0].values())[0])
                    WebApi.conn = connect
                    Data.append({"data": f"{connect}"})

                except psycopg2.Error as ex:
                    
                    WebApi.conn = None
                    Sucess = False
                    Errors.append({"msg": "Erro ao se conectar à base de dados! {0}".format(ex)})

            else:

                Sucess = False
                
                for error in connectionErrors:

                    Errors.append({"msg": list(error.values())[0]})

        except:

            Sucess = False

            Errors.append({"msg": "Erro interno na Api - Conexão na Base de Dados!"})

        finally:

            return json.dumps({"Sucess": Sucess, "errors": Errors, "data": Data})

    def Status(WebApi):

        Sucess = True
        Errors = []
        Data = []
        
        try:
            
            if WebApi.conn == None:
                
                try:

                    connection = json.loads(ConnectDataBase.Connection(WebApi))
                    connectionStatus = list(connection.values())[0]
                    connectionErrors = list(connection.values())[1]
                    connectionData = list(connection.values())[2]

                    Sucess = connectionStatus
                    
                    for error in connectionErrors:
                        
                        Errors.append({"msg": list(error.values())[0]})

                    for data in connectionData:

                        Data.append({"msg": list(data.values())[0]})

                except Exception as ex:

                    Sucess = False
                    Errors.append({"msg": ex})

        except:

            Sucess = False
            Errors.append({"msg": "Erro ao autenticar a conexão com o banco de dados, contate o suporte!"})

        finally:

            return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

class WebApi(Bottle):

    def __init__(self):

        super().__init__()

        # TipoDispositivo

        self.route("/microservices/web/dispositivo/tipo/get/all", method="GET", callback=self.TipoDispositivoGetAll)

        self.route("/microservices/web/dispositivo/tipo/get/actives", method="GET", callback=self.TipoDispositivoGetAll)

        self.route("/microservices/web/dispositivo/tipo/getby/id", method="GET", callback=self.TipoDispositivoGetById)

        self.route("/microservices/web/dispositivo/tipo/getby/name", method="GET", callback=self.TipoDispositivoGetByName)

        self.route("/microservices/web/dispositivo/tipo/insert", method="POST", callback=self.TipoDispositivoInsert)

        self.route("/microservices/web/dispositivo/tipo/update", method="PUT", callback=self.TipoDispositivoUpdate)

        self.route("/microservices/web/dispositivo/tipo/update/name", method="PATCH", callback=self.TipoDispositivoUpdateName)

        self.route("/microservices/web/dispositivo/tipo/delete", method="DELETE", callback=self.TipoDispositivoDelete)

        # Dispositivo

        self.route("/microservices/web/dispositivo/get/all", method="GET", callback=self.DispositivoGetAll)

        self.route("/microservices/web/dispositivo/get/actives", method="GET", callback=self.DispositivoGetAll)

        self.route("/microservices/web/dispositivo/getby/id", method="GET", callback=self.DispositivoGetById)

        self.route("/microservices/web/dispositivo/getby/id/type", method="GET", callback=self.DispositivoGetById)

        self.route("/microservices/web/dispositivo/getby/id/environment", method="GET", callback=self.DispositivoGetById)

        self.route("/microservices/web/dispositivo/getby/string/name", method="GET", callback=self.DispositivoGetByString)

        self.route("/microservices/web/dispositivo/getby/string/code", method="GET", callback=self.DispositivoGetByString)

        self.route("/microservices/web/dispositivo/insert", method="POST", callback=self.DispositivoInsert)

        self.route("/microservices/web/dispositivo/update", method="PUT", callback=self.DispositivoUpdate)

        # self.route("/microservices/web/dispositivo/update/name", method="PATCH", callback=self.DispositivoUpdateName) 
        #     
        # self.route("/microservices/web/dispositivo/update/code", method="PATCH", callback=self.DispositivoUpdateCode) 
        #        
        # self.route("/microservices/web/dispositivo/delete", method="DELETE", callback=self.DispositivoDelete)

        # Ambiente

        # Medição

        @self.error(400)

        def error_handler_400(error):

            return PageError.error400(error)

        @self.error(401)

        def error_handler_401(error):

            return PageError.error401(error)

        @self.error(403)

        def error_handler_403(error):

            return PageError.error403(error)

        @self.error(404)

        def error_handler_404(error):

            return PageError.error404(error)

        @self.error(405)

        def error_handler_405(error):

            return PageError.error405(error)

        @self.error(408)

        def error_handler_408(error):

            return PageError.error408(error)

        @self.error(500)

        def error_handler_500(error):

            return PageError.error500(error)

        @self.error(501)

        def error_handler_501(error):

            return PageError.error501(error)

        @self.error(502)

        def error_handler_502(error):

            return PageError.error502(error)

        @self.error(503)

        def error_handler_503(error):

            return PageError.error503(error)

        try:

            connection          = json.loads(ConnectDataBase.Connection(self))
            connectionStatus    = list(connection.values())[0]
            connectionErrors    = list(connection.values())[1]
            connectionData      = list(connection.values())[2]

            if connectionStatus == False:

                print(connectionErrors)

            else:

                print("Conection has been established!")
                print(list(list(connectionData)[0].values())[0])

        except:
            
            print("Connection error!")
            print(ConnectDataBase.Connection(self))


    #   TipoDispositivo

    def TipoDispositivoGetAll(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus == True:

            SQL = "SELECT * FROM TIPODISPOSITIVO "
            Sucess = True
            Errors = []
            Data = []

            try:

                chamada = request['bottle.route'].rule.replace("/microservices/web/dispositivo/tipo/get/", "")

                if chamada == "actives":

                    SQL = SQL + "WHERE IND_SIT = 1 "

                SQL = SQL + "ORDER BY IDTIPO"

                cur = self.conn.cursor()
                cur.execute(SQL)
                row_headers = [x[0] for x in cur.description]
                rv = cur.fetchall()
                self.conn.commit()

                for result in rv:

                    Data.append(dict(zip(row_headers, result)))

            except:

                Sucess = False
                Errors.append({"msg": "Erro na listagem de tipos de dispositivo!"})

            finally:

                cur.close()

                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})
        
        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": "Erro na conexão com o banco de dados, contate o suporte!"}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    def TipoDispositivoGetById(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus == True:

            Sucess  = True
            Errors  = []
            Data    = []

            try:

                variavelStatus, variavelErrors, variavelData = UrlHandling.OpenGetValues("idbusca", 1)

                if variavelStatus == True:

                    idbusca = list(list(variavelData)[0].values())[0]

                    if(str(idbusca).isnumeric()):

                        SQL = f"SELECT * FROM TIPODISPOSITIVO WHERE 1 = 1 AND IDTIPO = {idbusca} ORDER BY IDTIPO"

                        try:

                            cur = self.conn.cursor()
                            cur.execute(SQL)
                            row_headers = [x[0] for x in cur.description]
                            rv = cur.fetchall()
                            self.conn.commit()

                            for result in rv:

                                Data.append(dict(zip(row_headers, result)))
                                break

                        except:

                            Sucess = False
                            Errors.append({"msg": "Erro na listagem de tipos de dispositivo!"})

                        finally:

                            cur.close()

                    elif str(idbusca) == "":

                        Sucess = False
                        Errors.append({"msg": "O valor buscado deve ser diferente de vazio!"})

                    else:

                        Sucess = False
                        Errors.append({"msg": "O valor buscado não é um inteiro!"})

                else:

                    Sucess = False

                    for error in variavelErrors:

                        Errors.append({"msg": list(error.values())[0]})
                        
            except:

                Sucess = False
                Errors.append({"msg": "Erro interno na Api - busca por id!"})

            finally:

                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})
        
        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg":"Erro na conexão com o banco de dados, contate o suporte!"}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    def TipoDispositivoGetByName(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus == True:

            Sucess  = True
            Errors  = []
            Data    = []

            try:

                variavelStatus, variavelErrors, variavelData = UrlHandling.OpenGetValues("nomebusca", 1)

                if variavelStatus == True:

                    nomebusca = list(list(variavelData)[0].values())[0]

                    if str(nomebusca) != "":

                        SQL =  f"SELECT * FROM TIPODISPOSITIVO " + \
                               f"WHERE 1 = 1 AND UPPER(NOME) LIKE '%{str(nomebusca).upper()}%' " + \
                                "ORDER BY IDTIPO"

                        try:

                            cur = self.conn.cursor()
                            cur.execute(SQL)
                            row_headers = [x[0] for x in cur.description]
                            rv = cur.fetchall()
                            self.conn.commit()

                            for result in rv:

                                Data.append(dict(zip(row_headers, result)))

                        except:

                            Sucess = False
                            Errors.append({"msg": "Erro na listagem de tipos de dispositivo!"})

                        finally:

                            cur.close()

                    else:

                        Sucess = False
                        Errors.append({"msg": "O valor buscado deve ser diferente de vazio!"})
                else:

                    Sucess = False

                    for error in variavelErrors:

                        Errors.append({"msg": list(error.values())[0]})

            except:

                Sucess = False
                Errors.append({"msg": "Erro interno na Api - busca por nome!"})

            finally:

                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": "Erro na conexão com o banco de dados, contate o suporte!"}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    def TipoDispositivoInsert(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus == True:        

            Sucess      = True
            Errors      = []
            Data        = []
            FormData    = request.forms

            try:

                cadastra = FormData.get("cadastra") if "cadastra" in FormData.keys() else None

                if cadastra != None:
                    
                    SQL = "INSERT INTO TIPODISPOSITIVO (NOME, IND_SIT) VALUES " + f" ('{cadastra}', 1)"

                    try:

                        cur = self.conn.cursor()
                        cur.execute(SQL)
                        self.conn.commit()

                        try:

                            SQL =  f"SELECT * FROM TIPODISPOSITIVO " + \
                                   f"WHERE NOME = '{cadastra}' " + \
                                    "ORDER BY IDTIPO DESC LIMIT 1"

                            cur = self.conn.cursor()
                            cur.execute(SQL)
                            row_headers = [x[0] for x in cur.description]
                            rv = cur.fetchall()
                            self.conn.commit()

                            for result in rv:

                                Data.append(dict(zip(row_headers, result)))
                                break

                            if not Data:

                                Sucess = False
                                Errors.append({"msg": "A inserção foi bem sucedida, porém não encontramos os dados no banco!"})
                        
                        except:

                            Sucess = False
                            Errors.append({"msg": "A inserção parece ter ocorrido normalmente, mas ocorreu um erro ao buscar os indices do dado"})
                        
                        finally:
                        
                            cur.close()
                    
                    except:
                    
                        Sucess = False
                        Errors.append({"msg": "Erro na inserção dos dados!"})
                    
                    finally:
                    
                        cur.close()
                
                else:
                
                    Sucess = False
                    Errors.append({"msg": "As variáveis esperadas não foram passadas"})
            
            except:
            
                Sucess = False
                Errors.append({"msg": "Erro interno na Api - inserir!"})
            
            finally:
            
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": "Erro na conexão com o banco de dados, contate o suporte!"}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    def TipoDispositivoUpdate(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus == True:

            Sucess      = True
            Errors      = []
            Data        = []
            FormData    = request.forms

            try:

                idtipo = FormData.get("id") if "id" in FormData.keys() else None

                if not FormData:

                    Sucess = False
                    Errors.append({"msg": "Não foram passados parametros!"})

                elif idtipo != None and str(idtipo).isnumeric():

                    request.query.update({'idbusca': f'{idtipo}'})
                    DataBefore = json.loads(self.TipoDispositivoGetById())
                    DataBeforeStatus    = list(DataBefore.values())[0]
                    DataBeforeErrors    = list(DataBefore.values())[1]
                    DataBeforeData      = list(DataBefore.values())[2]

                    if  DataBeforeStatus == True and DataBeforeData:

                        columns = 0
                        SQL     = "UPDATE TIPODISPOSITIVO SET "

                        nome = FormData.get("nome") if "nome" in FormData.keys() else None
                    
                        if nome != None:

                            SQL     = StringHandling.AddColumns(columns, SQL)
                            SQL     = SQL + f"NOME = '{nome}'"
                            columns = columns + 1

                        if columns > 0:

                            SQL = SQL + f" WHERE 1 = 1 AND IDTIPO = {idtipo}"
                            
                            try:
                            
                                cur = self.conn.cursor()
                                cur.execute(SQL)
                                self.conn.commit()

                                try:
                            
                                    SQL =  f"SELECT * FROM TIPODISPOSITIVO " + \
                                           f"WHERE IDTIPO = {idtipo} " + \
                                            "ORDER BY IDTIPO"

                                    cur = self.conn.cursor()
                                    cur.execute(SQL)
                                    row_headers = [x[0] for x in cur.description]
                                    rv = cur.fetchall()
                                    self.conn.commit()

                                    for result in rv:
                                    
                                        Data.append(dict(zip(row_headers, result)))
                                        break
                                    
                                    if not Data:
                                    
                                        Sucess = False
                                        Errors.append({"msg": "A atualização foi bem sucedida, porém não encontramos os dados no banco!"})
                                
                                except:
                                
                                    Sucess = False
                                    Errors.append({"msg": "A atualização foi bem sucedida, mas ocorreu um erro ao buscar os indices do dado!"})
                                
                                finally:
                                
                                    cur.close()
                            
                            except:
                            
                                Sucess = False
                                Errors.append({"msg": "Erro na atualização dos dados!"})
                            
                            finally:
                            
                                cur.close()
                        
                        else:
                        
                            Sucess = False
                            Errors.append({"msg": "Nenhuma coluna foi passada para o update"})
                    
                    else:
                    
                        Sucess = False
                        Errors.append({"msg": "O id do tipo de dispositivo não foi localizado!"})

                        for error in DataBeforeErrors:

                            Errors.append({"msg": list(error.values())[0]})
                
                else:
                
                    Sucess = False
                    Errors.append({"msg": "O id do objeto não pôde ser resolvido, ele deve ser um inteiro!"})
            
            except:
            
                Sucess = False
                Errors.append({"msg": "Erro interno na Api - atualizar!"})
            
            finally:
            
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": "Erro na conexão com o banco de dados, contate o suporte!"}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    def TipoDispositivoUpdateName(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus == True:

            Sucess      = True
            Errors      = []
            Data        = []
            FormData    = request.forms

            try:

                idtipo  = FormData.get("id")    if "id"     in FormData.keys()  else None
                nome    = FormData.get("nome")  if "nome"   in FormData.keys()  else None

                if idtipo != None and str(idtipo).isnumeric():

                    if nome != None:

                        SQL = "UPDATE TIPODISPOSITIVO SET NOME = '{}' WHERE IDTIPO = {}".format(
                            nome ,
                            idtipo
                        )
                        request.query.update({'idbusca': f'{idtipo}'})
                        DataBefore = json.loads(self.TipoDispositivoGetById())
                        DataBeforeStatus    = list(DataBefore.values())[0]
                        DataBeforeErrors    = list(DataBefore.values())[1]
                        DataBeforeData      = list(DataBefore.values())[2]                        

                        if  DataBeforeStatus == True and DataBeforeData:

                            try:

                                cur = self.conn.cursor()
                                cur.execute(SQL)
                                self.conn.commit()

                                try:

                                    SQL =  f"SELECT * FROM TIPODISPOSITIVO " + \
                                           f"WHERE IDTIPO = {idtipo} " + \
                                            "ORDER BY IDTIPO"

                                    cur = self.conn.cursor()
                                    cur.execute(SQL)
                                    row_headers = [x[0] for x in cur.description]
                                    rv = cur.fetchall()
                                    self.conn.commit()

                                    for result in rv:

                                        Data.append(dict(zip(row_headers, result)))
                                        break

                                    if not Data:

                                        Sucess = False
                                        Errors.append({"msg": "A atualização foi bem sucedida, porém não encontramos os dados no banco!"})
                                
                                except:
                            
                                    Sucess = False
                                    Errors.append({"msg": "A atualização foi bem sucedida, mas ocorreu um erro ao buscar os indices do dado!"})
                            
                                finally:
                            
                                    cur.close()
                            
                            except:
                            
                                Sucess = False
                                Errors.append({"msg": "Erro na atualização do nome!"})
                            
                            finally:
                            
                                cur.close()
                        
                        else:
                        
                            Sucess = False
                            Errors.append({"msg": "O id do tipo de dispositivo não foi localizado!"})

                            for error in DataBeforeErrors:

                                Errors.append({"msg": list(error.values())[0]})
                    
                    else:
                    
                        Sucess = False
                        Errors.append({"msg": "O nome a ser alterado não foi passado!"})
                
                else:
                
                    Sucess = False
                    Errors.append({"msg": "O id do objeto não pôde ser resolvido, ele deve ser um inteiro!"})
            
            except:
            
                Sucess = False
                Errors.append({"msg": "Erro interno na Api - Atualizar nome!"})
            
            finally:
            
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": "Erro na conexão com o banco de dados, contate o suporte!"}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    def TipoDispositivoDelete(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus == True:

            Sucess      = True
            Errors      = []
            Data        = []
            FormData    = request.forms

            try:

                idtipo = FormData.get("id") if "id" in FormData.keys() else None

                if idtipo != None and str(idtipo).isnumeric():

                    request.query.update({'idbusca': f'{idtipo}'})
                    DataBefore          = json.loads(self.TipoDispositivoGetById())
                    DataBeforeStatus    = list(DataBefore.values())[0]
                    DataBeforeErrors    = list(DataBefore.values())[1]
                    DataBeforeData      = list(DataBefore.values())[2]
                    Count               = 0
                    IndSitPosition      = -1

                    if DataBeforeData:               

                        Keys = list(DataBeforeData)[0].keys()

                        for i in Keys:

                            if i == "ind_sit":

                                IndSitPosition = Count

                            Count = Count + 1

                    if  DataBeforeStatus == True and list(DataBefore.values())[2] and IndSitPosition != -1:

                        if  list(list(DataBeforeData)[0].values())[IndSitPosition] != 2:

                            SQL = f"UPDATE TIPODISPOSITIVO SET IND_SIT = 2 WHERE IDTIPO = {idtipo}"

                            try:

                                cur = self.conn.cursor()
                                cur.execute(SQL)
                                self.conn.commit()

                                try:

                                    SQL =  f"SELECT 1 FROM TIPODISPOSITIVO " + \
                                           f"WHERE IDTIPO = {idtipo} AND IND_SIT <> 2 " + \
                                            "ORDER BY IDTIPO"

                                    cur = self.conn.cursor()
                                    cur.execute(SQL)
                                    row_headers = [x[0] for x in cur.description]
                                    rv = cur.fetchall()
                                    self.conn.commit()

                                    for result in rv:

                                        Data.append(dict(zip(row_headers, result)))
                                        break

                                    if Data:

                                        Sucess = False
                                        Errors.append({"msg": "A exclusão não foi bem sucedida!"})

                                except:

                                    Sucess = False
                                    Errors.append({"msg": "A exclusão foi bem sucedida, mas ocorreu um erro ao buscar os indices do dado!"})

                                finally:
                                
                                    cur.close()
                            
                            except:
                            
                                Sucess = False
                                Errors.append({"msg": "Erro na exclusão do tipo!"})
                            
                            finally:
                            
                                cur.close()
                        
                        else:
                        
                            Sucess = False
                            Errors.append({"msg": "Tipo já deletado!"})
                    
                    else:
                    
                        Sucess = False
                        Errors.append({"msg": "O id do tipo de dispositivo não foi localizado!"})

                        for error in DataBeforeErrors:

                            Errors.append({"msg": list(error.values())[0]})

                else:

                    Sucess = False
                    Errors.append({"msg": "O id do objeto não pôde ser resolvido, ele deve ser um inteiro!"})

            except:

                Sucess = False
                Errors.append({"msg": "Erro interno na Api - deletar!"})

            finally:

                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg":"Erro na conexão com o banco de dados, contate o suporte!"}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    #   Dispositivo

    def DispositivoGetAll(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus == True:

            SQL     = "SELECT * FROM DISPOSITIVO "
            Sucess  = True
            Errors  = []
            Data    = []

            try:
            
                chamada = request['bottle.route'].rule.replace("/microservices/web/dispositivo/getall/", "")

                if chamada == "actives":

                    SQL = SQL + "WHERE IND_SIT = 1 " 

                SQL = SQL + "ORDER BY IDDISPOSITIVO"

                cur = self.conn.cursor()
                cur.execute(SQL)
                row_headers = [x[0] for x in cur.description]
                rv = cur.fetchall()
                self.conn.commit()

                for result in rv:

                    Data.append(dict(zip(row_headers, result)))

            except:

                Sucess = False
                Errors.append({"msg": "Erro na listagem de dispositivo!"})
            
            finally:
            
                cur.close()
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg":"Erro na conexão com o banco de dados, contate o suporte!"}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    def DispositivoGetById(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus == True:

            Sucess  = True
            Errors  = []
            Data    = []

            try:

                variavelStatus, variavelErrors, variavelData = UrlHandling.OpenGetValues("idbusca", 1)

                if variavelStatus == True:
                
                    idbusca = list(list(variavelData)[0].values())[0]
                
                    if(str(idbusca).isnumeric()):
                
                        SQL = "SELECT * FROM DISPOSITIVO WHERE 1 = 1 "

                        route   = "/microservices/web/dispositivo/getby/id"
                        chamada = request['bottle.route'].rule.replace(route + "/", "")

                        if chamada == "type":

                            SQL = SQL + f"AND IDTIPO = {idbusca} "
                            returnLines = 100

                        elif chamada == "environment":

                            SQL = SQL + f"AND IDAMBIENTE = {idbusca} "
                            returnLines = 100

                        elif chamada == route:

                            SQL = SQL + f"AND IDDISPOSITIVO = {idbusca} "
                            returnLines = 1

                        else:

                            Sucess = False
                            Errors.append({"msg":"Rota não encontrada!"})

                            return({"sucess":Sucess,"errors":Errors,"data":Data})
                
                        try:

                            SQL = SQL + "ORDER BY IDDISPOSITIVO"
                
                            cur = self.conn.cursor()
                            cur.execute(SQL)
                            row_headers = [x[0] for x in cur.description]
                            rv = cur.fetchall()
                            self.conn.commit()

                            counter = 1

                            for result in rv:

                                Data.append(dict(zip(row_headers, result)))
                                if returnLines == counter:
                                    break
                                counter = counter + 1

                        except:
                           
                            Sucess = False
                            Errors.append({"msg": "Erro na listagem de dispositivo!"})
                        
                        finally:
                        
                            cur.close()
                    
                    elif str(idbusca) == "":
                    
                        Sucess = False
                        Errors.append({"msg": "O valor buscado deve ser diferente de vazio!"})
                    
                    else:
                    
                        Sucess = False
                        Errors.append({"msg": "O valor buscado não é um inteiro!"})
                
                else:
                
                    Sucess = False
                    msgs = list(list(variavelErrors)[0].values())

                    for msg in msgs:
                    
                        Errors.append({"msg": msg})
            
            except:
            
                Sucess = False
                Errors.append({"msg": "Erro interno na Api - busca por id!"})
            
            finally:
            
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg":"Erro na conexão com o banco de dados, contate o suporte!"}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    def DispositivoGetByString(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus == True:

            Sucess  = True
            Errors  = []
            Data    = []

            try:

                variavelStatus, variavelErrors, variavelData = UrlHandling.OpenGetValues("textobusca", 1)

                if variavelStatus == True:
                
                    textobusca = list(list(variavelData)[0].values())[0]

                    if textobusca != "":
                
                        SQL = "SELECT * FROM DISPOSITIVO WHERE 1 = 1 "

                        route = "/microservices/web/dispositivo/getby/string"
                        chamada = request['bottle.route'].rule.replace(route + "/", "")

                        if chamada == "name":

                            SQL = SQL + f"AND UPPER(NOME) LIKE '%{str(textobusca).upper()}%' "

                        elif chamada == "code":

                            SQL = SQL + f"AND UPPER(CODIGODISPOSITIVO) LIKE '%{str(textobusca).upper()}%' "

                        else:

                            Sucess = False
                            Errors.append({"msg":"Rota não encontrada!"})

                            return({"sucess":Sucess,"errors":Errors,"data":Data})

                        try:

                            SQL = SQL + "ORDER BY IDDISPOSITIVO"
                    
                            cur = self.conn.cursor()
                            cur.execute(SQL)
                            row_headers = [x[0] for x in cur.description]
                            rv = cur.fetchall()
                            self.conn.commit()

                            for result in rv:

                                Data.append(dict(zip(row_headers, result)))

                        except:
                            
                            Sucess = False
                            Errors.append({"msg": "Erro na busca de dispositivo!"})
                        
                        finally:
                        
                            cur.close()

                    else:

                        Sucess = False
                        Errors.append({"msg": "O valor buscado deve ser diferente de vazio!"})
                
                else:
                
                    Sucess = False
                    msgs = list(list(variavelErrors)[0].values())

                    for msg in msgs:
                    
                        Errors.append({"msg": msg})
            
            except:
            
                Sucess = False
                Errors.append({"msg": "Erro interno na Api - busca por texto!"})
            
            finally:
            
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg":"Erro na conexão com o banco de dados, contate o suporte!"}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    def DispositivoInsert(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus == True:        

            Sucess      = True
            Errors      = []
            Data        = []
            FormData    = request.forms

            try:

                MandatoryVars = ["codigo", "tipo", "ambiente", "nome", "eixox", "eixoy", "orientacao"]

                MandatoryVarsExists = True

                for var in MandatoryVars:

                    if var not in FormData.keys():

                        MandatoryVarsExists = False

                MandatoryVarsTypes = True

                if MandatoryVarsExists == True:

                    idtipo      = FormData.get("tipo")
                    idambiente  = FormData.get("ambiente")
                    eixox       = FormData.get("eixox")
                    eixoy       = FormData.get("eixoy")
                    
                    MandatoryVarsTypes = True   if  (       str(idtipo).isnumeric() == True \
                                                        and str(idambiente).isnumeric() == True \
                                                        and StringHandling.isnumber(eixox) == True \
                                                        and StringHandling.isnumber(eixoy) == True \
                                                    ) \
                                                else False

                else:

                    MandatoryVarsTypes = False

                if MandatoryVarsExists == True and MandatoryVarsTypes == True:

                    try:
                        
                        codigodispositivo   = FormData.get("codigo")
                        idtipo              = FormData.get("tipo")
                        idambiente          = FormData.get("ambiente")
                        nome                = FormData.get("nome")
                        descricao           = FormData.get("descricao") if "descricao" in FormData.keys() else ""
                        eixox               = FormData.get("eixox")
                        eixoy               = FormData.get("eixoy")
                        orientacao          = FormData.get("orientacao")
                            
                        SQL = " INSERT INTO DISPOSITIVO (" + \
                                                            "CODIGODISPOSITIVO , " + \
                                                            "IDTIPO , " + \
                                                            "IDAMBIENTE , " + \
                                                            "NOME , " + \
                                                            "DESCRICAO , " + \
                                                            "EIXO_X , " + \
                                                            "EIXO_Y , " + \
                                                            "ORIENTACAO , " + \
                                                            "IND_SIT" + \
                                                        ")" + \
                                "VALUES " + " ('{}', {}, {}, '{}', '{}', {}, {}, '{}', 1)".format(
                                    codigodispositivo ,
                                    idtipo ,
                                    idambiente ,
                                    nome ,
                                    descricao ,
                                    eixox ,
                                    eixoy ,
                                    orientacao
                                )

                        try:

                            cur = self.conn.cursor()
                            cur.execute(SQL)
                            self.conn.commit()

                            try:

                                SQL = "SELECT * FROM DISPOSITIVO ORDER BY IDDISPOSITIVO DESC LIMIT 1"

                                cur = self.conn.cursor()
                                cur.execute(SQL)
                                row_headers = [x[0] for x in cur.description]
                                rv = cur.fetchall()
                                self.conn.commit()

                                for result in rv:

                                    Data.append(dict(zip(row_headers, result)))
                                    break

                                if not Data:

                                    Sucess = False
                                    Errors.append({"msg": "A inserção foi bem sucedida, porém não encontramos os dados no banco!"})
                            
                            except:

                                Sucess = False
                                Errors.append({"msg": "A inserção parece ter ocorrido normalmente, mas ocorreu um erro ao buscar os índices do dado!"})
                            
                            finally:
                            
                                cur.close()
                        
                        except:
                        
                            Sucess = False
                            Errors.append({"msg": "Erro na inserção dos dados!"})
                        
                        finally:
                        
                            cur.close()
                    
                    except:
                    
                        Sucess = False
                        Errors.append({"msg": "Erro interno na Api - inserir!"})

                elif MandatoryVarsExists == False:

                    Sucess = False
                    Errors.append({"msg":"Variáveis obrigatórias não foram passadas!"})

                else: #MandatoryVarsTypes == False

                    Sucess = False
                    Errors.append({"msg":"Os tipos das variáveis obrigatórias estão incorretos!"})
            
            except:

                Sucess = False
                Errors.append({"msg":"Erro ao decodificar as variáveis!"})

            finally:

                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": "Erro na conexão com o banco de dados, contate o suporte!"}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    def DispositivoUpdate(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus == True:

            Sucess      = True
            Errors      = []
            Data        = []
            FormData    = request.forms

            try:

                iddispositivo = FormData.get("id") if "id" in FormData.keys() else None

                if not FormData:

                    Sucess = False
                    Errors.append({"msg": "Não foram passados parametros!"})

                elif iddispositivo != None and str(iddispositivo).isnumeric():

                    request.query.update({'idbusca': f'{iddispositivo}'})

                    DataBefore          = json.loads(self.TipoDispositivoGetById())
                    DataBeforeStatus    = list(DataBefore.values())[0]
                    DataBeforeErrors    = list(DataBefore.values())[1]
                    DataBeforeData      = list(DataBefore.values())[2]

                    if  DataBeforeStatus == True and DataBeforeData:

                        codigodispositivo   = FormData.get("codigo")        if "codigo"     in FormData.keys()  else None
                        idtipo              = FormData.get("tipo")          if "tipo"       in FormData.keys()  else None
                        idambiente          = FormData.get("ambiente")      if "ambiente"   in FormData.keys()  else None
                        nome                = FormData.get("nome")          if "nome"       in FormData.keys()  else None
                        descricao           = FormData.get("descricao")     if "descricao"  in FormData.keys()  else None
                        eixox               = FormData.get("eixox")         if "eixox"      in FormData.keys()  else None
                        eixoy               = FormData.get("eixoy")         if "eixoy"      in FormData.keys()  else None
                        orientacao          = FormData.get("orientacao")    if "orientacao" in FormData.keys()  else None

                        if      (   str(idtipo).isnumeric()         == True     or idtipo       == None ) \
                            and (   str(idambiente).isnumeric()     == True     or idambiente   == None ) \
                            and (   StringHandling.isnumber(eixox)  == True     or eixox        == None ) \
                            and (   StringHandling.isnumber(eixoy)  == True     or eixoy        == None ):

                            columns = 0
                            SQL     = "UPDATE DISPOSITIVO SET "

                            if codigodispositivo != None:

                                SQL     = StringHandling.AddColumns(columns, SQL)
                                SQL     = SQL + f"CODIGODISPOSITIVO = '{codigodispositivo}'"
                                columns = columns + 1

                            if idtipo != None:

                                SQL     = StringHandling.AddColumns(columns, SQL)
                                SQL     = SQL + f"IDTIPO = '{idtipo}'"
                                columns = columns + 1

                            if idambiente != None:

                                SQL     = StringHandling.AddColumns(columns, SQL)
                                SQL     = SQL + f"IDAMBIENTE = '{idambiente}'"
                                columns = columns + 1

                            if nome != None:

                                SQL     = StringHandling.AddColumns(columns, SQL)
                                SQL     = SQL + f"NOME = '{nome}'"
                                columns = columns + 1

                            if descricao != None:

                                SQL     = StringHandling.AddColumns(columns, SQL)
                                SQL     = SQL + f"DESCRICAO = '{descricao}'"
                                columns = columns + 1

                            if eixox != None:

                                SQL     = StringHandling.AddColumns(columns, SQL)
                                SQL     = SQL + f"EIXO_X = '{eixox}'"
                                columns = columns + 1

                            if eixoy != None:

                                SQL     = StringHandling.AddColumns(columns, SQL)
                                SQL     = SQL + f"EIXO_Y = '{eixoy}'"
                                columns = columns + 1

                            if orientacao != None:

                                SQL     = StringHandling.AddColumns(columns, SQL)
                                SQL     = SQL + f"ORIENTACAO = '{orientacao}'"
                                columns = columns + 1

                            if columns > 0:

                                SQL = SQL + f" WHERE 1 = 1 AND IDDISPOSITIVO = {iddispositivo}"

                                try:
                                
                                    cur = self.conn.cursor()
                                    cur.execute(SQL)
                                    self.conn.commit()

                                    try:
                                
                                        SQL =  f"SELECT * FROM DISPOSITIVO " + \
                                               f"WHERE IDDISPOSITIVO = {iddispositivo} " + \
                                                "ORDER BY IDDISPOSITIVO"
                                        cur = self.conn.cursor()
                                        cur.execute(SQL)
                                        row_headers = [x[0] for x in cur.description]
                                        rv = cur.fetchall()
                                        self.conn.commit()

                                        for result in rv:
                                        
                                            Data.append(dict(zip(row_headers, result)))
                                            break
                                        
                                        if not Data:
                                        
                                            Sucess = False
                                            Errors.append({"msg": "A atualização foi bem sucedida, porém não encontramos os dados no banco!"})
                                    
                                    except:
                                    
                                        Sucess = False
                                        Errors.append({"msg": "A atualização foi bem sucedida, mas ocorreu um erro ao buscar os indices do dado!"})
                                    
                                    finally:
                                    
                                        cur.close()
                                
                                except:
                                
                                    Sucess = False
                                    Errors.append({"msg": "Erro na atualização dos dados!"})
                                
                                finally:
                                
                                    cur.close()
                            
                            else:
                            
                                Sucess = False
                                Errors.append({"msg": "Nenhuma coluna foi passada para o update"})

                        else:

                            Sucess = False
                            Errors.append({"msg":"O tipo da variável está incorreto!"})
                        
                    else:
                    
                        Sucess = False
                        Errors.append({"msg": "O id do dispositivo não foi localizado!"})
                    
                else:
                
                    Sucess = False
                    Errors.append({"msg": "O id do objeto não pôde ser resolvido, ele deve ser um inteiro!"})
            
            except:
            
                Sucess = False
                Errors.append({"msg": "Erro interno na Api - atualizar!"})
            
            finally:
            
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": "Erro na conexão com o banco de dados, contate o suporte!"}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})


if __name__ == '__main__':

    webapi = WebApi()
    webapi.run(host='0.0.0.0', port=8081, debug=True)
