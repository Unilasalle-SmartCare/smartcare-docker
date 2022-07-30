import ErrorsDict
import json
import os

class Get():

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
