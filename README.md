# Example-python-Iothub-Postgresql

This is WIES-PaaS iothub example-code include the sso、rabbitmq、Postgresql service。

**https://wise-paas.advantech.com/en-us**

## Quick Start

cf-cli

[https://docs.cloudfoundry.org/cf-cli/install-go-cli.html](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html?source=post_page---------------------------)

python3

[https://www.python.org/downloads/](https://www.python.org/downloads/?source=post_page---------------------------)

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

    git clone this respository

## Login to WISE-PaaS

![Imgur](https://i.imgur.com/JNJmxFy.png)

    #cf login -skip-ssl-validation -a {api.domain_name}  -u "account" -p "password"

    cf login –skip-ssl-validation -a api.wise-paas.io -u xxxxx@advtech.com.tw -p xxxxxx

    #check the cf status
    cf target

open **`manifest.yml`** and editor the **application name** to yours，because the appication can't duplicate。

![Imgur](https://i.imgur.com/OQegiAy.png)

open **`templates/index.html`**

#change this **`python-demo-jimmy`** to your **application name**
var ssoUrl = myUrl.replace('python-demo-jimmy', 'portal-sso');

(In `index.js` the service name need same to WISE-PaaS Service name)
![https://github.com/WISE-PaaS/example-python-iothub-postgresql/blob/master/source/servicename.PNG](https://github.com/WISE-PaaS/example-python-iothub-postgresql/blob/master/source/servicename.PNG)
![Imgur](https://i.imgur.com/6777rmg.png)

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

**service_instance_name**
![Imgur](https://i.imgur.com/VVMcYO8.png)

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

We need to add datasource first。
(Configuration => Data sources => Add Datasource => choose the "Postgresql")

![Imgur](https://i.imgur.com/L0xB7S5.png)

#### Go back to your application and get config

![Imgur](https://i.imgur.com/88mfQkh.png)

#### Add panel

Create => Dashboard => We choose "Graph"

[Imgur](https://i.imgur.com/MYHUkyz.png)

Panel Title => Edit

## The "A" and "B" is the same thing just use the different way

[Imgur](https://i.imgur.com/NYmmksN.png)

Now we can see our data in Dashboard graph

[Imgur](https://i.imgur.com/oiRzAtS.png)
