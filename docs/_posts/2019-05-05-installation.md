---
title : INSTALLATION WALKTHROUGH
categories:
  - guide
tags:
  - documentation
  - configuration
  - installation
toc: true
toc_label: " contents"
toc_sticky: true
---


--------

## Build and run 

You have two different options to run (locally) solidata on your computer/server : with **Python** or with **Docker**, depending where your heart leans...

--------


### WITH DOCKER - LOCALLY


- **locally - in your browser check this url**
    - install [Docker (here for mac OS)](https://docs.docker.com/docker-for-mac/install/) 
    - clone or [download](https://github.com/co-demos/ApiViz/archive/master.zip) the repo
    - [install MongoDB](https://docs.mongodb.com/manual/installation/) locally/on your server or get the URI of the MongoDB you're using
    - go to your `/solidata` folder
    - launch docker and run : 
        ```sh
        make up
        ```
    - check the following URL in your browser : 
      ```
      http://localhost:4000/api/dsi/documentation
      ```    

- **in production** 
    - install [Docker](https://phoenixnap.com/kb/how-to-install-docker-on-ubuntu-18-04) on your server (here for Ubuntu 18) 
      ```sh
      sudo apt-get update
      sudo apt-get remove docker docker-engine docker.io
      sudo apt install docker.io
      sudo systemctl start docker
      sudo systemctl enable docker
      ```
    - set up UFW, GIT, NGINX, ...
    - (optional) [install MongoDB](https://docs.mongodb.com/manual/installation/) (if the solidata's DB for config is hosted on your own server)
    - add the github repo
    - create and set of secret env variables at the project's folder root based on `example.env.global` and `example.env.mongodb`
    - lauch docker and run the command : 
      ```sh
      make up-prod
      ```

    - test the following url in your browser : 
    [`http://localhost:4000/api/dsi/documentation`](http://localhost:4000/api/dsi/documentation)

<hr>

### _WITHOUT DOCKER - LOCALLY_

1. **clone or [download](https://github.com/co-demos/ApiViz/archive/master.zip) the repo**
1. **[install MongoDB](https://docs.mongodb.com/manual/installation/) locally** or get the URI of the MongoDB you're using
1. **go to your solidata folder**
1. **install python pip and virtualenv**
	```sh 
	sudo apt install python-pip
	sudo apt install virtualenv
	```


1. **install a [virtual environment](https://pypi.python.org/pypi/virtualenv)**
	```sh
	virtualenv -p python3 venv
	source venv/bin/activate
	````
		
1. **install the libraries**

	```sh
	sudo pip install -r requirements.txt
	```


1. **Go to your app folder and run :**

	```sh
	python appserver.py
	````
1. **optional** : you can also use some variables in the command line : 
	```sh
	# get the list of available CLI options
	python appserver.py --help

	# for example : run with a custom port number in testing mode
	python appserver.py --port=4001 --mode=preprod
	```

1. **test the following url in your browser** : 
[`http://localhost:4001/api/dsi/documentation`](http://localhost:4001/api/dsi/documentation)


### _WITHOUT DOCKER - IN PRODUCTION_

1. **get a server** - check digital ocean, OVH, ...
1. optionnal : get a domain name : check OVH, namecheap, godaddy.... + setup DNS
1. **follow (most of) these [instructions](https://github.com/entrepreneur-interet-general/tutos-2018/wiki/Admin-Sys)**
1. **go to app folder and create a virtual env** (for instance called "venv")
1. **create and set of secret env variables** at the project's folder root based on `example.env.global` and `example.env.mongodb`
1. **set up the [gunicorn service](./unit/working_service_config.service) and [NGINX](./nginx/working_nginx_config)** with supervisor 

1. ... pray for all that to work as expected, and keep calm... 

1. **update code and (re-)deploy**

    ```sh
    cd /<your_app_folder>/<username>/app_solidata
    git pull origin master

    # start app with supervisor
    sudo supervisorctl start solidata
    ```
    
--------

## Environment variables


### the `.env` files

The environment variables are stored in a couple of files at the root of the project : 

- `example.env.global`
- `example.env.mongodb`

If you want or need to use Apiviz in production you will have to duplicate those files at the same level with those new names : 

- `.env.global`
- `.env.mongodb`

... then you will be able to change the environment variable you want and begin to use all of the available arguments like :

```sh
# with Docker
make up-prod
```

```sh
# with Python only
python appserver.py mongodb=distant mode=dev_email
```

```sh
# with Gunicorn
gunicorn wsgi_prod:app --bind=0.0.0.0:4000
```


### the variables

At the CLI level you can use :

``` python
@click.option('--mode', default="dev", nargs=1, help="The <mode> you need to run the app : dev (default), dev_email, prod, preprod" )
@click.option('--docker',  default="docker_off", nargs=1,  help="Are you running the app with <docker> : docker_off | docker_on" )
@click.option('--host', default="localhost", nargs=1,  help="The <host> name you want the app to run on : localhost(default) | <IP_NUMBER> " )
@click.option('--port', default="4000", nargs=1,  help="The <port> number you want the app to run on : 4000 (default) | <PORT_NUMBER>")
@click.option('--mongodb', default="local", nargs=1,  help="The <mongodb> you need to run the app : local | distant | server" )
@click.option('--rsa', default="no", nargs=1,  help="The <rsa> mode (RSA encrypt/decrypt for forms), protects '/login' + '/register' + '/password_forgotten' + '/reset_password': 'no' (default), 'yes'" )
@click.option('--anojwt', default="no", nargs=1, help="The <anojwt> mode (needs an anonymous JWT for login and register routes), affects '/login' + '/register' + '/password_forgotten' : 'no' (default), 'yes'" )
@click.option('--antispam', default="no", nargs=1, help="The <antispam> mode (add hidden field check for forms) protects '/login' + '/register' + '/password_forgotten' : 'no' (default), 'yes'" )
@click.option('--antispam_val', default="", nargs=1, help="The <antispam_val> to check in forms against spams : '' (default), <your-string-to-check>" )
@click.option('--https', default="false", nargs=1, help="The <https> mode you want the app to run on : true | false")
```

Within the `.env`files you can change the following variables : 

- `example.env.global`

``` bash
RUN_MODE=default
DOCKER_MODE=docker_off
AUTH_MODE=local
HTTPS_MODE=false

### FLASK RELATED 
DEBUG=true
TESTING=true
DOMAIN_ROOT=localhost
DOMAIN_PORT=4000
SECRET_KEY=app_very_secret_key
SERVER_NAME_TEST=True

### MONGO DB RELATED
MONGODB_MODE=local

```

- `example.env.mongodb`

``` bash

### to build mongodb URI
MONGO_ROOT_LOCAL=localhost
MONGO_ROOT_DOCKER=host.docker.internal
MONGO_PORT_LOCAL=27017

MONGO_DBNAME=solidata
MONGO_DBNAME_TEST=solidata-test
MONGO_DBNAME_PREPROD=solidata-preprod
MONGO_DBNAME_PROD=solidata-prod

MONGO_ROOT_SERVER=127.0.0.1
MONGO_PORT_SERVER=27017
MONGO_USER_SERVER=MY-MONGODB-SERVER-USERNAME
MONGO_PASS_SERVER=MY-MONGODB-SERVER-USER-PASSWORD
MONGO_OPTIONS_SERVER=?MY-MONGODB-SERVER-OPTIONS

### for instance on MongodbAtlas
MONGO_DISTANT_URI=mongodb://<DISTANT-USERNAME>:<DISTANT-PASSWORD>@<DISTANT-HOST>:<DISTANT-PORT>
MONGO_DISTANT_URI_OPTIONS=?ssl=true&replicaSet=<REPLICA-SET>&authSource=admin&retryWrites=true

### mongodb collections
MONGO_COLL_TAGS=tags
MONGO_COLL_USERS=users
MONGO_COLL_LICENCES=licences
MONGO_COLL_JWT_BLACKLIST=jwt_blacklist
```