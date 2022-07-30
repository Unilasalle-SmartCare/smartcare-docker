from bottle import Bottle, request
from datetime import datetime
from urllib.parse import parse_qs
import json
import os
import psycopg2
import requests
import ErrorsDict
import ListHandling

class PageError():

    def error400(error):

        return json.dumps({"success": False, "error": [{"msg": "400 Bad Request"}], "data": [{}]})

    def error401(error):

        return json.dumps({"success": False, "error": [{"msg": "401 Unauthorised"}], "data": [{}]})

    def error403(error):

        return json.dumps({"success": False, "error": [{"msg": "403 Forbidden"}], "data": [{}]})

    def error404(error):

        # Se em algum momento for usar html como resposta de erro
        # import codecs

        # file = codecs.open("./error-pages/404.html", "r", "utf-8")
        # HTML = file.read()
        # file.close()

        return json.dumps({"success": False, "errors": [{"msg": "404 Not Found"}], "data": [{}]})

    def error405(error):

        return json.dumps({"success": False, "errors": [{"msg": "405 Method Not Allowed"}], "data": [{}]})

    def error408(error):

        return json.dumps({"success": False, "errors": [{"msg": "408 Request Time-Out"}], "data": [{}]})

    def error500(error):

        return json.dumps({"success": False, "errors": [{"msg": "500 Internal Server Error"}], "data": [{}]})

    def error501(error):

        return json.dumps({"success": False, "errors": [{"msg": "501 Not Implemented"}], "data": [{}]})

    def error502(error):

        return json.dumps({"success": False, "errors": [{"msg": "502 Service Temporarily Overloaded"}], "data": [{}]})

    def error503(error):

        return json.dumps({"success": False, "errors": [{"msg": "503 Service Unavailable"}], "data": [{}]})

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

    def isdatetime(string):

        Retorno = True

        try:

            formato = f"%Y%m%d %H:%M:%S"

            datetime.strptime(string, formato)

        except:

            try:

                formato = f"%Y%m%d"

                datetime.strptime(string, formato)

            except:

                Retorno = False

        finally:

            return Retorno

class UrlHandling():

    def FindGetVars(varsearch):

        Success  = True
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

            if repeats > 1:

                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(101)})

            elif repeats == 0:

                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(102)})

            else:

                Data.append({varsearch: search})

            if not Success:

                try:

                    keys = request.query.keys()

                    for key in keys:

                        if key == "idbusca":

                            idbusca = request.query.get("idbusca")
                            Data.append({varsearch: idbusca})

                            Success = True
                            Errors.clear()
                
                except:

                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(102)+ " - Erro na segunda tentativa de encontrar a variável"})

        except:

            Success = False
            Errors.append({"msg": ErrorsDict.Get.ByCode(103)})

        finally:

            return json.dumps({"success": Success, "errors": Errors, "data": Data})

    def OpenGetValues(varsearch, typereturn):

        Success  = True
        Errors  = []
        Data    = []

        try:

            variavel        = json.loads(UrlHandling.FindGetVars(varsearch))
            variavelStatus  = list(variavel.values())[0]
            variavelErrors  = list(variavel.values())[1]
            variavelData    = list(variavel.values())[2]

            if variavelStatus:

                for data in variavelData:

                    Data.append({f"{varsearch}": list(data.values())[0]})

            else:

                Success = False

                for error in variavelErrors:

                    Errors.append({"msg": f"{list(error.values())[0]}"})

        except:

            Success = False
            Errors.append({"msg": ErrorsDict.Get.ByCode(111)})

        finally:

            if typereturn == 1:

                return Success, Errors, Data

            else:

                return json.dumps({"success": Success, "errors": Errors, "data": Data})

class Env():

    def DataBase():

        Success  = True
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

                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(201)})

        except:

            Success = False
            Errors.append({"msg": ErrorsDict.Get.ByCode(202)})

        finally:

            return json.dumps({"success": Success, "errors": Errors, "data": Data})

