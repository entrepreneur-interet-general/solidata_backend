---
title : HOW TO CONFIGURE YOUR APIVIZ INSTANCE
categories:
  - guide
tags:
  - documentation
  - configuration
  - backoffice
toc: true
toc_label: " contents"
toc_sticky: true
---

{% include figure image_path="/documentation/screenshots/backoffice-sonum-02.png" alt="admin view" %}


-----
## Create an admin user

1. register an user (user data will stored and managed in TokTok, so you'd need to install Toktok locally) ;
1. make this user an `admin` (in TokTok) ;

## Go to the back office

1. log in (`admin` link in the default footer, `/login` route by default) ;
1. go to the `/backoffice` route by clicking on the button `back office`;
1. set up your ApiViz configuration : 
    
    - set up the global variables ; 
    - set up your data endpoints ; 
    - set up your authentication endpoints ; 
    - set up your routes (pages must point out to html contents, f.e. on Github) ; 
    - set up the styles ;
    - set up your navbar ; 
    - set up your footer ;

1. save your configuration ;

## (optional) redeploy

1. deploy (if not done already) and enjoy ;

More detailed configuration documentation on its way...
