# Example-python-Iothub-Postgresql-Dashboard

This is WIES-PaaS iothub example-code include the sso、rabbitmq、Postgresql service，and finally use Dashboard to show the postgresql database with iothub send。

[cf-introduce](https://advantech.wistia.com/medias/ll0ov3ce9e)

[IotHub](https://advantech.wistia.com/medias/up3q2vxvn3)

[Dashboard](https://advantech.wistia.com/medias/bpvxpuvnk4)

[graph](https://advantech.wistia.com/medias/hluoy8qdz3)


## Quick Start

cf-cli

[https://docs.cloudfoundry.org/cf-cli/install-go-cli.html](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html?source=post_page---------------------------)

python3

[https://www.python.org/downloads/](https://www.python.org/downloads/?source=post_page---------------------------)

#### Postgrsql

You can download pgAdmin so you can see the result in WISE-PaaS Postgresql servince instance

[https://www.postgresql.org/](https://www.postgresql.org/)

![](https://cdn-images-1.medium.com/max/2000/1*iJwh3dROjmveF8x1rC6zag.png)



python3 package(those library you can try application in local):

    #mqtt
    pip3 install paho-mqtt
    #python-backend
    pip3 install Flask

    #python postgresql library
    pip3 install sqlalchemy
    pip3 install psycopg2

## Download this file

    git clone this repository

## Login to WISE-PaaS

![Imgur](https://i.imgur.com/JNJmxFy.png)

    #cf login -skip-ssl-validation -a {api.domain_name}  -u "account" -p "password"

    cf login –skip-ssl-validation -a api.wise-paas.io -u xxxxx@advtech.com.tw -p xxxxxx

    #check the cf status
    cf target
    
 ## Application Introduce

#### manifest.yml

open **`manifest.yml`** and editor the **application name** to yours，because the appication can't duplicate。

We bind service in **manifest.yml** in `services`，and we will bind again in downside use command line

![Imgur](https://i.imgur.com/OQegiAy.png)

**Service Instance Name**
![Imgur](https://i.imgur.com/VVMcYO8.png)

#### SSO(Single Sign On)

This is the [sso](https://advantech.wistia.com/medias/vay5uug5q6) applicaition，open **`templates/index.html`** and editor the `ssoUrl` to your application name，

If you don't want it，you can ignore it。

    #change this **`python-demo-jimmy`** to your **application name**
    var ssoUrl = myUrl.replace('python-demo-jimmy', 'portal-sso');

#### index.py

(In `index.js` the service name need same to WISE-PaaS Service name)

![Imgur](https://i.imgur.com/6777rmg.png)

```py

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

```

Create schema & table bind in group to `groupfamily`。 


```py

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
```

Connect to mqtt service，and use `on_message` to insert data，because we want to use dashboard we need have `timestamp` and we already define in table `timestamp timestamp (2) default  current_timestamp`，so we insert one data it will creat Date automatic。

```py

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
```





Push application & Bind PostgreSQL、Rabbitmq service instance

    #cf push application_name
    cf push python-demo-postgresql --no-start

    #cf bs {application_name} {service_instance_name} -c '{\"group\":\"group_name\"}'
    #The group we define in `index.py`
    cf bs python-demo-postgresql postgresql -c '{\"group\":\"groupfamily\"}'

    #bind the rabbitmq service
    cf bs python-demo-postgresql rabbitmq

    #cf start {application_name}
    cf start python-demo-postgresql




You can look it does it sueeess use

    #cf logs {application name} --recent

![Imgur](https://i.imgur.com/2bFpboC.png)

get the application environment

#get the application environment
cf env {application name} > env.json

Edit the **publisher.py** `broker、port、username、password` you can find in **env.json**

- bokrer:"VCAP_SERVICES => p-rabbitmq => externalHosts"
- port :"VCAP_SERVICES => p-rabbitmq => mqtt => port"
- username :"VCAP_SERVICES => p-rabbitmq => mqtt => username"
- password: "VCAP_SERVICES => p-rabbitmq => mqtt => password"

open two terminal

#cf logs {application name}
cf logs python-demo-postgresql

.

    python publisher.py

![Imgur](https://i.imgur.com/eoQC698.png)

**result**

You can use pgAdmin to chech our your insert data，so you need to go to WISE-PaaS to get your config

![Imgur](https://i.imgur.com/RciwrZq.png)

go to pdAdmin(Servers => create => server)

### connection config

![Imgur](https://i.imgur.com/HEb9o42.png)

(Databases => Schemas => Tables => right click => View/Edit data)

![Imgur](https://i.imgur.com/Jbj8u2c.png)

### Open Dashboard

_ Notice:If you create your own service instance your nedd to bind it to Dashboard first_

We need to add datasource first。
(Configuration => Data sources => Add Datasource => choose the "Postgresql")

![Imgur](https://i.imgur.com/L0xB7S5.png)

#### Go back to your application and get config

![Imgur](https://i.imgur.com/88mfQkh.png)

#### Add panel

Create => Dashboard => We choose "Graph"

![Imgur](https://i.imgur.com/MYHUkyz.png)

Panel Title => Edit

## The "A" and "B" is the same thing just use the different way，you only need one

![Imgur](https://i.imgur.com/NYmmksN.png)

Now we can see our data in Dashboard graph

![Imgur](https://i.imgur.com/oiRzAtS.png)
