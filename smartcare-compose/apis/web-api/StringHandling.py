from datetime import datetime

class Is():

    def number(string):

        try:

            float(string)

            return True

        except:

            return False

    def datetime(string):

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

class Do():

    def AddColumns(columns, str):

        if columns > 0:

            return str + ","

        else:

            return str

    def CleanSqlString(str):

        if str is None:

            return ""

        Remove = "'" #adicionar aqui os caracteres a serem removidos

        for c in Remove:

            str = str.replace(c, "")

        return str