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

    def CleanSqlString(str):

        Remove = "'" #adicionar aqui os caracteres a serem removidos

        for c in Remove:

            str = str.replace(c, "")

        return str

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
                Errors.append({"msg": ErrorsDict.errorcode(101)})

            elif repeats == 0:

                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(102)})

            else:

                Data.append({varsearch: search})

        except:

            Sucess = False
            Errors.append({"msg": ErrorsDict.errorcode(103)})

        finally:

            return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

    def OpenGetValues(varsearch, typereturn):

        Sucess  = True
        Errors  = []
        Data    = []

        try:

            variavel        = json.loads(UrlHandling.FindGetVars(varsearch))
            variavelStatus  = list(variavel.values())[0]
            variavelErrors  = list(variavel.values())[1]
            variavelData    = list(variavel.values())[2]

            if variavelStatus == True:

                for data in variavelData:

                    Data.append({f"{varsearch}": list(data.values())[0]})

            else:

                Sucess = False

                for error in variavelErrors:

                    Errors.append({"msg": f"{list(error.values())[0]}"})

        except:

            Sucess = False
            Errors.append({"msg": ErrorsDict.errorcode(111)})

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
            db_pass = os.getenv("DB_PASS", "")

            if db_host != "" and db_user != "" and db_name != "" and db_pass:

                Data.append({"data": f"dbname={db_name} user={db_user} password={db_pass} host={db_host}"})

            else:

                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(201)})

        except:

            Sucess = False
            Errors.append({"msg": ErrorsDict.errorcode(202)})

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
                    Errors.append({"msg": ErrorsDict.errorcode(301) + " - {0}".format(ex)})

            else:

                Sucess = False
                
                for error in connectionErrors:

                    Errors.append({"msg": list(error.values())[0]})

        except:

            Sucess = False

            Errors.append({"msg": ErrorsDict.errorcode(302)})

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
            Errors.append({"msg": ErrorsDict.errorcode(311)})

        finally:

            return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

