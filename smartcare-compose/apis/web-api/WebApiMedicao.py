import ErrorsDict
import json
import requests
import StringHandling
import UrlHandling

class route:

    def GetMedicaoTratada(self):

        Success = True
        Errors  = []
        Data    = []

        try:

            DataInicioStatus, DataInicioErrors, DataInicioData = UrlHandling.Do.OpenGetValues("datainicio", 1)

            DataFimStatus, DataFimErrors, DataFimData = UrlHandling.Do.OpenGetValues("datafim", 1)

            if DataInicioStatus and DataFimStatus:

                DataInicioBusca = list(list(DataInicioData)[0].values())[0]

                DataFimBusca = list(list(DataFimData)[0].values())[0]

                if StringHandling.isdatetime(DataInicioBusca) and StringHandling.isdatetime(DataFimBusca):

                    request = requests.get(f"http://172.21.0.6:8083/medicao/tratada/{DataInicioBusca}/{DataFimBusca}")
                    
                    Medicao = request.json()

                    Medicao = Medicao["data"]

                    Data = Medicao

                else:

                    Success = False
                    Errors.append({"msg": ErrorsDict.Get.ByCode(701)})

            else:

                Success = False
                Errors.append({"msg": DataInicioErrors})
                Errors.append({"msg": DataFimErrors})

        except:

            Success = False
            Errors.append({"msg": ErrorsDict.Get.ByCode(702)})
            

        finally:

            return json.dumps({"success": Success, "errors": Errors, "data": Data})