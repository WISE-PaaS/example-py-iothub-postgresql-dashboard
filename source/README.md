
# WISE-PaaS example-python-Postgresql & MQTT Data Worker

This example can show you how to use WISE-PaaS Postgresql and Rabbitmq and we can make a device connection application

## STEP 1:Prepare Environment

cf-cli

[https://docs.cloudfoundry.org/cf-cli/install-go-cli.html](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html?source=post_page---------------------------)

python3

[https://www.python.org/downloads/](https://www.python.org/downloads/?source=post_page---------------------------)

![](https://cdn-images-1.medium.com/max/2000/0*z9YCGSvJ3XnTjF7q.png)

## STEP 2:How to use Rabbitmq(MQTT)

This article only tell you the quick set up，go to download this article

[https://github.com/WISE-PaaS/example-python-iothub-sso](https://github.com/WISE-PaaS/example-python-iothub-sso?source=post_page---------------------------)

First，we need to use cf to login to our WISE-PaaS ，if you can’t login you need to check our your domain is wise-paas.ioor wise-paas.com 。

![domain_name](https://cdn-images-1.medium.com/max/2000/1*o_Dd2Nh5wBBhCLt6JTXp_g.png)*domain_name*

    #cf login -skip-ssl-validation -a {api.domain_name}  -u "account" -p "password"

    cf login –skip-ssl-validation -a api.wise-paas.io -u xxxxx@advtech.com.tw -p xxxxxx

    #check the cf status

    cf target

Open the manifest.yml and **edit** the application name to yours，because the application name can't duplicate。

open templates/index.html

    #change this '**python-demo-jimmy'** to your ***application name***
    var ssoUrl = myUrl.replace('python-demo-jimmy', 'portal-sso');

When we login，we need to push our application to the WISE-PaaS

    #cf push {application name}
    cf push python-demo-postgresql

and we need to get the application environment save it to env.json

    #cf env {application name} > env.json

Edit the “publisher.py” broker、port、username、password you can find in env.json

* bokrer:”VCAP_SERVICES => p-rabbitmq => externalHosts”

* port :”VCAP_SERVICES => p-rabbitmq => mqtt => port”

* username :”VCAP_SERVICES => p-rabbitmq => mqtt => username”

* password: “VCAP_SERVICES => p-rabbitmq => mqtt => password”

open two terminal

    #cf logs {application name}
    cf logs python-demo-postgresql

&

    python publish.py

![](https://cdn-images-1.medium.com/max/2466/1*WzwjNwVA7QMZRJn7bGH27Q.png)

## STEP 3: PostgreSQL Setup

First we need to install two library to help us connect to WISE-PaaS PostgreSQL。

    #The two command install in local so no necessary because we need to install in WISE-PaaS use python_buildpack 
    pip3 install psycopg2

    pip3 install sqlalchemy

The above code is install library in your computer，but we also need to let our pytho_buildpack to install。

Open requirements.txt and add sqlalchemy 、 psycopg2

<iframe src="https://medium.com/media/98c91b4947b649fce7e6d12f43160a53" frameborder=0></iframe>

Now，we can add PostgreSQL python code。

open index.py ，add our library，and get application environment in WISE-PaaS，you need to notice the service_name must same as in WISE-PaaS。

<iframe src="https://medium.com/media/30fd8ba82ab5ce4633a547d220d71b95" frameborder=0></iframe>

![service_name](https://cdn-images-1.medium.com/max/2050/1*XXNNAxBurUm_Sp-d9Ps8lQ.png)*service_name*

Add PostgreSQL connection config， POSTGRES save the connection config we define above，and we also create own schema and table let then belong to group name “groupfamily”

<iframe src="https://medium.com/media/59fb1cff17f4cf101f4aaca73f58a4ff" frameborder=0></iframe>

and we also create two route to help us debug， /temp(get) can show all the data in Postgresql， /insert(post) can insert fake data。

<iframe src="https://medium.com/media/3307ca84fbf41aeb720f3f83ecdb8460" frameborder=0></iframe>

Because we already push our application in WISE-PaaS and it still working，so we need to stop it。

    #cf stop {application_name}
    cf stop python-demo-postgresql

    #cf push python-demo-postgresql --no-start

![service_instance_name](https://cdn-images-1.medium.com/max/2042/1*4ttlqPf5eSYSoUFVm4BmWQ.png)*service_instance_name*

Now we need to know the service instance name in WISE-PaaS，we want to bind to our application and set the group to our application。

    cf bs python-demo-postgresql postgresql -c '{\"group\":\"groupfamily\"}'

(I use windows，if you use other OS ， cf bs -h can tell you how to bind group)

Start it。

    cf start python-demo-postgresql

If you have pgAdmin you can connect it and check it，use cf env {appilcation name} or go to application list => environment to get。

![application list environment](https://cdn-images-1.medium.com/max/2044/1*DF84pOezPIowrfEKtrI_-A.png)*application list environment*

![](https://cdn-images-1.medium.com/max/2000/1*N_v_7TlrNYd593JhpRJfmA.png)

(Serves => create serves)

* Host => VCAP_SERVICES => postgresql-innoworks=>external_host

* port => VCAP_SERVICES => postgresql-innoworks=> credentials=>port

* database => VCAP_SERVICES => postgresql-innoworks=> credentials=>database

* username => VCAP_SERVICES => postgresql-innoworks=> credentials=> username

* password => VCAP_SERVICES => postgresql-innoworks=> credentials=>password

Now we want to use rabbit(MQTT) to send data，in** step 2** we already set the rabbitmq sevice，so we just need to use on_message receive our data and sent to PostgreSQL

<iframe src="https://medium.com/media/99a6e79a8542c1b1968ff6c888a79b9b" frameborder=0></iframe>

![](https://cdn-images-1.medium.com/max/2000/1*ii0IszkEeTKo3xqsink7Eg.png)

![](https://cdn-images-1.medium.com/max/2410/1*ev2O442ygq9dPYI4YhbiCQ.png)
