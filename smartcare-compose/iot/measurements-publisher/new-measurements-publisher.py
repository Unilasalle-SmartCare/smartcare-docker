import json
import paho.mqtt.client as paho
import random
import time

broker = "broker"
port = 1883

def on_publish(client,userdata,result):  

    print("data published \n")
    pass

m = random.randrange(1,10)
while m >= 9:

    time.sleep(10)

    client1 = paho.Client("sensor-BTN-01")
    client1.on_publish = on_publish
    client1.connect(broker,port)
    m = random.randrange(1,10)  
    
    
    message = json.dumps({"msg":m,"dispositivo":"BTN-01"})   

    ret = client1.publish("home/sensor/BTN-01",message)