class ConnectDataBase():

    def Connection(WebApi):

        Success  = True
        Errors  = []
        Data    = []

        try:

            dsn                 = json.loads(Env.DataBase())
            connectionStatus    = list(dsn.values())[0]
            connectionErrors    = list(dsn.values())[1]
            connectionData      = list(dsn.values())[2]

            if connectionStatus:
                try:
                    
                    connect = psycopg2.connect(list(list(connectionData)[0].values())[0])
                    WebApi.conn = connect
                    Data.append({"data": f"{connect}"})

                except psycopg2.Error as ex:
                    
                    WebApi.conn = None
                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(301) + " - {0}".format(ex)})

            else:

                Success = False
                
                for error in connectionErrors:

                    Errors.append({"msg": list(error.values())[0]})

        except:

            Success = False

            Errors.append({"msg": ErrorsDict.Get.ByCode(302)})

        finally:

            return json.dumps({"success": Success, "errors": Errors, "data": Data})

    def Status(WebApi):

        Success = True
        Errors = []
        Data = []
        
        try:
            
            if WebApi.conn == None:
                
                try:

                    connection = json.loads(ConnectDataBase.Connection(WebApi))
                    connectionStatus = list(connection.values())[0]
                    connectionErrors = list(connection.values())[1]
                    connectionData = list(connection.values())[2]

                    Success = connectionStatus
                    
                    for error in connectionErrors:
                        
                        Errors.append({"msg": list(error.values())[0]})

                    for data in connectionData:

                        Data.append({"msg": list(data.values())[0]})

                except Exception as ex:

                    Success = False
                    Errors.append({"msg": ex})

        except:

            Success = False
            Errors.append({"msg": ErrorsDict.Get.ByCode(311)})

        finally:

            return json.dumps({"success": Success, "errors": Errors, "data": Data})


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

        self.route("/microservices/web/dispositivo/get/pending", method = "GET", callback = self.DispositivoGetAll)        

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

        self.route("/microservices/web/medicao/tratada", method = "GET", callback = self.MedicaoTratada)

        # Usuario

        self.route("/microservices/web/usuario/login", method = "POST", callback = self.UsuarioLogin)

        self.route("/microservices/web/usuario/register", method = "POST", callback = self.UsuarioRegister)

        # Enfermidade

        self.route("/microservices/web/enfermidade/get/all", method = "GET", callback = self.EnfermidadeGetAll)

        # Estado

        self.route("/microservices/web/estado/get/all", method = "GET", callback = self.EstadoGetAll)
        
        # Cidade

        self.route("/microservices/web/cidade/get/all", method = "GET", callback = self.CidadeGetAll)

        self.route("/microservices/web/cidade/getby/id/estado", method = "GET", callback = self.CidadeGetByIdEstado)

        # Paciente

        self.route("/microservices/web/paciente/get/all", method = "GET", callback = self.PacienteGetAll)

        self.route("/microservices/web/paciente/getby/id", method = "GET", callback = self.PacienteGetById)

        self.route("/microservices/web/paciente/getby/string/name", method = "GET", callback = self.PacienteGetByString)

        self.route("/microservices/web/paciente/getby/string/cpf", method = "GET", callback = self.PacienteGetByString)

        #self.route("/microservices/web/paciente/insert", method = "POST", callback = self.PacienteInsert)

        #self.route("/microservices/web/paciente/update", method = "PUT", callback = self.PacienteUpdate)

        #self.route("/microservices/web/paciente/delete", method = "DELETE", callback = self.PacienteDelete)

        # Alerta

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

        if connectionStatus:

            SQL     = "SELECT * FROM TIPODISPOSITIVO "
            Success  = True
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
                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(401)})

            finally:

                cur.close()

                return json.dumps({"success": Success, "errors": Errors, "data": Data})
        
        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def TipoDispositivoGetById(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success  = True
            Errors  = []
            Data    = []

            try:

                variavelStatus, variavelErrors, variavelData = UrlHandling.OpenGetValues("idbusca", 1)

                if variavelStatus:

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
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(411)})

                        finally:

                            cur.close()

                    elif str(idbusca) == "":

                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(104)})

                    else:

                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(109)})

                else:

                    Success = False

                    for error in variavelErrors:

                        Errors.append({"msg": list(error.values())[0]})
                        
            except:

                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(412)})

            finally:

                return json.dumps({"success": Success, "errors": Errors, "data": Data})
        
        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def TipoDispositivoGetByName(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success  = True
            Errors  = []
            Data    = []

            try:

                variavelStatus, variavelErrors, variavelData = UrlHandling.OpenGetValues("nomebusca", 1)

                if variavelStatus:

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
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(411)})

                        finally:

                            cur.close()

                    else:

                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(104)})
                else:

                    Success = False

                    for error in variavelErrors:

                        Errors.append({"msg": list(error.values())[0]})

            except:

                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(421)})

            finally:

                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def TipoDispositivoInsert(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:        

            Success      = True
            Errors      = []
            Data        = []
            FormData    = request.forms

            try:

                cadastra = FormData.get("cadastra") if "cadastra" in FormData.keys() else None
                cadastra = StringHandling.CleanSqlString(cadastra) if cadastra != None else cadastra

                if cadastra != None and cadastra != "":
                    
                    SQL = "INSERT INTO TIPODISPOSITIVO (NOME, IND_SIT) VALUES " + f" ('{cadastra}', 1) RETURNING *"

                    try:

                        cur = self.conn.cursor()
                        cur.execute(SQL)
                        row_headers = [x[0] for x in cur.description]
                        rv = cur.fetchall()
                        self.conn.commit()

                        for result in rv:

                            Data.append(dict(zip(row_headers, result)))
                            break

                        if not Data:

                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(431)})
                    
                    except:

                        self.conn.rollback()                    
                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(432)})
                    
                    finally:
                    
                        cur.close()
                
                else:
                
                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(110)})
            
            except:
            
                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(433)})
            
            finally:
            
                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def TipoDispositivoUpdate(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success      = True
            Errors      = []
            Data        = []
            FormData    = request.forms

            try:

                idtipo = FormData.get("id") if "id" in FormData.keys() else None

                if not FormData:

                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(105)})

                elif idtipo != None and str(idtipo).isnumeric():

                    request.query.update({'idbusca': f'{idtipo}'})
                    DataBefore          = json.loads(self.TipoDispositivoGetById())
                    DataBeforeStatus    = list(DataBefore.values())[0]
                    DataBeforeErrors    = list(DataBefore.values())[1]
                    DataBeforeData      = list(DataBefore.values())[2]

                    if  DataBeforeStatus and DataBeforeData:

                        columns = 0
                        SQL     = "UPDATE TIPODISPOSITIVO SET "

                        nome = FormData.get("nome") if "nome" in FormData.keys() else None
                        nome = StringHandling.CleanSqlString(nome) if nome != None else nome
                    
                        if nome != None and nome != "":

                            SQL     = StringHandling.AddColumns(columns, SQL)
                            SQL     = SQL + f"NOME = '{nome}'"
                            columns = columns + 1

                        if columns > 0:

                            SQL = SQL + f" WHERE 1 = 1 AND IDTIPO = {idtipo} RETURNING *"
                            
                            try:

                                cur = self.conn.cursor()
                                cur.execute(SQL)
                                row_headers = [x[0] for x in cur.description]
                                rv = cur.fetchall()
                                self.conn.commit()

                                for result in rv:
                                
                                    Data.append(dict(zip(row_headers, result)))
                                    break
                                
                                if not Data:
                                
                                    Success = False
                                    Errors.append({"msg": ErrorsDict.Get.ByCode(441)})
                            
                            except:

                                self.conn.rollback()                            
                                Success = False
                                Errors.append({"msg": ErrorsDict.Get.ByCode(442)})
                            
                            finally:
                            
                                cur.close()
                        
                        else:
                        
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(106)})
                    
                    else:
                    
                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(443)})

                        for error in DataBeforeErrors:

                            Errors.append({"msg": list(error.values())[0]})
                
                else:
                
                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(107)})
            
            except:
            
                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(444)})
            
            finally:
            
                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def TipoDispositivoUpdateName(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success      = True
            Errors      = []
            Data        = []
            FormData    = request.forms

            try:

                idtipo  = FormData.get("id")    if "id"     in FormData.keys()  else None
                nome    = FormData.get("nome")  if "nome"   in FormData.keys()  else None
                nome    = StringHandling.CleanSqlString(nome) if nome != None else nome

                if idtipo != None and str(idtipo).isnumeric():

                    if nome != None and nome != "":

                        SQL = "UPDATE TIPODISPOSITIVO SET NOME = '{}' WHERE IDTIPO = {} RETURNING *".format(
                            nome ,
                            idtipo
                        )
                        request.query.update({'idbusca': f'{idtipo}'})
                        DataBefore          = json.loads(self.TipoDispositivoGetById())
                        DataBeforeStatus    = list(DataBefore.values())[0]
                        DataBeforeErrors    = list(DataBefore.values())[1]
                        DataBeforeData      = list(DataBefore.values())[2]                        

                        if  DataBeforeStatus and DataBeforeData:

                            try:

                                cur = self.conn.cursor()
                                cur.execute(SQL)
                                row_headers = [x[0] for x in cur.description]
                                rv = cur.fetchall()
                                self.conn.commit()

                                for result in rv:

                                    Data.append(dict(zip(row_headers, result)))
                                    break

                                if not Data:

                                    Success = False
                                    Errors.append({"msg": ErrorsDict.Get.ByCode(441)})
                            
                            except:

                                self.conn.rollback()                            
                                Success = False
                                Errors.append({"msg": ErrorsDict.Get.ByCode(442)})
                            
                            finally:
                            
                                cur.close()
                        
                        else:
                        
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(443)})

                            for error in DataBeforeErrors:

                                Errors.append({"msg": list(error.values())[0]})
                    
                    else:
                    
                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(451)})
                
                else:
                
                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(107)})
            
            except:
            
                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(452)})
            
            finally:
            
                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def TipoDispositivoDelete(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success      = True
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

                    if  DataBeforeStatus and DataBeforeData and IndSitPosition != -1:

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

                                        Success = False
                                        Errors.append({"msg": ErrorsDict.Get.ByCode(461)})

                                except:

                                    self.conn.rollback()
                                    Success = False
                                    Errors.append({"msg": ErrorsDict.Get.ByCode(462)})

                                finally:
                                
                                    cur.close()
                            
                            except:

                                self.conn.rollback()                
                                Success = False
                                Errors.append({"msg": ErrorsDict.Get.ByCode(463)})
                            
                            finally:

                                cur.close()
                        
                        else:
                        
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(464)})
                    
                    else:
                    
                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(443)})

                        for error in DataBeforeErrors:

                            Errors.append({"msg": list(error.values())[0]})

                else:

                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(107)})

            except:

                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(465)})

            finally:

                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    #   Dispositivo

    def DispositivoGetAll(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            SQL     = "SELECT * FROM DISPOSITIVO "
            Success  = True
            Errors  = []
            Data    = []

            try:
            
                chamada = request['bottle.route'].rule.replace("/microservices/web/dispositivo/get/", "")

                if chamada == "actives":

                    SQL = SQL + "WHERE IND_SIT = 1 " 

                if chamada == "pending":

                    SQL = SQL + "WHERE IND_SIT = 3 " 

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
                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(501)})
            
            finally:
            
                cur.close()
                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def DispositivoGetById(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success  = True
            Errors  = []
            Data    = []

            try:

                variavelStatus, variavelErrors, variavelData = UrlHandling.OpenGetValues("idbusca", 1)

                if variavelStatus:
                
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

                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(108)})

                            return({"success":Success,"errors":Errors,"data":Data})
                
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
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(501)})
                        
                        finally:
                        
                            cur.close()
                    
                    elif str(idbusca) == "":
                    
                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(104)})
                    
                    else:
                    
                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(109)})
                
                else:
                
                    Success = False
                    msgs = list(list(variavelErrors)[0].values())

                    for msg in msgs:
                    
                        Errors.append({"msg": msg})
            
            except:
            
                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(511)})
            
            finally:
            
                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def DispositivoGetByString(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success  = True
            Errors  = []
            Data    = []

            try:

                variavelStatus, variavelErrors, variavelData = UrlHandling.OpenGetValues("textobusca", 1)

                if variavelStatus:
                
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

                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(108)})

                            return({"success":Success,"errors":Errors,"data":Data})

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
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(521)})
                        
                        finally:
                        
                            cur.close()

                    else:

                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(104)})
                
                else:
                
                    Success = False
                    msgs = list(list(variavelErrors)[0].values())

                    for msg in msgs:
                    
                        Errors.append({"msg": msg})
            
            except:
            
                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(522)})
            
            finally:
            
                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def DispositivoInsert(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:        

            Success      = True
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

                if MandatoryVarsExists:

                    idtipo      = FormData.get("tipo")
                    idambiente  = FormData.get("ambiente")
                    eixox       = FormData.get("eixox")
                    eixoy       = FormData.get("eixoy")
                    
                    MandatoryVarsTypes = True   if  (       str(idtipo).isnumeric() \
                                                        and str(idambiente).isnumeric() \
                                                        and StringHandling.isnumber(eixox) \
                                                        and StringHandling.isnumber(eixoy) \
                                                    ) \
                                                else False

                else:

                    MandatoryVarsTypes = False

                if MandatoryVarsExists and MandatoryVarsTypes:

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
                                "VALUES " + " ('{}', {}, {}, '{}', '{}', {}, {}, '{}', 1) RETURNING *".format(
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
                            row_headers = [x[0] for x in cur.description]
                            rv = cur.fetchall()
                            self.conn.commit()

                            for result in rv:

                                Data.append(dict(zip(row_headers, result)))
                                break

                            if not Data:

                                Success = False
                                Errors.append({"msg": ErrorsDict.Get.ByCode(531)})
                        
                        except:
                            
                            self.conn.rollback()
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(532)})
                        
                        finally:
                        
                            cur.close()
                    
                    except:
                    
                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(533)})

                elif MandatoryVarsExists == False:

                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(112)})

                else: #MandatoryVarsTypes == False

                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(113)})
            
            except:

                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(114)})

            finally:

                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def DispositivoUpdate(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success      = True
            Errors      = []
            Data        = []
            FormData    = request.forms

            try:

                iddispositivo = FormData.get("id") if "id" in FormData.keys() else None

                if not FormData:

                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(105)})

                elif iddispositivo != None and str(iddispositivo).isnumeric():

                    request.query.update({'idbusca': f'{iddispositivo}'})

                    DataBefore          = json.loads(self.DispositivoGetById())
                    DataBeforeStatus    = list(DataBefore.values())[0]
                    DataBeforeErrors    = list(DataBefore.values())[1]
                    DataBeforeData      = list(DataBefore.values())[2]

                    if  DataBeforeStatus and DataBeforeData:

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

                        if      (   str(idtipo).isnumeric()             or idtipo       == None ) \
                            and (   str(idambiente).isnumeric()         or idambiente   == None ) \
                            and (   StringHandling.isnumber(eixox)      or eixox        == None ) \
                            and (   StringHandling.isnumber(eixoy)      or eixoy        == None ):

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

                                SQL = SQL + f" WHERE 1 = 1 AND IDDISPOSITIVO = {iddispositivo} RETURNING *"

                                try:
                                
                                    cur = self.conn.cursor()
                                    cur.execute(SQL)
                                    row_headers = [x[0] for x in cur.description]
                                    rv = cur.fetchall()
                                    self.conn.commit()

                                    for result in rv:
                                    
                                        Data.append(dict(zip(row_headers, result)))
                                        break
                                    
                                    if not Data:
                                    
                                        Success = False
                                        Errors.append({"msg": ErrorsDict.Get.ByCode(541)})
                                
                                except:

                                    self.conn.rollback()                                
                                    Success = False
                                    Errors.append({"msg": ErrorsDict.Get.ByCode(542)})
                                
                                finally:
                                
                                    cur.close()
                            
                            else:
                            
                                Success = False
                                Errors.append({"msg": ErrorsDict.Get.ByCode(106)})

                        else:

                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(115)})
                        
                    else:
                    
                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(543)})
                    
                else:
                
                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(107)})
            
            except:
            
                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(544)})
            
            finally:
            
                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def DispositivoUpdateName(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success      = True
            Errors      = []
            Data        = []
            FormData    = request.forms

            try:

                iddispositivo   = FormData.get("id")    if "id"     in FormData.keys()  else None
                nome            = FormData.get("nome")  if "nome"   in FormData.keys()  else None
                nome            = StringHandling.CleanSqlString(nome) if nome != None else nome

                if iddispositivo != None and str(iddispositivo).isnumeric():

                    if nome != None and nome != "":

                        SQL = "UPDATE DISPOSITIVO SET NOME = '{}' WHERE IDDISPOSITIVO = {} RETURNING *".format(
                            nome ,
                            iddispositivo
                        )
                        request.query.update({'idbusca': f'{iddispositivo}'})
                        DataBefore          = json.loads(self.DispositivoGetById())
                        DataBeforeStatus    = list(DataBefore.values())[0]
                        DataBeforeErrors    = list(DataBefore.values())[1]
                        DataBeforeData      = list(DataBefore.values())[2]                        

                        if  DataBeforeStatus and DataBeforeData:

                            try:

                                cur = self.conn.cursor()
                                cur.execute(SQL)
                                row_headers = [x[0] for x in cur.description]
                                rv = cur.fetchall()
                                self.conn.commit()

                                for result in rv:

                                    Data.append(dict(zip(row_headers, result)))
                                    break

                                if not Data:

                                    Success = False
                                    Errors.append({"msg": ErrorsDict.Get.ByCode(541)})
                            
                            except:

                                self.conn.rollback()                            
                                Success = False
                                Errors.append({"msg": ErrorsDict.Get.ByCode(542)})
                            
                            finally:
                            
                                cur.close()
                        
                        else:
                        
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(543)})

                            for error in DataBeforeErrors:

                                Errors.append({"msg": list(error.values())[0]})
                    
                    else:
                    
                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(551)})
                
                else:
                
                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(107)})
            
            except:
            
                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(552)})
            
            finally:
            
                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def DispositivoUpdateCode(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success      = True
            Errors      = []
            Data        = []
            FormData    = request.forms

            try:

                iddispositivo   = FormData.get("id")        if "id"     in FormData.keys()  else None
                codigo          = FormData.get("codigo")    if "codigo" in FormData.keys()  else None
                codigo          = StringHandling.CleanSqlString(codigo) if codigo != None   else codigo

                if iddispositivo != None and str(iddispositivo).isnumeric():

                    if codigo != None and codigo != "":

                        SQL = "UPDATE DISPOSITIVO SET CODIGODISPOSITIVO = '{}' WHERE IDDISPOSITIVO = {} RETURNING *".format(
                            codigo ,
                            iddispositivo
                        )
                        request.query.update({'idbusca': f'{iddispositivo}'})
                        DataBefore          = json.loads(self.DispositivoGetById())
                        DataBeforeStatus    = list(DataBefore.values())[0]
                        DataBeforeErrors    = list(DataBefore.values())[1]
                        DataBeforeData      = list(DataBefore.values())[2]                        

                        if  DataBeforeStatus and DataBeforeData:

                            try:

                                cur = self.conn.cursor()
                                cur.execute(SQL)
                                row_headers = [x[0] for x in cur.description]
                                rv = cur.fetchall()
                                self.conn.commit()

                                for result in rv:

                                    Data.append(dict(zip(row_headers, result)))
                                    break

                                if not Data:

                                    Success = False
                                    Errors.append({"msg": ErrorsDict.Get.ByCode(541)})
                            
                            except:

                                self.conn.rollback()                            
                                Success = False
                                Errors.append({"msg": ErrorsDict.Get.ByCode(542)})
                            
                            finally:
                            
                                cur.close()
                        
                        else:
                        
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(543)})

                            for error in DataBeforeErrors:

                                Errors.append({"msg": list(error.values())[0]})
                    
                    else:
                    
                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(561)})
                
                else:
                
                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(107)})
            
            except:
            
                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(562)})
            
            finally:
            
                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def DispositivoDelete(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success      = True
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

                    if  DataBeforeStatus and DataBeforeData and IndSitPosition != -1:

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

                                        Success = False
                                        Errors.append({"msg": ErrorsDict.Get.ByCode(571)})

                                except:

                                    self.conn.rollback()
                                    Success = False
                                    Errors.append({"msg": ErrorsDict.Get.ByCode(572)})

                                finally:
                                
                                    cur.close()
                            
                            except:

                                self.conn.rollback()                
                                Success = False
                                Errors.append({"msg": ErrorsDict.Get.ByCode(573)})
                            
                            finally:

                                cur.close()
                        
                        else:
                        
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(574)})
                    
                    else:
                    
                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(543)})

                        for error in DataBeforeErrors:

                            Errors.append({"msg": list(error.values())[0]})

                else:

                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(107)})

            except:

                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(575)})

            finally:

                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    #   Ambiente

    def AmbienteGetAll(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            SQL     = "SELECT * FROM AMBIENTE "
            Success  = True
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
                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(601)})
            
            finally:
            
                cur.close()
                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def AmbienteGetById(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success  = True
            Errors  = []
            Data    = []

            try:

                variavelStatus, variavelErrors, variavelData = UrlHandling.OpenGetValues("idbusca", 1)

                if variavelStatus:
                
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

                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(108)})

                            return({"success":Success,"errors":Errors,"data":Data})
                
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
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(611)})
                        
                        finally:
                        
                            cur.close()
                    
                    elif str(idbusca) == "":
                    
                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(104)})
                    
                    else:
                    
                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(109)})
                
                else:
                
                    Success = False
                    msgs = list(list(variavelErrors)[0].values())

                    for msg in msgs:
                    
                        Errors.append({"msg": msg})
            
            except:
            
                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(612)})
            
            finally:
            
                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def AmbienteGetByString(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success  = True
            Errors  = []
            Data    = []

            try:

                variavelStatus, variavelErrors, variavelData = UrlHandling.OpenGetValues("textobusca", 1)

                if variavelStatus:
                
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

                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(108)})

                            return({"success":Success,"errors":Errors,"data":Data})

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
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(611)})
                        
                        finally:
                        
                            cur.close()

                    else:

                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(104)})
                
                else:
                
                    Success = False
                    msgs = list(list(variavelErrors)[0].values())

                    for msg in msgs:
                    
                        Errors.append({"msg": msg})
            
            except:
            
                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(621)})
            
            finally:
            
                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def AmbienteInsert(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:        

            Success      = True
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

                if MandatoryVarsExists and MandatoryVarsTypes:

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
                                "VALUES " + " ('{}', '{}', 1) RETURNING *".format(
                                    nome ,
                                    descricao
                                )

                        try:

                            cur = self.conn.cursor()
                            cur.execute(SQL)
                            row_headers = [x[0] for x in cur.description]
                            rv = cur.fetchall()
                            self.conn.commit()

                            for result in rv:

                                Data.append(dict(zip(row_headers, result)))
                                break

                            if not Data:

                                Success = False
                                Errors.append({"msg": ErrorsDict.Get.ByCode(631)})
                        
                        except:
                            
                            self.conn.rollback()
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(632)})
                        
                        finally:
                        
                            cur.close()
                    
                    except:
                    
                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(633)})

                elif MandatoryVarsExists == False:

                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(112)})

                else: #MandatoryVarsTypes == False

                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(113)})
            
            except:

                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(114)})

            finally:

                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def AmbienteUpdate(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success      = True
            Errors      = []
            Data        = []
            FormData    = request.forms

            try:

                idambiente = FormData.get("id") if "id" in FormData.keys() else None

                if not FormData:

                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(105)})

                elif idambiente != None and str(idambiente).isnumeric():

                    request.query.update({'idbusca': f'{idambiente}'})

                    DataBefore          = json.loads(self.AmbienteGetById())
                    DataBeforeStatus    = list(DataBefore.values())[0]
                    DataBeforeErrors    = list(DataBefore.values())[1]
                    DataBeforeData      = list(DataBefore.values())[2]

                    if  DataBeforeStatus and DataBeforeData:

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

                            SQL = SQL + f" WHERE 1 = 1 AND IDAMBIENTE = {idambiente} RETURNING *"

                            try:
                        
                                cur = self.conn.cursor()
                                cur.execute(SQL)
                                row_headers = [x[0] for x in cur.description]
                                rv = cur.fetchall()
                                self.conn.commit()

                                for result in rv:
                                
                                    Data.append(dict(zip(row_headers, result)))
                                    break
                                
                                if not Data:
                                
                                    Success = False
                                    Errors.append({"msg": ErrorsDict.Get.ByCode(641)})
                            
                            except:

                                self.conn.rollback()                                
                                Success = False
                                Errors.append({"msg": ErrorsDict.Get.ByCode(642)})
                            
                            finally:
                            
                                cur.close()
                        
                        else:
                        
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(106)})
                    
                    else:
                    
                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(644)})
                    
                else:
                
                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(107)})
            
            except:
            
                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(645)})
            
            finally:
            
                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def AmbienteUpdateName(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success      = True
            Errors      = []
            Data        = []
            FormData    = request.forms

            try:

                idambiente      = FormData.get("id")    if "id"     in FormData.keys()  else None
                nome            = FormData.get("nome")  if "nome"   in FormData.keys()  else None
                nome            = StringHandling.CleanSqlString(nome) if nome != None else nome

                if idambiente != None and str(idambiente).isnumeric():

                    if nome != None and nome != "":

                        SQL = "UPDATE AMBIENTE SET NOME = '{}' WHERE IDAMBIENTE = {} RETURNING *".format(
                            nome ,
                            idambiente
                        )
                        request.query.update({'idbusca': f'{idambiente}'})
                        DataBefore          = json.loads(self.AmbienteGetById())
                        DataBeforeStatus    = list(DataBefore.values())[0]
                        DataBeforeErrors    = list(DataBefore.values())[1]
                        DataBeforeData      = list(DataBefore.values())[2]

                        if  DataBeforeStatus and DataBeforeData:

                            try:

                                cur = self.conn.cursor()
                                cur.execute(SQL)
                                row_headers = [x[0] for x in cur.description]
                                rv = cur.fetchall()
                                self.conn.commit()

                                for result in rv:

                                    Data.append(dict(zip(row_headers, result)))
                                    break

                                if not Data:

                                    Success = False
                                    Errors.append({"msg": ErrorsDict.Get.ByCode(541)})
                            
                            except:

                                self.conn.rollback()                            
                                Success = False
                                Errors.append({"msg": ErrorsDict.Get.ByCode(642)})
                            
                            finally:
                            
                                cur.close()
                        
                        else:
                        
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(644)})

                            for error in DataBeforeErrors:

                                Errors.append({"msg": list(error.values())[0]})
                    
                    else:
                    
                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(651)})
                
                else:
                
                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(107)})
            
            except:
            
                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(652)})
            
            finally:
            
                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def AmbienteUpdateDescription(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success      = True
            Errors      = []
            Data        = []
            FormData    = request.forms

            try:

                idambiente  = FormData.get("id")            if "id"         in FormData.keys()  else None
                descricao   = FormData.get("descricao")     if "descricao"  in FormData.keys()  else None
                descricao   = StringHandling.CleanSqlString(descricao) if descricao != None else descricao

                if idambiente != None and str(idambiente).isnumeric():

                    if descricao != None and descricao != "":

                        SQL = "UPDATE AMBIENTE SET DESCRICAO = '{}' WHERE IDAMBIENTE = {} RETURNING *".format(
                            descricao ,
                            idambiente
                        )
                        request.query.update({'idbusca': f'{idambiente}'})
                        DataBefore          = json.loads(self.AmbienteGetById())
                        DataBeforeStatus    = list(DataBefore.values())[0]
                        DataBeforeErrors    = list(DataBefore.values())[1]
                        DataBeforeData      = list(DataBefore.values())[2]

                        if  DataBeforeStatus and DataBeforeData:

                            try:

                                cur = self.conn.cursor()
                                cur.execute(SQL)
                                row_headers = [x[0] for x in cur.description]
                                rv = cur.fetchall()
                                self.conn.commit()

                                for result in rv:

                                    Data.append(dict(zip(row_headers, result)))
                                    break

                                if not Data:

                                    Success = False
                                    Errors.append({"msg": ErrorsDict.Get.ByCode(641)})
                            
                            except:

                                self.conn.rollback()                            
                                Success = False
                                Errors.append({"msg": ErrorsDict.Get.ByCode(661)})
                            
                            finally:
                            
                                cur.close()
                        
                        else:
                        
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(644)})

                            for error in DataBeforeErrors:

                                Errors.append({"msg": list(error.values())[0]})
                    
                    else:
                    
                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(662)})
                
                else:
                
                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(107)})
            
            except:
            
                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(663)})
            
            finally:
            
                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def AmbienteDelete(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success      = True
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

                    if  DataBeforeStatus and DataBeforeData and IndSitPosition != -1:

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

                                        Success = False
                                        Errors.append({"msg": ErrorsDict.Get.ByCode(671)})

                                except:

                                    self.conn.rollback()
                                    Success = False
                                    Errors.append({"msg": ErrorsDict.Get.ByCode(672)})

                                finally:
                                
                                    cur.close()
                            
                            except:

                                self.conn.rollback()                
                                Success = False
                                Errors.append({"msg": ErrorsDict.Get.ByCode(673)})
                            
                            finally:

                                cur.close()
                        
                        else:
                        
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(674)})
                    
                    else:
                    
                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(644)})

                        for error in DataBeforeErrors:

                            Errors.append({"msg": list(error.values())[0]})

                else:

                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(107)})

            except:

                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(675)})

            finally:

                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    #   Medição

    def MedicaoTratada(self):

        Success = True
        Errors  = []
        Data    = []

        try:

            DataInicioStatus, DataInicioErrors, DataInicioData = UrlHandling.OpenGetValues("datainicio", 1)

            DataFimStatus, DataFimErrors, DataFimData = UrlHandling.OpenGetValues("datafim", 1)

            if DataInicioStatus and DataFimStatus:

                DataInicioBusca = list(list(DataInicioData)[0].values())[0]

                DataFimBusca = list(list(DataFimData)[0].values())[0]

                if StringHandling.isdatetime(DataInicioBusca) and StringHandling.isdatetime(DataFimBusca):

                    request = requests.get(f"http://172.21.0.6:8083/medicao/tratada/{DataInicioBusca}/{DataFimBusca}")
                    
                    Medicao = request.json()

                    Medicao = Medicao["data"]

                    Data = Medicao

                else:

                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(701)})

            else:

                Success = False
                Errors.append({"msg": DataInicioErrors})
                Errors.append({"msg": DataFimErrors})

        except:

            Success = False
            Errors.append({"msg": ErrorsDict.Get.ByCode(702)})
            

        finally:

            return json.dumps({"success": Success, "errors": Errors, "data": Data})

    #   Usuario

    def UsuarioLogin(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:        

            Success      = True
            Errors      = []
            Data        = []
            FormData    = request.forms

            try:

                MandatoryVars = ["email", "password"]

                MandatoryVarsExists = True

                for var in MandatoryVars:

                    if var not in FormData.keys():

                        MandatoryVarsExists = False

                MandatoryVarsTypes = True if MandatoryVarsExists else False

                if MandatoryVarsExists and MandatoryVarsTypes:

                    try:
                        
                        email       = FormData.get("email")
                        password    = FormData.get("password")

                        email       = StringHandling.CleanSqlString(email)      if email    != None     else email
                        password    = StringHandling.CleanSqlString(password)   if password != None     else password
                            
                        SQL = f"    SELECT \
                                        NOME AS NAME , \
                                        EMAIL \
                                    FROM    USUARIO \
                                    WHERE   1 = 1 \
                                        AND UPPER(EMAIL) = UPPER('{email}') \
                                        AND UPPER(SENHA) = UPPER('{password}') "

                        try:

                            cur = self.conn.cursor()
                            cur.execute(SQL)
                            row_headers = [x[0] for x in cur.description]
                            rv = cur.fetchall()
                            self.conn.commit()

                            for result in rv:

                                Data.append(dict(zip(row_headers, result)))
                                break

                            if not Data:

                                Success = False
                                Errors.append({"msg": ErrorsDict.Get.ByCode(801)})
                        
                        except:
                            
                            self.conn.rollback()
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(802)})
                        
                        finally:
                        
                            cur.close()
                    
                    except:
                    
                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(803)})

                elif MandatoryVarsExists == False:

                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(112)})

                else: #MandatoryVarsTypes == False

                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(113)})
            
            except:

                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(114)})

            finally:

                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def UsuarioRegister(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:        

            Success      = True
            Errors      = []
            Data        = []
            FormData    = request.forms

            try:

                MandatoryVars = ["username", "email", "password", "passwordconfirmation"]

                MandatoryVarsExists = True

                for var in MandatoryVars:

                    if var not in FormData.keys():

                        MandatoryVarsExists = False

                MandatoryVarsTypes = True if MandatoryVarsExists else False

                if MandatoryVarsExists and MandatoryVarsTypes:

                    try:
                        
                        username = FormData.get("username")
                        email = FormData.get("email")
                        password = FormData.get("password")
                        passwordconfirmation = FormData.get("passwordconfirmation")

                        username                = StringHandling.CleanSqlString(username)   if username != None     else username
                        email                   = StringHandling.CleanSqlString(email)      if email    != None     else email
                        password                = StringHandling.CleanSqlString(password)   if password != None     else password
                        passwordconfirmation    = StringHandling.CleanSqlString(passwordconfirmation) \
                                                  if passwordconfirmation != None     else passwordconfirmation

                        if len(password) >= 6 and password == passwordconfirmation:
                            
                            SQL = " INSERT INTO USUARIO (" + \
                                                                "NOME , " + \
                                                                "EMAIL , " + \
                                                                "SENHA , " + \
                                                                "IND_SIT" + \
                                                            ")" + \
                                    "VALUES " + " ('{}', '{}', '{}', 1) RETURNING EMAIL".format(
                                        username,
                                        email,
                                        password
                                    )

                            try:

                                cur = self.conn.cursor()
                                cur.execute(SQL)
                                row_headers = [x[0] for x in cur.description]
                                rv = cur.fetchall()
                                self.conn.commit()

                                for result in rv:

                                    Data.append(dict(zip(row_headers, result)))
                                    break

                                if not Data:

                                    Success = False
                                    Errors.append({"msg": ErrorsDict.Get.ByCode(811)})
                            
                            except psycopg2.Error as ex:

                                psycopgError = ""

                                if ex.pgcode == "23505": #CODIGO 23505 == UniqueViolation

                                    psycopgError = " - Email já cadastrado!"
                                
                                self.conn.rollback()
                                Success = False
                                Errors.append({"msg": ErrorsDict.Get.ByCode(812) + psycopgError})

                            except:
    
                                self.conn.rollback()
                                Success = False
                                Errors.append({"msg": ErrorsDict.Get.ByCode(812)})
                            
                            finally:
                            
                                cur.close()
                        else:
                            
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(813)})
                    
                    except:
                    
                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(814)})

                elif MandatoryVarsExists == False:

                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(112)})

                else: #MandatoryVarsTypes == False

                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(113)})
            
            except:

                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(114)})

            finally:

                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    #   Estado
    
    def EstadoGetAll(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            SQL     = "SELECT * FROM ESTADO "
            Success  = True
            Errors  = []
            Data    = []

            try:

                SQL = SQL + "ORDER BY IDESTADO"

                cur = self.conn.cursor()
                cur.execute(SQL)
                row_headers = [x[0] for x in cur.description]
                rv = cur.fetchall()
                self.conn.commit()

                for result in rv:

                    Data.append(dict(zip(row_headers, result)))

            except:

                self.conn.rollback()
                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(601)})
            
            finally:
            
                cur.close()
                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})            

    #   Cidade

    def CidadeGetAll(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            SQL     = "SELECT * FROM CIDADE "
            Success  = True
            Errors  = []
            Data    = []

            try:

                SQL = SQL + "ORDER BY IDCIDADE"

                cur = self.conn.cursor()
                cur.execute(SQL)
                row_headers = [x[0] for x in cur.description]
                rv = cur.fetchall()
                self.conn.commit()

                for result in rv:

                    Data.append(dict(zip(row_headers, result)))

            except:

                self.conn.rollback()
                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(401)})

            finally:

                cur.close()

                return json.dumps({"success": Success, "errors": Errors, "data": Data})
        
        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def CidadeGetByIdEstado(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success  = True
            Errors  = []
            Data    = []

            try:

                variavelStatus, variavelErrors, variavelData = UrlHandling.OpenGetValues("idbusca", 1)

                if variavelStatus:

                    idbusca = list(list(variavelData)[0].values())[0]

                    if(str(idbusca).isnumeric()):

                        SQL = f"SELECT * FROM CIDADE WHERE 1 = 1 AND IDESTADO = {idbusca} ORDER BY NOME ASC"

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
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(411)})

                        finally:

                            cur.close()

                    elif str(idbusca) == "":

                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(104)})

                    else:

                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(109)})

                else:

                    Success = False

                    for error in variavelErrors:

                        Errors.append({"msg": list(error.values())[0]})
                        
            except:

                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(412)})

            finally:

                return json.dumps({"success": Success, "errors": Errors, "data": Data})
        
        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    #   Enfermidade

    def EnfermidadeGetAll(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            SQL     = "SELECT * FROM ENFERMIDADE "
            Success  = True
            Errors  = []
            Data    = []

            try:

                SQL = SQL + "ORDER BY IDENFERMIDADE"

                cur = self.conn.cursor()
                cur.execute(SQL)
                row_headers = [x[0] for x in cur.description]
                rv = cur.fetchall()
                self.conn.commit()

                for result in rv:

                    Data.append(dict(zip(row_headers, result)))

            except:

                self.conn.rollback()
                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(401)})

            finally:

                cur.close()

                return json.dumps({"success": Success, "errors": Errors, "data": Data})
        
        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    #   Paciente
    
    def PacienteGetAll(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            SQL     = "SELECT * FROM PACIENTE "

            Success = True
            Errors  = []
            Data    = []

            try:

                SQL = SQL + "ORDER BY IDPACIENTE"

                cur = self.conn.cursor()
                cur.execute(SQL)
                row_headers = [x[0] for x in cur.description]
                rv = cur.fetchall()
                self.conn.commit()

                for result in rv:

                    result = ListHandling.MapDate.ToString(result)

                    Data.append(dict(zip(row_headers, result)))

            except:

                self.conn.rollback()
                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(401)})

            finally:

                cur.close()

                return json.dumps({"success": Success, "errors": Errors, "data": Data})
        
        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def PacienteGetById(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success = True
            Errors  = []
            Data    = []

            try:

                variavelStatus, variavelErrors, variavelData = UrlHandling.OpenGetValues("idbusca", 1)

                if variavelStatus:

                    idbusca = list(list(variavelData)[0].values())[0]

                    if(str(idbusca).isnumeric()):

                        SQL = f"SELECT * FROM PACIENTE WHERE 1 = 1 AND IDPACIENTE = {idbusca} ORDER BY IDPACIENTE"

                        try:

                            cur = self.conn.cursor()
                            cur.execute(SQL)
                            row_headers = [x[0] for x in cur.description]
                            rv = cur.fetchall()
                            self.conn.commit()

                            for result in rv:

                                result = ListHandling.MapDate.ToString(result)

                                Data.append(dict(zip(row_headers, result)))
                                break

                        except:

                            self.conn.rollback()
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(411)})

                        finally:

                            cur.close()

                    elif str(idbusca) == "":

                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(104)})

                    else:

                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(109)})

                else:

                    Success = False

                    for error in variavelErrors:

                        Errors.append({"msg": list(error.values())[0]})
                        
            except:

                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(412)})

            finally:

                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

    def PacienteGetByString(self):

        connection          = json.loads(ConnectDataBase.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success = True
            Errors  = []
            Data    = []

            try:

                variavelStatus, variavelErrors, variavelData = UrlHandling.OpenGetValues("textobusca", 1)

                if variavelStatus:
                
                    textobusca = list(list(variavelData)[0].values())[0]
                    textobusca = StringHandling.CleanSqlString(textobusca) if textobusca != None else textobusca

                    if textobusca != "":
                
                        SQL = "SELECT * FROM PACIENTE WHERE 1 = 1 "

                        route = "/microservices/web/paciente/getby/string"
                        chamada = request['bottle.route'].rule.replace(route + "/", "")

                        if chamada == "name":

                            SQL = SQL + f"AND UPPER(NOME) LIKE '%{str(textobusca).upper()}%' "

                        elif chamada == "cpf":

                            SQL = SQL + f"AND CPF LIKE '{str(textobusca).upper()}' "

                        else:

                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(108)})

                            return({"success":Success,"errors":Errors,"data":Data})

                        try:

                            SQL = SQL + "ORDER BY IDPACIENTE"
                    
                            cur = self.conn.cursor()
                            cur.execute(SQL)
                            row_headers = [x[0] for x in cur.description]
                            rv = cur.fetchall()
                            self.conn.commit()

                            for result in rv:

                                result = ListHandling.MapDate.ToString(result)

                                Data.append(dict(zip(row_headers, result)))

                        except:
            
                            self.conn.rollback()                            
                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(611)})
                        
                        finally:
                        
                            cur.close()

                    else:

                        Success = False
                        Errors.append({"msg": ErrorsDict.Get.ByCode(104)})
                
                else:
                
                    Success = False
                    msgs = list(list(variavelErrors)[0].values())

                    for msg in msgs:
                    
                        Errors.append({"msg": msg})
            
            except:
            
                Success = False
                Errors.append({"msg": ErrorsDict.Get.ByCode(621)})
            
            finally:
            
                return json.dumps({"success": Success, "errors": Errors, "data": Data})

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData})

if __name__ == '__main__':

    webapi = WebApi()
    webapi.run(host='0.0.0.0', port=8081, debug=True)
