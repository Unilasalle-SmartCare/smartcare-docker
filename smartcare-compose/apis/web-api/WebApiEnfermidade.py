import ConnectDataBase
import ErrorsDict
import json

class route:

    def GetAll(self):

        connection          = json.loads(ConnectDataBase.Get.Status(self))
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

                return json.dumps({"success": Success, "errors": Errors, "data": Data},sort_keys=True, indent=4, ensure_ascii=False)
        
        else:

            # connectionErrors só será passado para usuarioid 1(suporte)
            Errors = [{"msg": ErrorsDict.Get.ByCode(300)}]

            return json.dumps({"success": connectionStatus, "errors": Errors, "data": connectionData},sort_keys=True, indent=4, ensure_ascii=False)