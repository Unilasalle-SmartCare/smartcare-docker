from bottle import request
from urllib.parse import parse_qs
import ErrorsDict
import json

class Do():

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

            variavel        = json.loads(Do.FindGetVars(varsearch))
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
