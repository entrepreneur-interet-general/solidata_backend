---
title : PRESENTATION
categories:
  - general
tags:
  - documentation
  - configuration
  - deployment
  - ecosystem
toc: true
toc_label: "contents"
toc_sticky: true
---

-----

{% include figure image_path="/static/logos/logo_solidata_15a-380x64.png" alt="solidata logo" %}

## SOLIDATA BACKEND

**Solidata** is a microservice (a REST API) for data management and authentication based on access and refresh JSON Web Tokens (JWT)


{% include figure image_path="/documentation/screenshots/endpoints_dataset_inputs.png" alt="solidata dsi" %}


- compatible with the **TADATA!** sofware suite ( [ApiViz](https://github.com/co-demos/apiviz-frontend) / [Solidata_frontend](https://github.com/entrepreneur-interet-general/solidata_frontend) / [Toktok](https://github.com/co-demos/toktok) / [OpenScraper](https://github.com/entrepreneur-interet-general/OpenScraper)  )

-------

## GOALS

- allow you to consume data from your own csv/xls files or external APIs ;
- consolidate your data : apply your own datamodel, simplify columns, apply metadatas, ... ; 
- share the consolidated datas on API endpoints with the level of openness you decide (opendata, commons, collective, private) ;
- manage all your data and your recipes by projects ;
- be able to manage projects by teams and share data/recipes/datamodels...

---------

## FEATURES 

Solidata includes "out-the-box" some classic features related to user authentication

### JWT (JSON Web Tokens) :

- access and refresh token for security over all the app
- RSA encryption (optionnal)
- RSA encryption : server can send to the client a RSA public key for encryption client-side
- RSA decryption : server can decode forms (login/register) encoded client-side with the RSA public key

### Users management :

- login / register user 
- anonymous login (optionnal) : sends a JWT for an anonymous use. Can be expected by server for routes with `@anonymous_required` decorator like `/login` or `/register`
- confirm email (optionnal in dev mode): confirm user by sending a confirmation link (protected) in an email 
- password forgotten by sending a link (protected) in an email with redirection to new password form 
- reset password from client interface (protected) ...

### Documentation 
	- on all API endpoints with Swagger (and some patience from the developer)

### Features TO DO  :
- user : 
	- edit user (working on)
	- edit email (protect email update)

------

## INSPIRATIONS / BENCHMARK

- [Dataiku](https://www.dataiku.com/), [Parabola](https://parabola.io/), but they are proprietary solutions (and too complex for our purposes)... Not to mention they are very expensive...
- [Match ID](https://matchid-project.github.io/), but the backend doesn't resolve the "sharing" part with levels as ["opendata", "commons", "collective", "private"], and no BDD to back up recipes