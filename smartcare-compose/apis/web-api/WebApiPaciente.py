from bottle import request
import ConnectDataBase
import ErrorsDict
import json
import ListHandling
import StringHandling
import UrlHandling

class route:

    def GetAll(self):

        connection          = json.loads(ConnectDataBase.Get.Status(self))
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

            Success = True
            Errors  = []
            Data    = []

            try:

                variavelStatus, variavelErrors, variavelData = UrlHandling.Do.OpenGetValues("idbusca", 1)

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

                return json.dumps({"success": Success, "errors": Errors, "data": Data},sort_keys=True, indent=4, ensure_ascii=False)

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData},sort_keys=True, indent=4, ensure_ascii=False)

    def GetByString(self):

        connection          = json.loads(ConnectDataBase.Get.Status(self))
        connectionStatus    = list(connection.values())[0]
        connectionErrors    = list(connection.values())[1]
        connectionData      = list(connection.values())[2]

        if connectionStatus:

            Success = True
            Errors  = []
            Data    = []

            try:

                variavelStatus, variavelErrors, variavelData = UrlHandling.Do.OpenGetValues("textobusca", 1)

                if variavelStatus:
                
                    textobusca = list(list(variavelData)[0].values())[0]
                    textobusca = StringHandling.Do.CleanSqlString(textobusca) if textobusca != None else textobusca

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

                MandatoryVars = ["cpf", "nome", "nascimento", "enfermidade", "estagio_enfermidade"]

                MandatoryVarsExists = True

                for var in MandatoryVars:

                    if var not in FormData.keys():

                        MandatoryVarsExists = False

                MandatoryVarsTypes = True

                if MandatoryVarsExists:

                    cpf                 = FormData.get("cpf")
                    nome                = FormData.get("nome")
                    nascimento          = FormData.get("nascimento")
                    idenfermidade       = FormData.get("enfermidade")
                    estagio_enfermidade = FormData.get("estagio_enfermidade")
                    #Variaveis sem obrigatoriedade no request, mas se vier tem que ser de um tipo
                    idestado            = FormData.get("estado") if "estado" in FormData.keys() else 1 
                    idcidade            = FormData.get("cidade") if "cidade" in FormData.keys() else 1
                    
                    MandatoryVarsTypes = True   if  (           str(idenfermidade).isnumeric() \
                                                            and StringHandling.Is.datetime(nascimento) \
                                                            and str(idestado).isnumeric() \
                                                            and str(idestado).isnumeric() \
                                                    ) \
                                                else False

                else:

                    MandatoryVarsTypes = False

                if MandatoryVarsExists and MandatoryVarsTypes:

                    try:
                        
                        cpf                 = FormData.get("cpf")
                        nome                = FormData.get("nome")
                        nascimento          = FormData.get("nascimento")
                        idenfermidade       = FormData.get("enfermidade")
                        estagio_enfermidade = FormData.get("estagio_enfermidade")
                        idestado            = FormData.get("estado") if "estado" in FormData.keys() else 1 
                        idcidade            = FormData.get("cidade") if "cidade" in FormData.keys() else 1
                        bairro              = FormData.get("bairro") if "bairro" in FormData.keys() else ""
                        endereco            = FormData.get("endereco") if "endereco" in FormData.keys() else ""
                        complemento         = FormData.get("complemento") if "complemento" in FormData.keys() else ""

                        cpf                 = StringHandling.Do.CleanSqlString(cpf)
                        nome                = StringHandling.Do.CleanSqlString(nome)
                        nascimento          = StringHandling.Do.CleanSqlString(nascimento)
                        idenfermidade       = StringHandling.Do.CleanSqlString(idenfermidade)
                        estagio_enfermidade = StringHandling.Do.CleanSqlString(estagio_enfermidade)
                        bairro              = StringHandling.Do.CleanSqlString(bairro)
                        endereco            = StringHandling.Do.CleanSqlString(endereco)
                        complemento         = StringHandling.Do.CleanSqlString(complemento)

                        SQL = " INSERT INTO PACIENTE (" + \
                                                            "CPF , " + \
                                                            "NOME , " + \
                                                            "NASCIMENTO , " + \
                                                            "IDENFERMIDADE , " + \
                                                            "ESTAGIO_ENFERMIDADE , " + \
                                                            "IDESTADO , " + \
                                                            "IDCIDADE , " + \
                                                            "BAIRRO , " + \
                                                            "ENDERECO , " + \
                                                            "COMPLEMENTO , " + \
                                                            "BIT_ALERTA , " + \
                                                            "IND_SIT" + \
                                                        ")" + \
                                "VALUES " + " ('{}', '{}', '{}', {}, '{}', {}, {}, '{}','{}','{}', {}, 1) RETURNING *".format(
                                    cpf ,
                                    nome ,
                                    nascimento ,
                                    idenfermidade ,
                                    estagio_enfermidade ,
                                    idestado ,
                                    idcidade ,
                                    bairro ,
                                    endereco ,
                                    complemento ,
                                    False
                                )

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

                return json.dumps({"success": Success, "errors": Errors, "data": Data},sort_keys=True, indent=4, ensure_ascii=False)

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData},sort_keys=True, indent=4, ensure_ascii=False)

    #def Update(self):

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

                idpaciente = FormData.get("id") if "id" in FormData.keys() else None

                if idpaciente != None and str(idpaciente).isnumeric():

                    request.query.update({'idbusca': f'{idpaciente}'})
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

                            SQL = f"UPDATE PACIENTE SET IND_SIT = 2 WHERE IDPACIENTE = {idpaciente}"

                            try:

                                cur = self.conn.cursor()
                                cur.execute(SQL)
                                self.conn.commit()

                                try:

                                    SQL =  f"SELECT 1 FROM PACIENTE " + \
                                           f"WHERE IDPACIENTE = {idpaciente} AND IND_SIT <> 2 " + \
                                            "ORDER BY IDPACIENTE"

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

                return json.dumps({"success": Success, "errors": Errors, "data": Data},sort_keys=True, indent=4, ensure_ascii=False)

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData},sort_keys=True, indent=4, ensure_ascii=False)        