class ErrorsDict():

    def errorcode(int):

        Errors = {}
        #TRATAMENTO DE VARIAVEIS
        Errors[101] = "A variável buscada foi passada mais de uma vez!"
        Errors[102] = "A variável buscada não foi passada!"
        Errors[103] = "Erro ao tratar as variáveis da requisição!"
        Errors[104] = "O valor buscado deve ser diferente de vazio!"
        Errors[105] = "Não foram passados parâmetros!"
        Errors[106] = "Nenhuma coluna foi passada para a atualização!"
        Errors[107] = "O id passado não pôde ser resolvido, ele deve ser um inteiro!"
        Errors[108] = "Rota não encontrada!"
        Errors[109] = "O valor buscado não é um inteiro!"
        Errors[110] = "As variáveis esperadas não foram passadas ou estão incorretas!"
        Errors[111] = "Erro extrair valores das variáveis do formulário!"
        Errors[112] = "Variáveis obrigatórias não foram passadas!"
        Errors[113] = "Os tipos das variáveis obrigatórias estão incorretos!"
        Errors[114] = "Erro ao decodificar as variáveis!"
        Errors[115] = "O tipo da variável está incorreto!"
        #VARIAVEIS DE AMBIENTE
        Errors[201] = "Não foi possivel resolver os dados de conexão da base de dados!"
        Errors[202] = "Erro interno na api - Tradução de dados de conexão da base de dados!"
        #CONEXÃO BASE DE DADOS
        Errors[300] = "Erro na conexão com o banco de dados, contate o suporte!"
        Errors[301] = "Erro ao se conectar à base de dados!"
        Errors[302] = "Erro interno na Api - Conexão na Base de Dados!"
        Errors[311] = "Erro ao autenticar a conexão com o banco de dados, contate o suporte!"
        #TIPO DISPOSITIVO
        Errors[401] = "Erro na listagem de tipo de dispositivo!"
        Errors[411] = "Erro na busca de tipos!"
        Errors[412] = "Erro interno na Api - busca tipo por id!"
        Errors[421] = "Erro interno na Api - busca tipo por nome!"
        Errors[431] = "A inserção foi bem sucedida, porém não encontramos os dados do tipo no banco!"
        Errors[432] = "A inserção foi bem sucedida, mas ocorreu um erro ao buscar os índices do dado!"
        Errors[433] = "Erro na inserção do tipo!"
        Errors[434] = "Erro interno na Api - inserir tipo!"
        Errors[441] = "A atualização do tipo foi bem sucedida, porém não encontramos os dados do tipo no banco!"
        Errors[442] = "A atualização do tipo foi bem sucedida, mas ocorreu um erro ao buscar os índices do tipo no banco!"
        Errors[443] = "Erro na atualização do tipo!"
        Errors[444] = "O id do tipo de dispositivo não foi localizado!"
        Errors[445] = "Erro interno na Api - atualizar tipo!"
        Errors[451] = "O nome do tipo a ser alterado não foi passado ou está incorreto!"
        Errors[452] = "Erro interno na Api - Atualizar nome do tipo!"
        Errors[461] = "A exclusão do tipo não foi bem sucedida!"
        Errors[462] = "A exclusão foi bem sucedida, mas ocorreu um erro ao buscar os índices do tipo!"
        Errors[463] = "Erro na exclusão do tipo!"
        Errors[464] = "Tipo já excluído!"
        Errors[465] = "Erro interno na Api - excluir tipo!"
        #500 - DISPOSITIVO
        Errors[501] = "Erro na listagem de dispositivo!"
        Errors[511] = "Erro interno na Api - busca dispositivo por id!"
        Errors[521] = "Erro na busca de dispositivo!"
        Errors[522] = "Erro interno na Api - busca dispositivo por texto!"
        Errors[531] = "A inserção foi bem sucedida, porém não encontramos os dados do dispositivo no banco!"
        Errors[532] = "A inserção foi bem sucedida, mas ocorreu um erro ao buscar os índices do dispositivo no banco!"
        Errors[533] = "Erro na inserção dos dispositivo!"
        Errors[534] = "Erro interno na Api - inserir dispositivo!"
        Errors[541] = "A atualização foi bem sucedida, porém não encontramos os dados do dispositivo no banco!"
        Errors[542] = "A atualização foi bem sucedida, mas ocorreu um erro ao buscar os índices do dispositivo no banco!"
        Errors[543] = "Erro na atualização do dispositivo!"
        Errors[544] = "O id do dispositivo não foi localizado!"
        Errors[545] = "Erro interno na Api - atualizar dispositivo!"
        Errors[551] = "O nome do dispositivo a ser alterado não foi passado ou está incorreto!"
        Errors[552] = "Erro interno na Api - Atualizar nome do dispositivo!"
        Errors[561] = "O codigo do dispositivo a ser alterado não foi passado ou está incorreto!"
        Errors[562] = "Erro interno na Api - Atualizar codigo do dispositivo!"
        Errors[571] = "A exclusão do dispositivo não foi bem sucedida!"
        Errors[572] = "A exclusão foi bem sucedida, mas ocorreu um erro ao buscar os índices do dispositivo!"
        Errors[573] = "Erro na exclusão do dispositivo!"
        Errors[574] = "Dispositivo já excluído!"
        Errors[575] = "Erro interno na Api - excluir dispositivo!"
        #600 - AMBIENTE
        Errors[601] = "Erro na listagem de ambiente!"
        Errors[611] = "Erro na busca de ambiente!"
        Errors[612] = "Erro interno na Api - busca ambiente por id!"
        Errors[621] = "Erro interno na Api - busca ambiente por texto!"
        Errors[631] = "A inserção foi bem sucedida, porém não encontramos os dados do ambiente no banco!"
        Errors[632] = "A inserção foi bem sucedida, mas ocorreu um erro ao buscar os índices do ambiente no banco!"
        Errors[633] = "Erro na inserção dos ambiente!"
        Errors[634] = "Erro interno na Api - inserir ambiente!"
        Errors[641] = "A atualização foi bem sucedida, porém não encontramos os dados do ambiente no banco!"
        Errors[642] = "A atualização foi bem sucedida, mas ocorreu um erro ao buscar os índices do ambiente no banco!"
        Errors[643] = "Erro na atualização do ambiente!"
        Errors[644] = "O id do ambiente não foi localizado!"
        Errors[645] = "Erro interno na Api - atualizar ambiente!"
        Errors[651] = "O nome do ambiente a ser alterado não foi passado ou está incorreto!"
        Errors[652] = "Erro interno na Api - Atualizar nome do ambiente!"
        Errors[661] = "Erro ao atualizar a descrição do ambiente!"
        Errors[662] = "A descrição do ambiente a ser alterado não foi passado ou está incorreto!"
        Errors[663] = "Erro interno na Api - Atualizar descrição do ambiente!"
        Errors[671] = "A exclusão do ambiente não foi bem sucedida!"
        Errors[672] = "A exclusão foi bem sucedida, mas ocorreu um erro ao buscar os índices do ambiente!"
        Errors[673] = "Erro na exclusão do ambiente!"
        Errors[674] = "Ambiente já excluído!"
        Errors[675] = "Erro interno na Api - excluir ambiente!"

        error = Errors[int] if int in Errors.keys() else None

        if error != None:

            return error

        else:

            return f"Ocorreu um erro, entre em contato com o suporte! (error code {int})"

