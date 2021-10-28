function fazGet(url){
    let request = new XMLHttpRequest();
    request.open("GET", url, false);
    request.send();
    return request.responseText;
}

function criaLinha(tipoDispositivo){

    linha = document.createElement("tr");
    tdIdTipo = document.createElement("td");
    tdNome = document.createElement("td");
    tdIdTipo.innerHTML = tipoDispositivo.idtipo;
    tdNome.innerHTML = tipoDispositivo.nome;

    linha.appendChild(tdIdTipo);
    linha.appendChild(tdNome);

    return linha;
}

function listaDispositivos() {

    let data = fazGet("http://localhost:8080/dispositivo/tipos/listar");

    let jsonData = JSON.parse(data);

    let errors = ""

    if (jsonData["sucess"] == false) {
        jsonData["errors"].forEach(element =>{
            errors = errors + " - " + element.msg
        })
        alert(errors)
        return;
    }

    let tipoDispositivo = jsonData["data"];

    let tabela = document.getElementById("TiposDispositivos");

    let cabecalho = document.createElement("tr");
    cabecalhoColumn1 = document.createElement("th");
    cabecalhoColumn2 = document.createElement("th");
    cabecalhoColumn1.innerHTML = "ID";
    cabecalhoColumn2.innerHTML = "Nome";

    cabecalho.appendChild(cabecalhoColumn1);
    cabecalho.appendChild(cabecalhoColumn2);
    
    tabela.appendChild(cabecalho);

    tipoDispositivo.forEach(element =>{
        let linha = criaLinha(element);
        tabela.appendChild(linha);
    });

}

function buscaDipositivos() {

    let idbusca = document.getElementById("idbusca").value;

    if (isInt(idbusca)) {
        let data = fazGet("http://localhost:8080/dispositivo/tipos/buscar/id"+"?idbusca="+idbusca.toString());
        
        let jsonData = JSON.parse(data);

        let errors = ""

        if (jsonData["sucess"] == false) {
            jsonData["errors"].forEach(element =>{
                errors = errors + " - " + element.msg
            })
            alert(errors)
            return;
        }
    

        document.getElementById("nomebusca").value = jsonData["data"][0]["nome"]

    }
    else {
        alert("o id de busca deve ser um valor inteiro!")
    }

}

function isInt(value) {
    return !isNaN(value) && 
           parseInt(Number(value)) == value && 
           !isNaN(parseInt(value, 10));
}

function buscaDispositivosNome(){

    let nomebusca = document.getElementById("buscanome").value

    let data = fazGet("http://localhost:8080/dispositivo/tipos/buscar/nome"+"?nomebusca="+nomebusca.toString());

    let jsonData = JSON.parse(data);

    let errors = ""

    if (jsonData["sucess"] == false) {
        jsonData["errors"].forEach(element =>{
            errors = errors + " - " + element.msg
        })
        alert(errors)
        return;
    }

    let tipoDispositivo = jsonData["data"];

    let tabela = document.getElementById("TiposDispositivosBusca");
    
    let cabecalho = document.createElement("tr");
    cabecalhoColumn1 = document.createElement("th");
    cabecalhoColumn2 = document.createElement("th");
    cabecalhoColumn1.innerHTML = "ID";
    cabecalhoColumn2.innerHTML = "Nome";

    cabecalho.appendChild(cabecalhoColumn1);
    cabecalho.appendChild(cabecalhoColumn2);
    
    tabela.appendChild(cabecalho);

    tipoDispositivo.forEach(element =>{
        let linha = criaLinha(element);
        tabela.appendChild(linha);
    });

}
