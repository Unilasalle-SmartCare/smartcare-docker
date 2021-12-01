import datetime
import json
import os
import paho.mqtt.client as mqtt
import requests

def on_connect(mqttc, mosq, obj, rc):

    print("Connected with result code:"+str(rc))
    mqttc.subscribe('home/#')

def on_message(mqttc, obj, msg):

    print("Mensagem recebida: ")
    print(msg.payload.decode('utf-8'))
    print("Topico: "+ msg.topic)

    rssi = -1

    Topico = str(msg.topic)
    Payload = str(msg.payload.decode('utf-8'))

    print("--------Topico---------")
    print(Topico)
    print("-------Payload---------")
    print(Payload)
    print("-----------------------")

    Topic_Handle(str(msg.topic), Payload)

def on_log(mqttc, obj, level, buf):

    print("message:" + str(buf))
    print("userdata:" + str(obj))

def on_publish(mosq, obj, mid):

    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):

    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def Topic_Handle(topic, value):

    print(topic, value)

    topic_array = topic.split("/")

    print(topic_array)

    if topic_array[1] == "sensor":

        CodigoDispositivo =  topic_array[2]

        DataHora = datetime.datetime.today()

        Valor = list(json.loads(value).values())[0]

        try:
            
            request = requests.get(f"http://172.20.0.5:8082/insert/measurement/{CodigoDispositivo}/{DataHora}/{Valor}")

            CadastroStatus = str(request.content).replace("b", "").replace("'", "")

            if CadastroStatus == "True":

                print("Dados de Medição cadastrado no banco de dados!")

            else:

                print("Não foi possível inserir os dados de medição no banco de dados!")

        except Exception as ex:

            print(ex.__cause__)
            print(ex)

    elif topic_array[1] == "alert":

        print("Mensagem recebida: " + topic + " " + str(value))

        AlertStatus = list(json.loads(value).values())[0]

        if AlertStatus == "True":

            print("Alerta detectado, atuador acionado!")

mqttc = mqtt.Client("sql_handle")
mqttc.on_connect    = on_connect
mqttc.on_message    = on_message
mqttc.on_log        = on_log
mqttc.on_publish    = on_publish
mqttc.on_subscribe  = on_subscribe

mqttc.connect("iot", 1883, 60)

run = True
while run:
    mqttc.loop()