class WebApi(Bottle):

    def __init__(self):

        super().__init__()

        # TipoDispositivo

        self.route("/microservices/web/dispositivo/tipo/get/all", method = "GET", callback = self.TipoDispositivoGetAll)

        self.route("/microservices/web/dispositivo/tipo/get/actives", method = "GET", callback = self.TipoDispositivoGetAll)

        self.route("/microservices/web/dispositivo/tipo/getby/id", method = "GET", callback = self.TipoDispositivoGetById)

        self.route("/microservices/web/dispositivo/tipo/getby/name", method = "GET", callback = self.TipoDispositivoGetByName)

        self.route("/microservices/web/dispositivo/tipo/insert", method = "POST", callback = self.TipoDispositivoInsert)

        self.route("/microservices/web/dispositivo/tipo/update", method = "PUT", callback = self.TipoDispositivoUpdate)

        self.route("/microservices/web/dispositivo/tipo/update/name", method = "PATCH", callback = self.TipoDispositivoUpdateName)

        self.route("/microservices/web/dispositivo/tipo/delete", method = "DELETE", callback = self.TipoDispositivoDelete)

        # Dispositivo

        self.route("/microservices/web/dispositivo/get/all", method = "GET", callback = self.DispositivoGetAll)

        self.route("/microservices/web/dispositivo/get/actives", method = "GET", callback = self.DispositivoGetAll)

        self.route("/microservices/web/dispositivo/getby/id", method = "GET", callback = self.DispositivoGetById)

        self.route("/microservices/web/dispositivo/getby/id/type", method = "GET", callback = self.DispositivoGetById)

        self.route("/microservices/web/dispositivo/getby/id/environment", method = "GET", callback = self.DispositivoGetById)

        self.route("/microservices/web/dispositivo/getby/string/name", method = "GET", callback = self.DispositivoGetByString)

        self.route("/microservices/web/dispositivo/getby/string/code", method = "GET", callback = self.DispositivoGetByString)

        self.route("/microservices/web/dispositivo/insert", method = "POST", callback = self.DispositivoInsert)

        self.route("/microservices/web/dispositivo/update", method = "PUT", callback = self.DispositivoUpdate)

        self.route("/microservices/web/dispositivo/update/name", method = "PATCH", callback = self.DispositivoUpdateName) 
            
        self.route("/microservices/web/dispositivo/update/code", method = "PATCH", callback = self.DispositivoUpdateCode) 
               
        self.route("/microservices/web/dispositivo/delete", method = "DELETE", callback = self.DispositivoDelete)

        # Ambiente

        self.route("/microservices/web/ambiente/get/all", method = "GET", callback = self.AmbienteGetAll)

        self.route("/microservices/web/ambiente/get/actives", method = "GET", callback = self.AmbienteGetAll)

        self.route("/microservices/web/ambiente/getby/id", method = "GET", callback = self.AmbienteGetById)

        self.route("/microservices/web/ambiente/getby/string/name", method = "GET", callback = self.AmbienteGetByString)

        self.route("/microservices/web/ambiente/getby/string/description", method = "GET", callback = self.AmbienteGetByString)

        self.route("/microservices/web/ambiente/insert", method = "POST", callback = self.AmbienteInsert)

        self.route("/microservices/web/ambiente/update", method = "PUT", callback = self.AmbienteUpdate)

        self.route("/microservices/web/ambiente/update/name", method = "PATCH", callback = self.AmbienteUpdateName)

        self.route("/microservices/web/ambiente/update/description", method = "PATCH", callback = self.AmbienteUpdateDescription)

        self.route("/microservices/web/ambiente/delete", method = "DELETE", callback = self.AmbienteDelete)

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

            SQL     = "SELECT * FROM TIPODISPOSITIVO "
            Sucess  = True
            Errors  = []
            Data    = []

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

                self.conn.rollback()
                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(401)})

            finally:

                cur.close()

                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})
        
        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

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

                            self.conn.rollback()
                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(411)})

                        finally:

                            cur.close()

                    elif str(idbusca) == "":

                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(104)})

                    else:

                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(109)})

                else:

                    Sucess = False

                    for error in variavelErrors:

                        Errors.append({"msg": list(error.values())[0]})
                        
            except:

                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(412)})

            finally:

                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})
        
        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

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
                    nomebusca = StringHandling.CleanSqlString(nomebusca)

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

                            self.conn.rollback()
                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(411)})

                        finally:

                            cur.close()

                    else:

                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(104)})
                else:

                    Sucess = False

                    for error in variavelErrors:

                        Errors.append({"msg": list(error.values())[0]})

            except:

                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(421)})

            finally:

                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

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
                cadastra = StringHandling.CleanSqlString(cadastra) if cadastra != None else cadastra

                if cadastra != None and cadastra != "":
                    
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
                                Errors.append({"msg": ErrorsDict.errorcode(431)})
                        
                        except:

                            self.conn.rollback()
                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(432)})
                        
                        finally:
                        
                            cur.close()
                    
                    except:

                        self.conn.rollback()                    
                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(433)})
                    
                    finally:
                    
                        cur.close()
                
                else:
                
                    Sucess = False
                    Errors.append({"msg": ErrorsDict.errorcode(110)})
            
            except:
            
                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(434)})
            
            finally:
            
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

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
                    Errors.append({"msg": ErrorsDict.errorcode(105)})

                elif idtipo != None and str(idtipo).isnumeric():

                    request.query.update({'idbusca': f'{idtipo}'})
                    DataBefore          = json.loads(self.TipoDispositivoGetById())
                    DataBeforeStatus    = list(DataBefore.values())[0]
                    DataBeforeErrors    = list(DataBefore.values())[1]
                    DataBeforeData      = list(DataBefore.values())[2]

                    if  DataBeforeStatus == True and DataBeforeData:

                        columns = 0
                        SQL     = "UPDATE TIPODISPOSITIVO SET "

                        nome = FormData.get("nome") if "nome" in FormData.keys() else None
                        nome = StringHandling.CleanSqlString(nome) if nome != None else nome
                    
                        if nome != None and nome != "":

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
                                        Errors.append({"msg": ErrorsDict.errorcode(441)})
                                
                                except:

                                    self.conn.rollback()                                
                                    Sucess = False
                                    Errors.append({"msg": ErrorsDict.errorcode(442)})
                                
                                finally:
                                
                                    cur.close()
                            
                            except:

                                self.conn.rollback()                            
                                Sucess = False
                                Errors.append({"msg": ErrorsDict.errorcode(443)})
                            
                            finally:
                            
                                cur.close()
                        
                        else:
                        
                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(106)})
                    
                    else:
                    
                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(444)})

                        for error in DataBeforeErrors:

                            Errors.append({"msg": list(error.values())[0]})
                
                else:
                
                    Sucess = False
                    Errors.append({"msg": ErrorsDict.errorcode(107)})
            
            except:
            
                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(445)})
            
            finally:
            
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

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
                nome    = StringHandling.CleanSqlString(nome) if nome != None else nome

                if idtipo != None and str(idtipo).isnumeric():

                    if nome != None and nome != "":

                        SQL = "UPDATE TIPODISPOSITIVO SET NOME = '{}' WHERE IDTIPO = {}".format(
                            nome ,
                            idtipo
                        )
                        request.query.update({'idbusca': f'{idtipo}'})
                        DataBefore          = json.loads(self.TipoDispositivoGetById())
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
                                        Errors.append({"msg": ErrorsDict.errorcode(441)})
                                
                                except:

                                    self.conn.rollback()                            
                                    Sucess = False
                                    Errors.append({"msg": ErrorsDict.errorcode(442)})
                            
                                finally:
                            
                                    cur.close()
                            
                            except:

                                self.conn.rollback()                            
                                Sucess = False
                                Errors.append({"msg": ErrorsDict.errorcode(443)})
                            
                            finally:
                            
                                cur.close()
                        
                        else:
                        
                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(444)})

                            for error in DataBeforeErrors:

                                Errors.append({"msg": list(error.values())[0]})
                    
                    else:
                    
                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(451)})
                
                else:
                
                    Sucess = False
                    Errors.append({"msg": ErrorsDict.errorcode(107)})
            
            except:
            
                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(452)})
            
            finally:
            
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

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

                    if  DataBeforeStatus == True and DataBeforeData and IndSitPosition != -1:

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
                                        Errors.append({"msg": ErrorsDict.errorcode(461)})

                                except:

                                    self.conn.rollback()
                                    Sucess = False
                                    Errors.append({"msg": ErrorsDict.errorcode(462)})

                                finally:
                                
                                    cur.close()
                            
                            except:

                                self.conn.rollback()                
                                Sucess = False
                                Errors.append({"msg": ErrorsDict.errorcode(463)})
                            
                            finally:

                                cur.close()
                        
                        else:
                        
                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(464)})
                    
                    else:
                    
                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(444)})

                        for error in DataBeforeErrors:

                            Errors.append({"msg": list(error.values())[0]})

                else:

                    Sucess = False
                    Errors.append({"msg": ErrorsDict.errorcode(107)})

            except:

                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(465)})

            finally:

                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

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
            
                chamada = request['bottle.route'].rule.replace("/microservices/web/dispositivo/get/", "")

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

                self.conn.rollback()
                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(501)})
            
            finally:
            
                cur.close()
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

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
                        anotherroutes = [   
                                            "/microservices/web/dispositivo/update",
                                            "/microservices/web/dispositivo/update/name", 
                                            "/microservices/web/dispositivo/update/code",
                                            "/microservices/web/dispositivo/delete"
                                        ]

                        if chamada == "type":

                            SQL = SQL + f"AND IDTIPO = {idbusca} "
                            returnLines = 100

                        elif chamada == "environment":

                            SQL = SQL + f"AND IDAMBIENTE = {idbusca} "
                            returnLines = 100

                        elif chamada == route or chamada in anotherroutes:

                            SQL = SQL + f"AND IDDISPOSITIVO = {idbusca} "
                            returnLines = 1

                        else:

                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(108)})

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

                            self.conn.rollback()                           
                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(501)})
                        
                        finally:
                        
                            cur.close()
                    
                    elif str(idbusca) == "":
                    
                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(104)})
                    
                    else:
                    
                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(109)})
                
                else:
                
                    Sucess = False
                    msgs = list(list(variavelErrors)[0].values())

                    for msg in msgs:
                    
                        Errors.append({"msg": msg})
            
            except:
            
                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(511)})
            
            finally:
            
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

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
                    textobusca = StringHandling.CleanSqlString(textobusca) if textobusca != None else textobusca

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
                            Errors.append({"msg": ErrorsDict.errorcode(108)})

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
            
                            self.conn.rollback()                            
                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(521)})
                        
                        finally:
                        
                            cur.close()

                    else:

                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(104)})
                
                else:
                
                    Sucess = False
                    msgs = list(list(variavelErrors)[0].values())

                    for msg in msgs:
                    
                        Errors.append({"msg": msg})
            
            except:
            
                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(522)})
            
            finally:
            
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

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

                        codigodispositivo   = StringHandling.CleanSqlString(codigodispositivo)
                        nome                = StringHandling.CleanSqlString(nome)
                        descricao           = StringHandling.CleanSqlString(descricao)
                        orientacao          = StringHandling.CleanSqlString(orientacao)
                            
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
                                    Errors.append({"msg": ErrorsDict.errorcode(531)})
                            
                            except:

                                self.conn.rollback()
                                Sucess = False
                                Errors.append({"msg": ErrorsDict.errorcode(532)})
                            
                            finally:
                            
                                cur.close()
                        
                        except:
                            
                            self.conn.rollback()
                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(533)})
                        
                        finally:
                        
                            cur.close()
                    
                    except:
                    
                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(534)})

                elif MandatoryVarsExists == False:

                    Sucess = False
                    Errors.append({"msg": ErrorsDict.errorcode(112)})

                else: #MandatoryVarsTypes == False

                    Sucess = False
                    Errors.append({"msg": ErrorsDict.errorcode(113)})
            
            except:

                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(114)})

            finally:

                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

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
                    Errors.append({"msg": ErrorsDict.errorcode(105)})

                elif iddispositivo != None and str(iddispositivo).isnumeric():

                    request.query.update({'idbusca': f'{iddispositivo}'})

                    DataBefore          = json.loads(self.DispositivoGetById())
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

                        codigodispositivo   =   StringHandling.CleanSqlString(codigodispositivo) \
                                                if codigodispositivo != None else codigodispositivo
                        nome                =   StringHandling.CleanSqlString(nome) \
                                                if nome != None else nome
                        descricao           =   StringHandling.CleanSqlString(descricao) \
                                                if descricao != None else descricao
                        orientacao          =   StringHandling.CleanSqlString(orientacao) \
                                                if orientacao != None else orientacao

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
                                            Errors.append({"msg": ErrorsDict.errorcode(541)})
                                    
                                    except:

                                        self.conn.rollback()                                    
                                        Sucess = False
                                        Errors.append({"msg": ErrorsDict.errorcode(542)})
                                    
                                    finally:
                                    
                                        cur.close()
                                
                                except:

                                    self.conn.rollback()                                
                                    Sucess = False
                                    Errors.append({"msg": ErrorsDict.errorcode(543)})
                                
                                finally:
                                
                                    cur.close()
                            
                            else:
                            
                                Sucess = False
                                Errors.append({"msg": ErrorsDict.errorcode(106)})

                        else:

                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(115)})
                        
                    else:
                    
                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(544)})
                    
                else:
                
                    Sucess = False
                    Errors.append({"msg": ErrorsDict.errorcode(107)})
            
            except:
            
                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(545)})
            
            finally:
            
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    def DispositivoUpdateName(self):

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

                iddispositivo   = FormData.get("id")    if "id"     in FormData.keys()  else None
                nome            = FormData.get("nome")  if "nome"   in FormData.keys()  else None
                nome            = StringHandling.CleanSqlString(nome) if nome != None else nome

                if iddispositivo != None and str(iddispositivo).isnumeric():

                    if nome != None and nome != "":

                        SQL = "UPDATE DISPOSITIVO SET NOME = '{}' WHERE IDDISPOSITIVO = {}".format(
                            nome ,
                            iddispositivo
                        )
                        request.query.update({'idbusca': f'{iddispositivo}'})
                        DataBefore          = json.loads(self.DispositivoGetById())
                        DataBeforeStatus    = list(DataBefore.values())[0]
                        DataBeforeErrors    = list(DataBefore.values())[1]
                        DataBeforeData      = list(DataBefore.values())[2]                        

                        if  DataBeforeStatus == True and DataBeforeData:

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
                                        Errors.append({"msg": ErrorsDict.errorcode(541)})
                                
                                except:

                                    self.conn.rollback()                            
                                    Sucess = False
                                    Errors.append({"msg": ErrorsDict.errorcode(542)})
                            
                                finally:
                            
                                    cur.close()
                            
                            except:

                                self.conn.rollback()                            
                                Sucess = False
                                Errors.append({"msg": ErrorsDict.errorcode(543)})
                            
                            finally:
                            
                                cur.close()
                        
                        else:
                        
                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(544)})

                            for error in DataBeforeErrors:

                                Errors.append({"msg": list(error.values())[0]})
                    
                    else:
                    
                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(551)})
                
                else:
                
                    Sucess = False
                    Errors.append({"msg": ErrorsDict.errorcode(107)})
            
            except:
            
                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(552)})
            
            finally:
            
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    def DispositivoUpdateCode(self):

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

                iddispositivo   = FormData.get("id")        if "id"     in FormData.keys()  else None
                codigo          = FormData.get("codigo")    if "codigo" in FormData.keys()  else None
                codigo          = StringHandling.CleanSqlString(codigo) if codigo != None   else codigo

                if iddispositivo != None and str(iddispositivo).isnumeric():

                    if codigo != None and codigo != "":

                        SQL = "UPDATE DISPOSITIVO SET CODIGODISPOSITIVO = '{}' WHERE IDDISPOSITIVO = {}".format(
                            codigo ,
                            iddispositivo
                        )
                        request.query.update({'idbusca': f'{iddispositivo}'})
                        DataBefore          = json.loads(self.DispositivoGetById())
                        DataBeforeStatus    = list(DataBefore.values())[0]
                        DataBeforeErrors    = list(DataBefore.values())[1]
                        DataBeforeData      = list(DataBefore.values())[2]                        

                        if  DataBeforeStatus == True and DataBeforeData:

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
                                        Errors.append({"msg": ErrorsDict.errorcode(541)})
                                
                                except:

                                    self.conn.rollback()                            
                                    Sucess = False
                                    Errors.append({"msg": ErrorsDict.errorcode(542)})
                            
                                finally:
                            
                                    cur.close()
                            
                            except:

                                self.conn.rollback()                            
                                Sucess = False
                                Errors.append({"msg": ErrorsDict.errorcode(543)})
                            
                            finally:
                            
                                cur.close()
                        
                        else:
                        
                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(544)})

                            for error in DataBeforeErrors:

                                Errors.append({"msg": list(error.values())[0]})
                    
                    else:
                    
                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(561)})
                
                else:
                
                    Sucess = False
                    Errors.append({"msg": ErrorsDict.errorcode(107)})
            
            except:
            
                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(562)})
            
            finally:
            
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    def DispositivoDelete(self):

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

                if iddispositivo != None and str(iddispositivo).isnumeric():

                    request.query.update({'idbusca': f'{iddispositivo}'})
                    DataBefore          = json.loads(self.DispositivoGetById())
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

                    if  DataBeforeStatus == True and DataBeforeData and IndSitPosition != -1:

                        if  list(list(DataBeforeData)[0].values())[IndSitPosition] != 2:

                            SQL = f"UPDATE DISPOSITIVO SET IND_SIT = 2 WHERE IDDISPOSITIVO = {iddispositivo}"

                            try:

                                cur = self.conn.cursor()
                                cur.execute(SQL)
                                self.conn.commit()

                                try:

                                    SQL =  f"SELECT 1 FROM DISPOSITIVO " + \
                                           f"WHERE IDDISPOSITIVO = {iddispositivo} AND IND_SIT <> 2 " + \
                                            "ORDER BY IDDISPOSITIVO"

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
                                        Errors.append({"msg": ErrorsDict.errorcode(571)})

                                except:

                                    self.conn.rollback()
                                    Sucess = False
                                    Errors.append({"msg": ErrorsDict.errorcode(572)})

                                finally:
                                
                                    cur.close()
                            
                            except:

                                self.conn.rollback()                
                                Sucess = False
                                Errors.append({"msg": ErrorsDict.errorcode(573)})
                            
                            finally:

                                cur.close()
                        
                        else:
                        
                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(574)})
                    
                    else:
                    
                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(544)})

                        for error in DataBeforeErrors:

                            Errors.append({"msg": list(error.values())[0]})

                else:

                    Sucess = False
                    Errors.append({"msg": ErrorsDict.errorcode(107)})

            except:

                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(575)})

            finally:

                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    #   Ambiente

    def AmbienteGetAll(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus == True:

            SQL     = "SELECT * FROM AMBIENTE "
            Sucess  = True
            Errors  = []
            Data    = []

            try:
            
                chamada = request['bottle.route'].rule.replace("/microservices/web/ambiente/get/", "")

                if chamada == "actives":

                    SQL = SQL + "WHERE IND_SIT = 1 " 

                SQL = SQL + "ORDER BY IDAMBIENTE"

                cur = self.conn.cursor()
                cur.execute(SQL)
                row_headers = [x[0] for x in cur.description]
                rv = cur.fetchall()
                self.conn.commit()

                for result in rv:

                    Data.append(dict(zip(row_headers, result)))

            except:

                self.conn.rollback()
                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(601)})
            
            finally:
            
                cur.close()
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    def AmbienteGetById(self):

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
                
                        SQL = "SELECT * FROM AMBIENTE WHERE 1 = 1 "

                        route   = "/microservices/web/ambiente/getby/id"
                        chamada = request['bottle.route'].rule.replace(route + "/", "")
                        anotherroutes = [
                                            "/microservices/web/ambiente/update",
                                            "/microservices/web/ambiente/update/name",
                                            "/microservices/web/ambiente/update/description",
                                            "/microservices/web/ambiente/delete"
                                        ]

                        if chamada == route or chamada in anotherroutes:

                            SQL = SQL + f"AND IDAMBIENTE = {idbusca} "
                            returnLines = 1

                        else:

                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(108)})

                            return({"sucess":Sucess,"errors":Errors,"data":Data})
                
                        try:

                            SQL = SQL + "ORDER BY IDAMBIENTE"
                
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

                            self.conn.rollback()                           
                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(611)})
                        
                        finally:
                        
                            cur.close()
                    
                    elif str(idbusca) == "":
                    
                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(104)})
                    
                    else:
                    
                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(109)})
                
                else:
                
                    Sucess = False
                    msgs = list(list(variavelErrors)[0].values())

                    for msg in msgs:
                    
                        Errors.append({"msg": msg})
            
            except:
            
                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(612)})
            
            finally:
            
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    def AmbienteGetByString(self):

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
                    textobusca = StringHandling.CleanSqlString(textobusca) if textobusca != None else textobusca

                    if textobusca != "":
                
                        SQL = "SELECT * FROM AMBIENTE WHERE 1 = 1 "

                        route = "/microservices/web/ambiente/getby/string"
                        chamada = request['bottle.route'].rule.replace(route + "/", "")

                        if chamada == "name":

                            SQL = SQL + f"AND UPPER(NOME) LIKE '%{str(textobusca).upper()}%' "

                        elif chamada == "description":

                            SQL = SQL + f"AND UPPER(DESCRICAO) LIKE '%{str(textobusca).upper()}%' "

                        else:

                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(108)})

                            return({"sucess":Sucess,"errors":Errors,"data":Data})

                        try:

                            SQL = SQL + "ORDER BY IDAMBIENTE"
                    
                            cur = self.conn.cursor()
                            cur.execute(SQL)
                            row_headers = [x[0] for x in cur.description]
                            rv = cur.fetchall()
                            self.conn.commit()

                            for result in rv:

                                Data.append(dict(zip(row_headers, result)))

                        except:
            
                            self.conn.rollback()                            
                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(611)})
                        
                        finally:
                        
                            cur.close()

                    else:

                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(104)})
                
                else:
                
                    Sucess = False
                    msgs = list(list(variavelErrors)[0].values())

                    for msg in msgs:
                    
                        Errors.append({"msg": msg})
            
            except:
            
                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(621)})
            
            finally:
            
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    def AmbienteInsert(self):

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

                MandatoryVars = ["nome"]

                MandatoryVarsExists = True

                for var in MandatoryVars:

                    if var not in FormData.keys():

                        MandatoryVarsExists = False

                MandatoryVarsTypes = True if FormData.get("nome") != "" else False   

                if MandatoryVarsExists == True and MandatoryVarsTypes == True:

                    try:
                        
                        nome        = FormData.get("nome")
                        descricao   = FormData.get("descricao") if "descricao" in FormData.keys() else ""

                        nome        = StringHandling.CleanSqlString(nome)
                        descricao   = StringHandling.CleanSqlString(descricao)
                            
                        SQL = " INSERT INTO AMBIENTE    (" + \
                                                            "NOME , " + \
                                                            "DESCRICAO , " + \
                                                            "IND_SIT" + \
                                                        ")" + \
                                "VALUES " + " ('{}', '{}', 1)".format(
                                    nome ,
                                    descricao
                                )

                        try:

                            cur = self.conn.cursor()
                            cur.execute(SQL)
                            self.conn.commit()

                            try:

                                SQL = "SELECT * FROM AMBIENTE ORDER BY IDAMBIENTE DESC LIMIT 1"

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
                                    Errors.append({"msg": ErrorsDict.errorcode(631)})
                            
                            except:

                                self.conn.rollback()
                                Sucess = False
                                Errors.append({"msg": ErrorsDict.errorcode(632)})
                            
                            finally:
                            
                                cur.close()
                        
                        except:
                            
                            self.conn.rollback()
                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(633)})
                        
                        finally:
                        
                            cur.close()
                    
                    except:
                    
                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(634)})

                elif MandatoryVarsExists == False:

                    Sucess = False
                    Errors.append({"msg": ErrorsDict.errorcode(112)})

                else: #MandatoryVarsTypes == False

                    Sucess = False
                    Errors.append({"msg": ErrorsDict.errorcode(113)})
            
            except:

                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(114)})

            finally:

                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    def AmbienteUpdate(self):

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

                idambiente = FormData.get("id") if "id" in FormData.keys() else None

                if not FormData:

                    Sucess = False
                    Errors.append({"msg": ErrorsDict.errorcode(105)})

                elif idambiente != None and str(idambiente).isnumeric():

                    request.query.update({'idbusca': f'{idambiente}'})

                    DataBefore          = json.loads(self.AmbienteGetById())
                    DataBeforeStatus    = list(DataBefore.values())[0]
                    DataBeforeErrors    = list(DataBefore.values())[1]
                    DataBeforeData      = list(DataBefore.values())[2]

                    if  DataBeforeStatus == True and DataBeforeData:

                        nome                = FormData.get("nome")          if "nome"       in FormData.keys()  else None
                        descricao           = FormData.get("descricao")     if "descricao"  in FormData.keys()  else None

                        nome                =   StringHandling.CleanSqlString(nome) \
                                                if nome != None else nome
                        descricao           =   StringHandling.CleanSqlString(descricao) \
                                                if descricao != None else descricao

                        columns = 0
                        SQL     = "UPDATE AMBIENTE SET "

                        if nome != None and nome != "":

                            SQL     = StringHandling.AddColumns(columns, SQL)
                            SQL     = SQL + f"NOME = '{nome}'"
                            columns = columns + 1

                        if descricao != None and descricao != "":

                            SQL     = StringHandling.AddColumns(columns, SQL)
                            SQL     = SQL + f"DESCRICAO = '{descricao}'"
                            columns = columns + 1

                        if columns > 0:

                            SQL = SQL + f" WHERE 1 = 1 AND IDAMBIENTE = {idambiente}"

                            try:
                            
                                cur = self.conn.cursor()
                                cur.execute(SQL)
                                self.conn.commit()

                                try:
                            
                                    SQL =  f"SELECT * FROM AMBIENTE " + \
                                           f"WHERE IDAMBIENTE = {idambiente} " + \
                                            "ORDER BY IDAMBIENTE"
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
                                        Errors.append({"msg": ErrorsDict.errorcode(641)})
                                
                                except:

                                    self.conn.rollback()                                    
                                    Sucess = False
                                    Errors.append({"msg": ErrorsDict.errorcode(642)})
                                
                                finally:
                                
                                    cur.close()
                            
                            except:

                                self.conn.rollback()                                
                                Sucess = False
                                Errors.append({"msg": ErrorsDict.errorcode(643)})
                            
                            finally:
                            
                                cur.close()
                        
                        else:
                        
                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(106)})
                    
                    else:
                    
                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(644)})
                    
                else:
                
                    Sucess = False
                    Errors.append({"msg": ErrorsDict.errorcode(107)})
            
            except:
            
                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(645)})
            
            finally:
            
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    def AmbienteUpdateName(self):

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

                idambiente      = FormData.get("id")    if "id"     in FormData.keys()  else None
                nome            = FormData.get("nome")  if "nome"   in FormData.keys()  else None
                nome            = StringHandling.CleanSqlString(nome) if nome != None else nome

                if idambiente != None and str(idambiente).isnumeric():

                    if nome != None and nome != "":

                        SQL = "UPDATE AMBIENTE SET NOME = '{}' WHERE IDAMBIENTE = {}".format(
                            nome ,
                            idambiente
                        )
                        request.query.update({'idbusca': f'{idambiente}'})
                        DataBefore          = json.loads(self.AmbienteGetById())
                        DataBeforeStatus    = list(DataBefore.values())[0]
                        DataBeforeErrors    = list(DataBefore.values())[1]
                        DataBeforeData      = list(DataBefore.values())[2]

                        if  DataBeforeStatus == True and DataBeforeData:

                            try:

                                cur = self.conn.cursor()
                                cur.execute(SQL)
                                self.conn.commit()

                                try:

                                    SQL =  f"SELECT * FROM AMBIENTE " + \
                                           f"WHERE IDAMBIENTE = {idambiente} " + \
                                            "ORDER BY IDAMBIENTE"

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
                                        Errors.append({"msg": ErrorsDict.errorcode(541)})
                                
                                except:

                                    self.conn.rollback()                            
                                    Sucess = False
                                    Errors.append({"msg": ErrorsDict.errorcode(642)})
                            
                                finally:
                            
                                    cur.close()
                            
                            except:

                                self.conn.rollback()                            
                                Sucess = False
                                Errors.append({"msg": ErrorsDict.errorcode(643)})
                            
                            finally:
                            
                                cur.close()
                        
                        else:
                        
                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(644)})

                            for error in DataBeforeErrors:

                                Errors.append({"msg": list(error.values())[0]})
                    
                    else:
                    
                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(651)})
                
                else:
                
                    Sucess = False
                    Errors.append({"msg": ErrorsDict.errorcode(107)})
            
            except:
            
                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(652)})
            
            finally:
            
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    def AmbienteUpdateDescription(self):

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

                idambiente  = FormData.get("id")            if "id"         in FormData.keys()  else None
                descricao   = FormData.get("descricao")     if "descricao"  in FormData.keys()  else None
                descricao   = StringHandling.CleanSqlString(descricao) if descricao != None else descricao

                if idambiente != None and str(idambiente).isnumeric():

                    if descricao != None and descricao != "":

                        SQL = "UPDATE AMBIENTE SET DESCRICAO = '{}' WHERE IDAMBIENTE = {}".format(
                            descricao ,
                            idambiente
                        )
                        request.query.update({'idbusca': f'{idambiente}'})
                        DataBefore          = json.loads(self.AmbienteGetById())
                        DataBeforeStatus    = list(DataBefore.values())[0]
                        DataBeforeErrors    = list(DataBefore.values())[1]
                        DataBeforeData      = list(DataBefore.values())[2]

                        if  DataBeforeStatus == True and DataBeforeData:

                            try:

                                cur = self.conn.cursor()
                                cur.execute(SQL)
                                self.conn.commit()

                                try:

                                    SQL =  f"SELECT * FROM AMBIENTE " + \
                                           f"WHERE IDAMBIENTE = {idambiente} " + \
                                            "ORDER BY IDAMBIENTE"

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
                                        Errors.append({"msg": ErrorsDict.errorcode(641)})
                                
                                except:

                                    self.conn.rollback()                            
                                    Sucess = False
                                    Errors.append({"msg": ErrorsDict.errorcode(642)})
                            
                                finally:
                            
                                    cur.close()
                            
                            except:

                                self.conn.rollback()                            
                                Sucess = False
                                Errors.append({"msg": ErrorsDict.errorcode(661)})
                            
                            finally:
                            
                                cur.close()
                        
                        else:
                        
                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(644)})

                            for error in DataBeforeErrors:

                                Errors.append({"msg": list(error.values())[0]})
                    
                    else:
                    
                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(662)})
                
                else:
                
                    Sucess = False
                    Errors.append({"msg": ErrorsDict.errorcode(107)})
            
            except:
            
                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(663)})
            
            finally:
            
                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    def AmbienteDelete(self):

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

                idambiente = FormData.get("id") if "id" in FormData.keys() else None

                if idambiente != None and str(idambiente).isnumeric():

                    request.query.update({'idbusca': f'{idambiente}'})
                    DataBefore          = json.loads(self.AmbienteGetById())
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

                    if  DataBeforeStatus == True and DataBeforeData and IndSitPosition != -1:

                        if  list(list(DataBeforeData)[0].values())[IndSitPosition] != 2:

                            SQL = f"UPDATE AMBIENTE SET IND_SIT = 2 WHERE IDAMBIENTE = {idambiente}"

                            try:

                                cur = self.conn.cursor()
                                cur.execute(SQL)
                                self.conn.commit()

                                try:

                                    SQL =  f"SELECT 1 FROM AMBIENTE " + \
                                           f"WHERE IDAMBIENTE = {idambiente} AND IND_SIT <> 2 " + \
                                            "ORDER BY IDAMBIENTE"

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
                                        Errors.append({"msg": ErrorsDict.errorcode(671)})

                                except:

                                    self.conn.rollback()
                                    Sucess = False
                                    Errors.append({"msg": ErrorsDict.errorcode(672)})

                                finally:
                                
                                    cur.close()
                            
                            except:

                                self.conn.rollback()                
                                Sucess = False
                                Errors.append({"msg": ErrorsDict.errorcode(673)})
                            
                            finally:

                                cur.close()
                        
                        else:
                        
                            Sucess = False
                            Errors.append({"msg": ErrorsDict.errorcode(674)})
                    
                    else:
                    
                        Sucess = False
                        Errors.append({"msg": ErrorsDict.errorcode(644)})

                        for error in DataBeforeErrors:

                            Errors.append({"msg": list(error.values())[0]})

                else:

                    Sucess = False
                    Errors.append({"msg": ErrorsDict.errorcode(107)})

            except:

                Sucess = False
                Errors.append({"msg": ErrorsDict.errorcode(675)})

            finally:

                return json.dumps({"sucess": Sucess, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.errorcode(300)}]

            return json.dumps({"sucess": connectionStatus, "errors": Errors, "data": connectionData})

    #   Medição

if __name__ == '__main__':

    webapi = WebApi()
    webapi.run(host='0.0.0.0', port=8081, debug=True)
