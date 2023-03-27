from bottle import request
import ConnectDataBase
import ErrorsDict
import json
import StringHandling
import UrlHandling

class route:

    def GetAll(self):

        connection          = json.loads(ConnectDataBase.Get.Status(self))
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

                return json.dumps({"success": Success, "errors": Errors, "data": Data},sort_keys=True, indent=4, ensure_ascii=False)
        
        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData},sort_keys=True, indent=4, ensure_ascii=False)

    def GetById(self):

        connection          = json.loads(ConnectDataBase.Get.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success  = True
            Errors  = []
            Data    = []

            try:

                variavelStatus, variavelErrors, variavelData = UrlHandling.Do.OpenGetValues("idbusca", 1)

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

                return json.dumps({"success": Success, "errors": Errors, "data": Data},sort_keys=True, indent=4, ensure_ascii=False)
        
        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData},sort_keys=True, indent=4, ensure_ascii=False)

    def GetByName(self):
        
        connection          = json.loads(ConnectDataBase.Get.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success  = True
            Errors  = []
            Data    = []

            try:

                variavelStatus, variavelErrors, variavelData = UrlHandling.Do.OpenGetValues("nomebusca", 1)

                if variavelStatus:

                    nomebusca = list(list(variavelData)[0].values())[0]
                    nomebusca = StringHandling.Do.CleanSqlString(nomebusca)

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

                return json.dumps({"success": Success, "errors": Errors, "data": Data},sort_keys=True, indent=4, ensure_ascii=False)

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData},sort_keys=True, indent=4, ensure_ascii=False)

    def Insert(self):

        connection          = json.loads(ConnectDataBase.Get.Status(self))
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
                cadastra = StringHandling.Do.CleanSqlString(cadastra) if cadastra != None else cadastra

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
            
                return json.dumps({"success": Success, "errors": Errors, "data": Data},sort_keys=True, indent=4, ensure_ascii=False)

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData},sort_keys=True, indent=4, ensure_ascii=False)

    def Update(self):

        connection          = json.loads(ConnectDataBase.Get.Status(self))
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
                    DataBefore          = json.loads(route.GetById(self))
                    DataBeforeStatus    = list(DataBefore.values())[0]
                    DataBeforeErrors    = list(DataBefore.values())[1]
                    DataBeforeData      = list(DataBefore.values())[2]

                    if  DataBeforeStatus and DataBeforeData:

                        columns = 0
                        SQL     = "UPDATE TIPODISPOSITIVO SET "

                        nome = FormData.get("nome") if "nome" in FormData.keys() else None
                        nome = StringHandling.Do.CleanSqlString(nome) if nome != None else nome
                    
                        if nome != None and nome != "":

                            SQL     = StringHandling.Do.AddColumns(columns, SQL)
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
            
                return json.dumps({"success": Success, "errors": Errors, "data": Data},sort_keys=True, indent=4, ensure_ascii=False)

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData},sort_keys=True, indent=4, ensure_ascii=False)

    def UpdateName(self):

        connection          = json.loads(ConnectDataBase.Get.Status(self))
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
                nome    = StringHandling.Do.CleanSqlString(nome) if nome != None else nome

                if idtipo != None and str(idtipo).isnumeric():

                    if nome != None and nome != "":

                        SQL = "UPDATE TIPODISPOSITIVO SET NOME = '{}' WHERE IDTIPO = {} RETURNING *".format(
                            nome ,
                            idtipo
                        )
                        request.query.update({'idbusca': f'{idtipo}'})
                        DataBefore          = json.loads(route.GetById(self))
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
            
                return json.dumps({"success": Success, "errors": Errors, "data": Data},sort_keys=True, indent=4, ensure_ascii=False)

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData},sort_keys=True, indent=4, ensure_ascii=False)

    def Delete(self):

        connection          = json.loads(ConnectDataBase.Get.Status(self))
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
                    DataBefore          = json.loads(route.GetById(self))
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

                return json.dumps({"success": Success, "errors": Errors, "data": Data},sort_keys=True, indent=4, ensure_ascii=False)

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData},sort_keys=True, indent=4, ensure_ascii=False)

