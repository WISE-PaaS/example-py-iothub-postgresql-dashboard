import paho.mqtt.client as mqtt
import random 
#externalHosts
broker="40.81.27.10"
#mqtt_port
mqtt_port=1883
#mqtt_username
username="f456d95d-b76f-43e9-8b35-bac8383bf941:270ddafc-f9c7-4c26-8214-1f31bdd912b0"
password="D2NMhE61GsvqQ9lIT6IlZiwv3"
def on_publish(client,userdata,result):             #create function for callback
    print("data published")
   
client= mqtt.Client()                           #create client object

client.username_pw_set(username,password)

client.on_publish = on_publish                          #assign function to callback
client.connect(broker,mqtt_port)                                 #establish connection
client.publish("/hello",random.randint(10,30))    




