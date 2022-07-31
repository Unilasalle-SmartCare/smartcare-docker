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

    def GetByString(self):

        connection          = json.loads(ConnectDataBase.Get.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success  = True
            Errors  = []
            Data    = []

            try:

                variavelStatus, variavelErrors, variavelData = UrlHandling.Do.OpenGetValues("textobusca", 1)

                if variavelStatus:
                
                    textobusca = list(list(variavelData)[0].values())[0]
                    textobusca = StringHandling.Do.CleanSqlString(textobusca) if textobusca != None else textobusca

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
                                                        and StringHandling.Is.number(eixox) \
                                                        and StringHandling.Is.number(eixoy) \
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

                        codigodispositivo   = StringHandling.Do.CleanSqlString(codigodispositivo)
                        nome                = StringHandling.Do.CleanSqlString(nome)
                        descricao           = StringHandling.Do.CleanSqlString(descricao)
                        orientacao          = StringHandling.Do.CleanSqlString(orientacao)
                            
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

                iddispositivo = FormData.get("id") if "id" in FormData.keys() else None

                if not FormData:

                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(105)})

                elif iddispositivo != None and str(iddispositivo).isnumeric():

                    request.query.update({'idbusca': f'{iddispositivo}'})

                    DataBefore          = json.loads(route.GetById(self))
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

                        codigodispositivo   =   StringHandling.Do.CleanSqlString(codigodispositivo) \
                                                if codigodispositivo != None else codigodispositivo
                        nome                =   StringHandling.Do.CleanSqlString(nome) \
                                                if nome != None else nome
                        descricao           =   StringHandling.Do.CleanSqlString(descricao) \
                                                if descricao != None else descricao
                        orientacao          =   StringHandling.Do.CleanSqlString(orientacao) \
                                                if orientacao != None else orientacao

                        if      (   str(idtipo).isnumeric()             or idtipo       == None ) \
                            and (   str(idambiente).isnumeric()         or idambiente   == None ) \
                            and (   StringHandling.Is.number(eixox)      or eixox        == None ) \
                            and (   StringHandling.Is.number(eixoy)      or eixoy        == None ):

                            columns = 0
                            SQL     = "UPDATE DISPOSITIVO SET "

                            if codigodispositivo != None:

                                SQL     = StringHandling.Do.AddColumns(columns, SQL)
                                SQL     = SQL + f"CODIGODISPOSITIVO = '{codigodispositivo}'"
                                columns = columns + 1

                            if idtipo != None:

                                SQL     = StringHandling.Do.AddColumns(columns, SQL)
                                SQL     = SQL + f"IDTIPO = '{idtipo}'"
                                columns = columns + 1

                            if idambiente != None:

                                SQL     = StringHandling.Do.AddColumns(columns, SQL)
                                SQL     = SQL + f"IDAMBIENTE = '{idambiente}'"
                                columns = columns + 1

                            if nome != None:

                                SQL     = StringHandling.Do.AddColumns(columns, SQL)
                                SQL     = SQL + f"NOME = '{nome}'"
                                columns = columns + 1

                            if descricao != None:

                                SQL     = StringHandling.Do.AddColumns(columns, SQL)
                                SQL     = SQL + f"DESCRICAO = '{descricao}'"
                                columns = columns + 1

                            if eixox != None:

                                SQL     = StringHandling.Do.AddColumns(columns, SQL)
                                SQL     = SQL + f"EIXO_X = '{eixox}'"
                                columns = columns + 1

                            if eixoy != None:

                                SQL     = StringHandling.Do.AddColumns(columns, SQL)
                                SQL     = SQL + f"EIXO_Y = '{eixoy}'"
                                columns = columns + 1

                            if orientacao != None:

                                SQL     = StringHandling.Do.AddColumns(columns, SQL)
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

                iddispositivo   = FormData.get("id")    if "id"     in FormData.keys()  else None
                nome            = FormData.get("nome")  if "nome"   in FormData.keys()  else None
                nome            = StringHandling.Do.CleanSqlString(nome) if nome != None else nome

                if iddispositivo != None and str(iddispositivo).isnumeric():

                    if nome != None and nome != "":

                        SQL = "UPDATE DISPOSITIVO SET NOME = '{}' WHERE IDDISPOSITIVO = {} RETURNING *".format(
                            nome ,
                            iddispositivo
                        )
                        request.query.update({'idbusca': f'{iddispositivo}'})
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

    def UpdateCode(self):

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

                iddispositivo   = FormData.get("id")        if "id"     in FormData.keys()  else None
                codigo          = FormData.get("codigo")    if "codigo" in FormData.keys()  else None
                codigo          = StringHandling.Do.CleanSqlString(codigo) if codigo != None   else codigo

                if iddispositivo != None and str(iddispositivo).isnumeric():

                    if codigo != None and codigo != "":

                        SQL = "UPDATE DISPOSITIVO SET CODIGODISPOSITIVO = '{}' WHERE IDDISPOSITIVO = {} RETURNING *".format(
                            codigo ,
                            iddispositivo
                        )
                        request.query.update({'idbusca': f'{iddispositivo}'})
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

                iddispositivo = FormData.get("id") if "id" in FormData.keys() else None

                if iddispositivo != None and str(iddispositivo).isnumeric():

                    request.query.update({'idbusca': f'{iddispositivo}'})
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

