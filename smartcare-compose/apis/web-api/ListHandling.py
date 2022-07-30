from datetime import datetime

class MapDate:

    def ToString(ListTuple):

        try:

            resultList = list(ListTuple)
            count = 0

            for var in ListTuple:

                if type(var).__name__ == "date":

                    resultList[count] = var.strftime(f"%d/%m/%Y, %H:%M:%S")

                count += 1
            
            return tuple(resultList)

        except:

            return None

