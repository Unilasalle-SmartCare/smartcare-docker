from bottle import Bottle, request
import ConnectDataBase
import ErrorsDict
import ErrorsPages
import json
import ListHandling
import StringHandling
import UrlHandling
import WebApiAmbiente
import WebApiCidade
import WebApiDispositivo
import WebApiEnfermidade
import WebApiEstado
import WebApiTipoDispositivo
import WebApiMedicao
import WebApiPaciente
import WebApiUsuario

class WebApi(Bottle):

    def __init__(self):

        super().__init__()

        # TipoDispositivo

        self.route("/microservices/web/dispositivo/tipo/get/all", method = "GET", callback = self.TipoDispositivoGetAll)

        self.route("/microservices/web/dispositivo/tipo/get/actives", method = "GET", callback = self.TipoDispositivoGetAll)

        self.route("/microservices/web/dispositivo/tipo/getby/id", method = "GET", callback = self.TipoDispositivoGetById)

        self.route("/microservices/web/dispositivo/tipo/getby/name", method = "GET", callback = self.TipoDispositivoGetByName)

        self.route("/microservices/web/dispositivo/tipo/insert", method = "POST", callback = self.TipoDispositivoInsert)

        self.route("/microservices/web/dispositivo/tipo/update", method = "PUT", callback = self.TipoDispositivoUpdate)

        self.route("/microservices/web/dispositivo/tipo/update/name", method = "PATCH", callback = self.TipoDispositivoUpdateName)

        self.route("/microservices/web/dispositivo/tipo/delete", method = "DELETE", callback = self.TipoDispositivoDelete)

        # Dispositivo

        self.route("/microservices/web/dispositivo/get/all", method = "GET", callback = self.DispositivoGetAll)

        self.route("/microservices/web/dispositivo/get/actives", method = "GET", callback = self.DispositivoGetAll)

        self.route("/microservices/web/dispositivo/get/pending", method = "GET", callback = self.DispositivoGetAll)        

        self.route("/microservices/web/dispositivo/getby/id", method = "GET", callback = self.DispositivoGetById)

        self.route("/microservices/web/dispositivo/getby/id/type", method = "GET", callback = self.DispositivoGetById)

        self.route("/microservices/web/dispositivo/getby/id/environment", method = "GET", callback = self.DispositivoGetById)

        self.route("/microservices/web/dispositivo/getby/string/name", method = "GET", callback = self.DispositivoGetByString)

        self.route("/microservices/web/dispositivo/getby/string/code", method = "GET", callback = self.DispositivoGetByString)

        self.route("/microservices/web/dispositivo/insert", method = "POST", callback = self.DispositivoInsert)

        self.route("/microservices/web/dispositivo/update", method = "PUT", callback = self.DispositivoUpdate)

        self.route("/microservices/web/dispositivo/update/name", method = "PATCH", callback = self.DispositivoUpdateName) 
            
        self.route("/microservices/web/dispositivo/update/code", method = "PATCH", callback = self.DispositivoUpdateCode) 
               
        self.route("/microservices/web/dispositivo/delete", method = "DELETE", callback = self.DispositivoDelete)

        # Ambiente

        self.route("/microservices/web/ambiente/get/all", method = "GET", callback = self.AmbienteGetAll)

        self.route("/microservices/web/ambiente/get/actives", method = "GET", callback = self.AmbienteGetAll)

        self.route("/microservices/web/ambiente/getby/id", method = "GET", callback = self.AmbienteGetById)

        self.route("/microservices/web/ambiente/getby/string/name", method = "GET", callback = self.AmbienteGetByString)

        self.route("/microservices/web/ambiente/getby/string/description", method = "GET", callback = self.AmbienteGetByString)

        self.route("/microservices/web/ambiente/insert", method = "POST", callback = self.AmbienteInsert)

        self.route("/microservices/web/ambiente/update", method = "PUT", callback = self.AmbienteUpdate)

        self.route("/microservices/web/ambiente/update/name", method = "PATCH", callback = self.AmbienteUpdateName)

        self.route("/microservices/web/ambiente/update/description", method = "PATCH", callback = self.AmbienteUpdateDescription)

        self.route("/microservices/web/ambiente/delete", method = "DELETE", callback = self.AmbienteDelete)

        # Medição

        self.route("/microservices/web/medicao/tratada", method = "GET", callback = self.MedicaoTratada)

        # Usuario

        self.route("/microservices/web/usuario/login", method = "POST", callback = self.UsuarioLogin)

        self.route("/microservices/web/usuario/register", method = "POST", callback = self.UsuarioRegister)

        # Enfermidade

        self.route("/microservices/web/enfermidade/get/all", method = "GET", callback = self.EnfermidadeGetAll)

        # Estado

        self.route("/microservices/web/estado/get/all", method = "GET", callback = self.EstadoGetAll)
        
        # Cidade

        self.route("/microservices/web/cidade/get/all", method = "GET", callback = self.CidadeGetAll)

        self.route("/microservices/web/cidade/getby/id/estado", method = "GET", callback = self.CidadeGetByIdEstado)

        # Paciente

        self.route("/microservices/web/paciente/get/all", method = "GET", callback = self.PacienteGetAll)

        self.route("/microservices/web/paciente/getby/id", method = "GET", callback = self.PacienteGetById)

        self.route("/microservices/web/paciente/getby/string/name", method = "GET", callback = self.PacienteGetByString)

        self.route("/microservices/web/paciente/getby/string/cpf", method = "GET", callback = self.PacienteGetByString)

        #self.route("/microservices/web/paciente/insert", method = "POST", callback = self.PacienteInsert)

        #self.route("/microservices/web/paciente/update", method = "PUT", callback = self.PacienteUpdate)

        #self.route("/microservices/web/paciente/delete", method = "DELETE", callback = self.PacienteDelete)

        # Alerta

        @self.error(400)

        def error_handler_400(error):

            return ErrorsPages.Get.error400(error)

        @self.error(401)

        def error_handler_401(error):

            return ErrorsPages.Get.error401(error)

        @self.error(403)

        def error_handler_403(error):

            return ErrorsPages.Get.error403(error)

        @self.error(404)

        def error_handler_404(error):

            return ErrorsPages.Get.error404(error)

        @self.error(405)

        def error_handler_405(error):

            return ErrorsPages.Get.error405(error)

        @self.error(408)

        def error_handler_408(error):

            return ErrorsPages.Get.error408(error)

        @self.error(500)

        def error_handler_500(error):

            return ErrorsPages.Get.error500(error)

        @self.error(501)

        def error_handler_501(error):

            return ErrorsPages.Get.error501(error)

        @self.error(502)

        def error_handler_502(error):

            return ErrorsPages.Get.error502(error)

        @self.error(503)

        def error_handler_503(error):

            return ErrorsPages.Get.error503(error)

        try:

            connection          = json.loads(ConnectDataBase.Get.Connection(self))
            connectionStatus    = list(connection.values())[0]
            connectionErrors    = list(connection.values())[1]
            connectionData      = list(connection.values())[2]

            if connectionStatus == False:

                print(connectionErrors)

            else:

                print("Conection has been established!")
                print(list(list(connectionData)[0].values())[0])

        except:
            
            print("Connection error!")
            print(ConnectDataBase.Get.Connection(self))

    #   TipoDispositivo

    def TipoDispositivoGetAll(self):

        return WebApiTipoDispositivo.route.GetAll(self)

    def TipoDispositivoGetById(self):

        return WebApiTipoDispositivo.route.GetById(self)

    def TipoDispositivoGetByName(self):

        return WebApiTipoDispositivo.route.GetByName(self)

    def TipoDispositivoInsert(self):

        return WebApiTipoDispositivo.route.Insert(self)

    def TipoDispositivoUpdate(self):

        return WebApiTipoDispositivo.route.Update(self)

    def TipoDispositivoUpdateName(self):

        return WebApiTipoDispositivo.route.UpdateName(self)

    def TipoDispositivoDelete(self):

        return WebApiTipoDispositivo.route.Delete(self)

    #   Dispositivo

    def DispositivoGetAll(self):

        return WebApiDispositivo.route.GetAll(self)

    def DispositivoGetById(self):

        return WebApiDispositivo.route.GetById(self)

    def DispositivoGetByString(self):

        return WebApiDispositivo.route.GetByString(self)

    def DispositivoInsert(self):

        return WebApiDispositivo.route.Insert(self)

    def DispositivoUpdate(self):

        return WebApiDispositivo.route.Update(self)

    def DispositivoUpdateName(self):

        return WebApiDispositivo.route.UpdateName(self)

    def DispositivoUpdateCode(self):

        return WebApiDispositivo.route.UpdateCode(self)

    def DispositivoDelete(self):

        return WebApiDispositivo.route.Delete(self)

    #   Ambiente

    def AmbienteGetAll(self):

        return WebApiAmbiente.route.Getall(self)

    def AmbienteGetById(self):

        return WebApiAmbiente.route.GetById(self)

    def AmbienteGetByString(self):

        return WebApiAmbiente.route.GetByString(self)

    def AmbienteInsert(self):

        return WebApiAmbiente.route.Insert(self)

    def AmbienteUpdate(self):

        return WebApiAmbiente.route.Update(self)

    def AmbienteUpdateName(self):

        return WebApiAmbiente.route.UpdateName(self)

    def AmbienteUpdateDescription(self):

        return WebApiAmbiente.route.UpdateDescription(self)

    def AmbienteDelete(self):

        return WebApiAmbiente.route.Delete(self)

    #   Medição

    def MedicaoTratada(self):

        return WebApiMedicao.route.GetMedicaoTratada(self)

    #   Usuario

    def UsuarioLogin(self):

        return WebApiUsuario.route.GetUsuarioLogin(self)

    def UsuarioRegister(self):

        return WebApiUsuario.route.UsuarioRegister(self)

    #   Estado
    
    def EstadoGetAll(self):

        return WebApiEstado.route.GetAll(self)

    #   Cidade

    def CidadeGetAll(self):

        return WebApiCidade.route.GetAll(self)

    def CidadeGetByIdEstado(self):

        return WebApiCidade.route.GetByIdEstado(self)

    #   Enfermidade

    def EnfermidadeGetAll(self):

        return WebApiEnfermidade.route.GetAll(self)

    #   Paciente
    
    def PacienteGetAll(self):

        return WebApiPaciente.route.GetAll(self)

    def PacienteGetById(self):

        return WebApiPaciente.route.GetById(self)

    def PacienteGetByString(self):

        return WebApiPaciente.route.GetByString(self)

if __name__ == '__main__':

    webapi = WebApi()
    webapi.run(host='0.0.0.0', port=8081, debug=True)
