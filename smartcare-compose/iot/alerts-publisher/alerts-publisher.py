import json
import os
import paho.mqtt.client as paho
import requests
import time

broker = "iot"
port = 1883

def on_publish(client, userdata, result):  

    print("data published \n")
    pass

while True:

    time.sleep(2)

    client1 = paho.Client("Alert-Monitor")
    client1.on_publish = on_publish
    client1.connect(broker, port)

    try:

        AlertStatus = False

        request = requests.get("http://172.20.0.5:8082/alert")

        AlertStatus = str(request.content).replace("b", "").replace("'", "")

        print("Leitura de alerta capturada no banco:", AlertStatus)

    except Exception as ex:

        print(ex.__cause__)
        print(ex)
    
    message = json.dumps({"msg":AlertStatus})   

    ret = client1.publish("home/alert", message)