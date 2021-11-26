import base64
import json

import paho.mqtt.client as mqtt
import pylint
import datetime
import psycopg2
import os

def on_connect(mqttc, mosq, obj,rc):

    print("Connected with result code:"+str(rc))
    mqttc.subscribe('home/#')

def on_message(mqttc,obj,msg):

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

    x = json.loads(msg.payload)
    Topic_Handle(str(msg.topic), Payload)

def on_log(mqttc,obj,level,buf):

    print("message:" + str(buf))
    print("userdata:" + str(obj))

def on_publish(mosq, obj, mid):

    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):

    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def Topic_Handle(topic, value):

    print(topic , value)

    topic_array = topic.split("/")

    print(topic_array)

    if topic_array[2] == "sensor":

        print(topic_array)

        CodigoDispositivo =  topic_array[3]

        print(CodigoDispositivo)

        DataHora = datetime.datetime.today()

        Valor = list(json.loads(value).values())[0]

        try:
            
            db_host = os.getenv("DB_HOST", "")
            db_user = os.getenv("DB_USER", "")
            db_name = os.getenv("DB_NAME", "")
            db_pass = os.getenv("DB_PASS", "")

            conn = psycopg2.connect(f'dbname={db_name} user={db_user} password={db_pass} host={db_host}')
            cur = conn.cursor()
            cur.execute(f"CALL PUBLIC.USP_INSERE_MEDICAO ('{CodigoDispositivo}','{DataHora}','{Valor}','Null')")
            conn.commit()
            conn.close()

            print ("Medição cadastrada no Banco de Dados.")        
            print ("")

        except Exception as ex:

            print(ex.__cause__)
            print(ex)

mqttc= mqtt.Client("sql_handle")
mqttc.on_connect=on_connect
mqttc.on_message=on_message
mqttc.on_log=on_log
mqttc.on_publish=on_publish
mqttc.on_subscribe=on_subscribe
# mqttc.username_pw_set("smartcare","unilasalle")

mqttc.connect("iot", 1883, 60)

run = True
while run:
    mqttc.loop()

