var store = [{
        "title": "LICENSE",
        "excerpt":"MIT License Copyright (c) 2018 Entrepreneurs d’Intérêt Général Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,...","categories": ["meta"],
        "tags": ["license"],
        "url": "http://localhost:4001/meta/license/",
        "teaser":null},{
        "title": "GIT",
        "excerpt":"GIT WALKTHROUGH (ubuntu 18.04) cf : tuto Digital Ocean / GIT INSTALL GIT sudo apt-get update sudo apt-get install git git --version FROM /var/wwww for each : cd /var/www/solidata-api.com cd /var/www/preprod.solidata-api.com … &lt; do &gt; git init . add remote repo links git remote add origin https://github.com/entrepreneur-interet-general/solidata_backend.git if need for...","categories": ["prod"],
        "tags": ["documentation","configuration","deployment","snippets"],
        "url": "http://localhost:4001/prod/git/",
        "teaser":null},{
        "title": "MONGO DB",
        "excerpt":"MONGO DB WALKTHROUGH FOR UBUNTU cf : tuto Mongo DB / install cf : tuto Digital Ocean / install INSTALL MONGO DB install MongoDB package (-y == —yes == —assume-yes) sudo apt update sudo apt install -y mongodb check service status sudo systemctl status mongodb mongo --eval 'db.runCommand({ connectionStatus: 1...","categories": ["prod"],
        "tags": ["documentation","configuration","deployment","snippets"],
        "url": "http://localhost:4001/prod/mongo_db/",
        "teaser":null},{
        "title": "NGINX",
        "excerpt":"NGINX - SUBDOMAINS AND SERVER BLOCKS cf : tuto digital ocean cf : tuto linuxize / nginx cf : tuto linuxize / blocks SETUP NGINX install nginx sudo apt update sudo apt install nginx check status sudo systemctl status nginx check possible configs sudo ufw app list for http and...","categories": ["prod"],
        "tags": ["documentation","configuration","deployment","snippets"],
        "url": "http://localhost:4001/prod/nginx/",
        "teaser":null},{
        "title": "SUPERVISOR",
        "excerpt":"USING SUPERVISOR TO RUN GUNICORN/PYTHON PROCESS cf : tuto medium cf : tuto real python install supervisor sudo apt-get install -y supervisor create a new supervisor process for gunicorn sudo nano /etc/supervisor/conf.d/solidata_preprod_api.conf [program:solidata_preprod] directory=/var/www/preprod.solidata-auth.com command=/var/www/preprod.solidata-auth.com/venv/bin/gunicorn wsgi:app --bind 0.0.0.0:4000 autostart=true autorestart=true #stderr_logfile=/var/log/solidata-preprod-api/solidata-preprod-api.err.log #stdout_logfile=/var/log/solidata-preprod-api/solidata-preprod-api.out.log check supervisor proces sudo supervisorctl reread sudo supervisorctl...","categories": ["prod"],
        "tags": ["documentation","configuration","deployment","snippets"],
        "url": "http://localhost:4001/prod/supervisor/",
        "teaser":null},{
        "title": "UBUNTU",
        "excerpt":"INITIAL SETUP UBUNTU 18.04 cf : tuto Digital Ocean config preprod #1 ubuntu 18.04 3Go RAM / 2CPU 60Go memory IP address : YOUR.SERVER.IP.ADDRESS connect by ssh from local terminal ssh root@YOUR.SERVER.IP.ADDRESS SETUP BASICS UBUNTU sudo apt-get update sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools sudo apt install...","categories": ["prod"],
        "tags": ["documentation","configuration","deployment","snippets"],
        "url": "http://localhost:4001/prod/ubuntu/",
        "teaser":null},{
        "title": "PRESENTATION",
        "excerpt":"SOLIDATA BACKEND Solidata is a microservice (a REST API) for data management and authentication based on access and refresh JSON Web Tokens (JWT) compatible with the TADATA! sofware suite ( ApiViz / Solidata_frontend / Toktok / OpenScraper ) GOALS allow you to consume data from your own csv/xls files or...","categories": ["general"],
        "tags": ["documentation","configuration","deployment","ecosystem"],
        "url": "http://localhost:4001/general/presentation/",
        "teaser":null},{
        "title": "THE SOLIDATA ECOSYSTEM",
        "excerpt":"The goal of Solidata is to work with any external service fulfilling different roles, so we developed an eco-system of open source applications allowing a complete and free way to deploy services without paying a dime… OUR OPEN SOURCE TOOLS Toktok for a dedicated authentication service to manage users, JWT,...","categories": ["general"],
        "tags": ["documentation","configuration","ecosystem","tadata"],
        "url": "http://localhost:4001/general/ecosystem/",
        "teaser":null},{
        "title": "INSTALLATION WALKTHROUGH",
        "excerpt":"Build and run You have two different options to run (locally) solidata on your computer/server : with Python or with Docker, depending where your heart leans… WITH DOCKER - LOCALLY locally - in your browser check this url install Docker (here for mac OS) clone or download the repo install...","categories": ["guide"],
        "tags": ["documentation","configuration","installation"],
        "url": "http://localhost:4001/guide/installation/",
        "teaser":null},{
        "title": "HOW TO CONFIGURE YOUR APIVIZ INSTANCE",
        "excerpt":"Create an admin user register an user (user data will stored and managed in TokTok, so you’d need to install Toktok locally) ; make this user an admin (in TokTok) ; Go to the back office log in (admin link in the default footer, /login route by default) ; go...","categories": ["guide"],
        "tags": ["documentation","configuration","backoffice"],
        "url": "http://localhost:4001/guide/backoffice/",
        "teaser":null},{
        "title": "BASIC DATAVISUALISATION PROJECT WORKFLOW",
        "excerpt":"SETTING UP A DATAVISUALISATION PROJECT This simplified illustration aims to explain the role of each service we usually encounter in a data-visualisation project : from the raw data on your desktop (CSV, XLS…) to an online interactive data-visualisation/valorisation service (a website for instance). Note : this illustration simply lists all...","categories": ["lexicon"],
        "tags": ["documentation","schema","principles","services","data","workflow"],
        "url": "http://localhost:4001/lexicon/basic-dataviz-project/",
        "teaser":null},{
        "title": "APIVIZ ECOSYSTEM DATA FLOWS",
        "excerpt":"  Apiviz manages dataflows as follow…         MAIN DATA FLOWS AND SERVICES                                                  click to enlarge illustration         MAIN BLUEPRINT                                                  click to enlarge illustration         DETAILED BLUEPRINT                                                  click to enlarge illustration       note : illustration in jpg here    ","categories": ["lexicon"],
        "tags": ["documentation","schema","principles","services"],
        "url": "http://localhost:4001/lexicon/data-flows/",
        "teaser":null},{
        "title": "DEPLOYMENT CONFIGURATIONS",
        "excerpt":" Apiviz can be deployed according to several configurations as follow…     LEGENDS                                                  click to enlarge illustration         DEPLOYMENT CONFIGURATIONS   DEPLOYMENT AS FULL MUTUALIZED MICROSERVICES SYTEM                                                                                                                          click to enlarge illustration         DEPLOYMENT AS FULL CLIENT SOVEREIGNETY ON SERVICES                                                                                                                          click to enlarge illustration        ","categories": ["guide"],
        "tags": ["documentation","configuration","schema","principles","installation","deployment"],
        "url": "http://localhost:4001/guide/deployment-configs/",
        "teaser":null},{
        "title": "INTEROPERABILITY",
        "excerpt":"  INTEGRATION WITH OTHER SERVICES   Apiviz aims to allow integration with third party services, either open sourced or closed.   This illustrations shows various possibilities of interoperability between services.                                                    click for fullscreen view       note : illustration in jpg here  ","categories": ["lexicon"],
        "tags": ["documentation","schema","principles","services"],
        "url": "http://localhost:4001/lexicon/third-services-integration/",
        "teaser":null},{
        "title": "INSTALL THE DOCS WITH JEKYLL",
        "excerpt":"The documentation is produced with : Github pages Jekyll Minimal Mistakes template For a local deployment of the documentation project (Jekyll + MMistakes template) Install ruby, Jekyll brew install ruby gem install jekyll From your repo’s root go to the /docs folder cd /docs Install setup (given the Gemfile, Gemfile.lock...","categories": ["guide"],
        "tags": ["documentation","configuration","installation","Jekyll"],
        "url": "http://localhost:4001/guide/install-docs/",
        "teaser":null},{
        "title": "STACK",
        "excerpt":"All libraries, packages and tools listed below are under open licence. Backend Flask… minimalistic Python framework to serve configuration Flask Restplus… extension for Flask that adds support for quickly building REST APIs… Swagger documentation integrated … praise be noirbizarre… Flask-JWT-extended… wrapper JWT for Flask Flask-email… templating, sending, etc… Server Ubuntu...","categories": ["dev"],
        "tags": ["tech","stack","credits"],
        "url": "http://localhost:4001/dev/stack/",
        "teaser":null},{
        "title": "CONTRIBUTING GUIDE",
        "excerpt":"Hello fellow developer/hacker/citizen/peer! inspired by : contributing guide of udata project … document to finish … Language The development language is English. All comments and documentation should be written in English, so that we don’t end up with “frenghish” methods, and so we can share our learnings with developers around...","categories": ["dev"],
        "tags": ["tech","stack","credits"],
        "url": "http://localhost:4001/dev/contributing/",
        "teaser":null},{
        "title": "ROADMAPS",
        "excerpt":"SOLIDATA ROADMAP FRONTEND To know more check the roadmap frontend Solidata ROADMAP BACKEND / API To know more check the roadmap backend Solidata TOKTOK microservice ROADMAP API To know more check the roadmap frontend Toktok APIVIZ ROADMAP FRONTEND To know more check the roadmap frontend Apiviz ROADMAP BACKEND To know...","categories": ["dev"],
        "tags": ["tech","roadmap","stack"],
        "url": "http://localhost:4001/dev/roadmaps/",
        "teaser":null},{
        "title": "GUIDELINES FOR DEVELOPMENT",
        "excerpt":"This project is prone to be developped by several developpers, so we agreed on some basic rules… GENERAL we try to comment and document in english check out our “project” boards board to have an idea about the priorities we collectively decided to work on “see something, say something” :...","categories": ["dev"],
        "tags": ["tech","roadmap","guidelines","stack"],
        "url": "http://localhost:4001/dev/guidelines/",
        "teaser":null},{
        "title": "MAINTAIN",
        "excerpt":"  Contacts :      Julien Paris (aka JPy on Github)   ","categories": ["meta"],
        "tags": ["credits","maintainance"],
        "url": "http://localhost:4001/meta/maintain/",
        "teaser":null},{
        "title": "CREDITS",
        "excerpt":"ApiViz’s team thanks : the EIG program by Etalab the Social Connect project, aka “Carrefour des Innovations Sociales” the CGET the MedNum the Mission Société Numérique and all those who believed and helped in this project : Christophe N. Damla S. Bastien G. Mathilde B. Rémy S. Cécile B. Elise...","categories": ["meta"],
        "tags": ["credits"],
        "url": "http://localhost:4001/meta/credits/",
        "teaser":null},{
        "title": "CHANGE LOG",
        "excerpt":"  v.0.1 alpha (2019-03-06)      First published version  ","categories": ["meta"],
        "tags": ["log","versions"],
        "url": "http://localhost:4001/meta/changelog/",
        "teaser":null},{
        "title": "API - authentication",
        "excerpt":"  The API for Solidata authentication     CONFIGURATION COLLECTIONS AND DOCUMENTS   DOCUMENTED URLs   check the following url :   http://localhost:4000/api/auth/documentation  ","categories": ["api"],
        "tags": ["documentation","configuration","api"],
        "url": "http://localhost:4001/api/authentication/",
        "teaser":null},{
        "title": "API - concepts",
        "excerpt":"The API of Solidata backend deals with several distinct concepts : usr : users (endpoints and models) auth : authentication and register (endpoints) dmf : datamodel fields (endpoints and models) dmt : datamodel templates (endpoints and models) dsi : dataset inputs (endpoints and models) dso : dataset outputs (endpoints and...","categories": ["api"],
        "tags": ["documentation","configuration","api"],
        "url": "http://localhost:4001/api/concepts/",
        "teaser":null},{
        "title": "API - datamodel fields",
        "excerpt":"  The API for Solidata DMF management     DOCUMENTED URLs   check the following url :   http://localhost:4000/api/dmf/documentation  ","categories": ["api"],
        "tags": ["documentation","configuration","api"],
        "url": "http://localhost:4001/api/dmf/",
        "teaser":null},{
        "title": "API - datamodel templates",
        "excerpt":"  The API for Solidata DMT management     DOCUMENTED URLs   check the following url :   http://localhost:4000/api/dmt/documentation  ","categories": ["api"],
        "tags": ["documentation","configuration","api"],
        "url": "http://localhost:4001/api/dmt/",
        "teaser":null},{
        "title": "API - dataset inputs",
        "excerpt":"  The API for Solidata DSI management     DOCUMENTED URLs   check the following url :   http://localhost:4000/api/dsi/documentation  ","categories": ["api"],
        "tags": ["documentation","configuration","api"],
        "url": "http://localhost:4001/api/dsi/",
        "teaser":null},{
        "title": "API - dataset outputs",
        "excerpt":"  The API for Solidata DSO management     DOCUMENTED URLs   check the following url :   http://localhost:4000/api/dso/documentation  ","categories": ["api"],
        "tags": ["documentation","configuration","api"],
        "url": "http://localhost:4001/api/dso/",
        "teaser":null},{
        "title": "API - projects",
        "excerpt":"  The API for Solidata PRJ management     DOCUMENTED URLs   check the following url :   http://localhost:4000/api/prj/documentation  ","categories": ["api"],
        "tags": ["documentation","configuration","api"],
        "url": "http://localhost:4001/api/prj/",
        "teaser":null},{
        "title": "API - recipes",
        "excerpt":"  The API for Solidata REC management     DOCUMENTED URLs   check the following url :   http://localhost:4000/api/rec/documentation  ","categories": ["api"],
        "tags": ["documentation","configuration","api"],
        "url": "http://localhost:4001/api/rec/",
        "teaser":null},{
        "title": "API - users",
        "excerpt":"  The API for Solidata users management     DOCUMENTED URLs   check the following url :   http://localhost:4000/api/usr/documentation  ","categories": ["api"],
        "tags": ["documentation","configuration","api"],
        "url": "http://localhost:4001/api/users/",
        "teaser":null}]
