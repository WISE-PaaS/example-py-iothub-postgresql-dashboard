from flask import Flask, render_template
import json
import paho.mqtt.client as mqtt
import os
import sqlalchemy

app = Flask(__name__)

# port from cloud environment variable or localhost:3000
port = int(os.getenv("PORT", 3000))


@app.route('/', methods=['GET'])
def root():

    if(port == 3000):
        return 'hello world! i am in the local'
    elif(port == int(os.getenv("PORT"))):
        return render_template('index.html')


# MQTT(rabbitmq)
vcap_services = os.getenv('VCAP_SERVICES')
vcap_services_js = json.loads(vcap_services)
service_name = 'p-rabbitmq'
broker = vcap_services_js[service_name][0]['credentials']['protocols']['mqtt']['host']
username = vcap_services_js[service_name][0]['credentials']['protocols']['mqtt']['username'].strip()
password = vcap_services_js[service_name][0]['credentials']['protocols']['mqtt']['password'].strip()
mqtt_port = vcap_services_js[service_name][0]['credentials']['protocols']['mqtt']['port']


# Postgresql
service_name = 'postgresql-innoworks'
database_database = vcap_services_js[service_name][0]['credentials']['database']
database_username = vcap_services_js[service_name][0]['credentials']['username'].strip(
)
database_password = vcap_services_js[service_name][0]['credentials']['password'].strip(
)
database_port = vcap_services_js[service_name][0]['credentials']['port']
database_host = vcap_services_js[service_name][0]['credentials']['host']


POSTGRES = {
    'user': database_username,
    'password': database_password,
    'db': database_database,
    'host': database_host,
    'port': database_port,
}


schema = 'room'
table = 'livingroom'
group = 'groupfamily'
engine = sqlalchemy.create_engine('postgresql://%(user)s:\
%(password)s@%(host)s:%(port)s/%(db)s' % POSTGRES, echo=True)  # connect to server


engine.execute("CREATE SCHEMA IF NOT EXISTS "+schema+" ;")  # create schema

engine.execute("ALTER SCHEMA "+schema+" OWNER TO "+group+" ;")

engine.execute("CREATE TABLE IF NOT EXISTS "+schema+"."+table+" \
        ( id serial, \
          timestamp timestamp (2) default current_timestamp, \
          temperature integer, \
          PRIMARY KEY (id));")

engine.execute("ALTER TABLE "+schema+"."+table+" OWNER to "+group+";")
engine.execute("GRANT ALL ON ALL TABLES IN SCHEMA "+schema+" TO "+group+";")
engine.execute("GRANT ALL ON ALL SEQUENCES IN SCHEMA "+schema+" TO "+group+";")


# mqtt connect
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/hello")
    print('subscribe on /hello')


def on_message(client, userdata, msg):

    engine.execute("INSERT INTO "+str(schema)+"."+str(table) +
                   " (temperature) VALUES ("+str(msg.payload.decode())+") ", echo=True)
    print('insert sueecssful')
    print(msg.topic+','+msg.payload.decode())


client = mqtt.Client()

client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, mqtt_port, 60)
client.loop_start()


# postgresql api
@app.route('/temp', methods=['GET'])
def temp():

    numOfTempsReturned = 30

    res = engine.execute("SELECT * FROM ( SELECT * FROM "+schema+"."+table+" ORDER BY timestamp DESC LIMIT "+str(numOfTempsReturned)+") \
      AS lastRows ORDER BY timestamp ASC;")
    output = []
    for r in res:
        output.append(r)

    return str(output)


@app.route('/insert', methods=['POST'])
def insert_data():

    data = 11
    engine.execute("INSERT INTO "+str(schema)+"."+str(table) +
                   " (temperature) VALUES ("+str(data)+") ", echo=True)

    return 'insert sueecssful'


if __name__ == '__main__':
    # Run the app, listening on all IPs with our chosen port number
    app.run(host='0.0.0.0', port=port)


# cf stop python-demo-postgresql
# cf push python-demo-postgresql --no-start
# cf bs python-demo-postgresql postgresql -c '{\"group\":\"groupfamily\"}'
# cf bs python-demo-postgresql rabbitmq

# cf start python-demo-postgresql
