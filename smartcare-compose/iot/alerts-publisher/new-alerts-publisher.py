import json
import paho.mqtt.client as paho
import requests
import time

broker = "broker"
port = 1883

def on_publish(client, userdata, result):  

    print("data published \n")
    pass
i=0

while i<5:

    time.sleep(2)

    client1 = paho.Client("Alert-Monitor")
    client1.on_publish = on_publish
    client1.connect(broker, port)

    AlertStatus = False

    try:

        request = requests.get("http://172.20.0.5:8082/alert")

        response = request.json()

        if response["success"]:

            AlertStatus = response["data"][0]["alert"]

            print("Leitura de alerta capturada no banco:", AlertStatus)
            i+=1

        else:

            print("Erro na iot api: ", response["errors"])
            i=11

    except Exception as ex:

        print(ex.__cause__)
        print(ex)
    
    message = json.dumps({"msg":AlertStatus})   

    ret = client1.publish("home/alert", message)