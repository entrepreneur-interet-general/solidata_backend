export APP=solidata

export D_FOLDER=docker-files
export DC_FOLDER=dockercomposes
export DF_FOLDER=dockerfiles

#other variable definition
# DC    := docker-compose
# DF    := Dockerfile.

export DC=docker-compose
export DF=Dockerfile.

export DC_PREFIX= $(shell pwd)/${DC}
export DC_PREFIX_FOLDER= $(shell pwd)/${D_FOLDER}/${DC_FOLDER}/${DC}

export DC_FOLDER_SUBPATH= ${D_FOLDER}/${DC_FOLDER}
export DF_FOLDER_SUBPATH= ${D_FOLDER}/${DF_FOLDER}

export APP_PATH := $(shell pwd)

export BACKEND=${APP_PATH}
export FRONTEND=${APP_PATH}



### ============ ###
### network
### ============ ###

network:
	@docker network create ${APP} 2> /dev/null; true
network-stop:
	docker network rm ${APP}


### ============ ###
### backend
### ============ ###

# dev 
gunicorn-dev:
	${DC} -f ${DC_PREFIX_FOLDER}-gunicorn-dev.yml up --build
gunicorn-dev-stop:
	${DC} -f ${DC_PREFIX_FOLDER}-gunicorn-dev.yml down

# prod 
gunicorn-prod:
	${DC} -f ${DC_PREFIX_FOLDER}-gunicorn-prod.yml up --build -d
gunicorn-prod-stop:
	${DC} -f ${DC_PREFIX_FOLDER}-gunicorn-prod.yml down


### ============================= ###
### main make / docker commands
### ============================= ###

# dev 
up: network gunicorn-dev
down: gunicorn-dev-stop network-stop
restart: down up

# prod
up-prod: network gunicorn-prod
down-prod: gunicorn-prod-stop network-stop
restart-prod: down-prod up-prod