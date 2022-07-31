from bottle import request
import ConnectDataBase
import ErrorsDict
import json
import psycopg2
import StringHandling

class route:

    def GetUsuarioLogin(self):

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

                        email       = StringHandling.Do.CleanSqlString(email)      if email    != None     else email
                        password    = StringHandling.Do.CleanSqlString(password)   if password != None     else password
                            
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

                        username                = StringHandling.Do.CleanSqlString(username)   if username != None     else username
                        email                   = StringHandling.Do.CleanSqlString(email)      if email    != None     else email
                        password                = StringHandling.Do.CleanSqlString(password)   if password != None     else password
                        passwordconfirmation    = StringHandling.Do.CleanSqlString(passwordconfirmation) \
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
            