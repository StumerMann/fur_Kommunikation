import datetime
import paho.mqtt.client as paho
from paho import mqtt
import json
from threading import Thread
import time

db = {}
secclean = 10

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    text = str(msg.payload)[str(msg.payload).index("\'")+1:][:str(msg.payload).index("\'")+1]
    print(msg.topic + " " + str(msg.qos) + " " + str(text))
    db[str(int(time.time()))]= msg.topic + " :topic|text: " + str(text)
    json.dump(db, open("db.json", "w"))

def mains():
    global db
    client = paho.Client()
    client.on_connect = on_connect

    # enable TLS for secure connection
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    # set username and password
    client.username_pw_set("outut", "")
    # connect to HiveMQ Cloud on port 8883 (default for MQTT)
    client.connect(", 8883)

    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_publish = on_publish

    client.subscribe("out/#")
    client.subscribe("in/#")

    #client.publish("out/test", payload="hot")

    # you can also use loop_start and loop_stop / loop_forever for simplicity, here you need to stop the loop manually
    client.loop_forever()

def etnicCleaning():
    global db
    while True:
        time.sleep(2)
        k = db.copy()
        for i in k.keys():
            if int(i) + secclean < int(time.time()):
                db.pop(i)
                json.dump(db, open("db.json", "w"))
            print(db)

firstThread = Thread(target = mains)
secondThread = Thread(target = etnicCleaning)
firstThread.start()
secondThread.start()
