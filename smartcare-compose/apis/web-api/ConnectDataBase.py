import Env
import ErrorsDict
import json
import psycopg2

class Get():

    def Connection(WebApi):

        Success  = True
        Errors  = []
        Data    = []

        try:

            dsn                 = json.loads(Env.Get.DataBase())
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

                    connection = json.loads(Get.Connection(WebApi))
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
