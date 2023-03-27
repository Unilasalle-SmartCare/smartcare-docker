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
                Errors.append({"msg": ErrorsDict.Get.ByCode(901)})
            
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

                        SQL = f"SELECT * FROM ESTADO WHERE 1 = 1 AND IDESTADO = {idbusca}"

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
                            Errors.append({"msg": ErrorsDict.Get.ByCode(911)})

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
                Errors.append({"msg": ErrorsDict.Get.ByCode(911)})

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

            Success  = True
            Errors  = []
            Data    = []

            try:

                variavelStatus, variavelErrors, variavelData = UrlHandling.Do.OpenGetValues("textobusca", 1)

                if variavelStatus:
                
                    textobusca = list(list(variavelData)[0].values())[0]
                    textobusca = StringHandling.Do.CleanSqlString(textobusca) if textobusca != None else textobusca

                    if textobusca != "":
                
                        SQL = "SELECT * FROM ESTADO WHERE 1 = 1 "

                        route = "/microservices/web/estado/getby/string"
                        chamada = request['bottle.route'].rule.replace(route + "/", "")

                        if chamada == "name":

                            SQL = SQL + f"AND NOME LIKE '%{str(textobusca)}%'"

                        elif chamada == "uf":

                            SQL = SQL + f"AND UF LIKE '%{str(textobusca)}%'"

                        else:

                            Success = False
                            Errors.append({"msg": ErrorsDict.Get.ByCode(108)})

                            return({"success":Success,"errors":Errors,"data":Data})

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
                            Errors.append({"msg": ErrorsDict.Get.ByCode(921)})
                        
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
                Errors.append({"msg": ErrorsDict.Get.ByCode(922)})
            
            finally:
            
                return json.dumps({"success": Success, "errors": Errors, "data": Data},sort_keys=True, indent=4, ensure_ascii=False)

        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData},sort_keys=True, indent=4, ensure_ascii=False)
