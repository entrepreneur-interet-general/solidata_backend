<h1 align=center>  SOLIDATA <br> backend</h1>


-------
## PRESENTATION

part 2a/3 of the TADATA! sofware suite (ApiViz / Solidata / OpenScraper)

A public service for managing, consolidating, and sharing data 


-------

## GOALS

- allow you to consume data from your own csv/xls files or external APIs ;
- consolidate your data : apply your own datamodel, simplify columns, apply metadatas, ... ; 
- share the consolidated datas on API endpoints with the level of openness you decide (opendata, commons, collective, private) ;
- manage all your data and your recipes by projects ;
- be able to manage projects by teams and share data/recipes/


-------

![alt text](./screenshots/endpoints_users.png "endpoint users")

------

## TECHNICAL POINTS

#### Tech stack
- _Language_  : **Python3**... yes ... I know ... hmmm ... gnnn ... don't judge me ?
- _Framework_ : **[Flask](http://flask.pocoo.org/)**... minimalistic Python framework
- _API_       : **[Flask-RestPlus](http://flask-restplus.readthedocs.io/en/stable/)**... Swagger documentation integrated
- _Security_  : **[Flask-JWT-extended](https://flask-jwt-extended.readthedocs.io/en/latest/)**
- _Emailing_  : **[Flask-email](https://pythonhosted.org/Flask-Mail/)**

#### Features
- login / register user ; 
- JSON web tokens (access and refresh) for security ; 
- confirm user by sending a confirmation link (protected) in an email ; 
- password forgotten by sending a link (protected) in an email with redirection to new password form ; 
- reset password from client interface or by sending an email with redirection to new password form... ; 
- documentation of all API endpoints with Swagger ;


------

## INSPIRATIONS / BENCHMARK

- [Dataiku](https://www.dataiku.com/), [Parabola](https://parabola.io/), but they are proprietary solutions (and too complex for our pruposes)... Not to mention they are very expensive...
- [Match ID](https://matchid-project.github.io/), but the backend doesn't resolve the "sharing" part with the level, and no BDD to back up recipes

