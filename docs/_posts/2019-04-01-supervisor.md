---
title : SUPERVISOR
categories:
  - prod
tags:
  - documentation
  - configuration
  - deployment
  - snippets
toc: true
toc_label: " contents"
toc_sticky: true
---

### USING SUPERVISOR TO RUN GUNICORN/PYTHON PROCESS

cf : [tuto medium](https://medium.com/ymedialabs-innovation/deploy-flask-app-with-nginx-using-gunicorn-and-supervisor-d7a93aa07c18)
cf : [tuto real python](https://realpython.com/kickstarting-flask-on-ubuntu-setup-and-deployment/#configure-supervisor)


#### install supervisor
```
sudo apt-get install -y supervisor
```

#### create a new supervisor process for gunicorn
```
sudo nano /etc/supervisor/conf.d/solidata_preprod_api.conf
```

```
[program:solidata_preprod]
directory=/var/www/preprod.solidata-auth.com
command=/var/www/preprod.solidata-auth.com/venv/bin/gunicorn wsgi:app --bind 0.0.0.0:4000
autostart=true
autorestart=true

#stderr_logfile=/var/log/solidata-preprod-api/solidata-preprod-api.err.log
#stdout_logfile=/var/log/solidata-preprod-api/solidata-preprod-api.out.log
```

#### check supervisor proces
```
sudo supervisorctl reread
sudo supervisorctl update
sudo service supervisor restart
sudo supervisorctl status
```

#### restart supervisor process
```
sudo systemctl restart solidata_preprod
```

