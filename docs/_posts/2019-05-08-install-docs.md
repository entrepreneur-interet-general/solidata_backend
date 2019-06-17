---
title : INSTALL THE DOCS WITH JEKYLL
categories:
  - guide
tags:
  - documentation
  - configuration
  - installation
  - Jekyll
---

--------

The documentation is produced with : 

  - **[Github pages](https://pages.github.com/)**
  - **[Jekyll](https://jekyllrb.com/)**
  - **[Minimal Mistakes template](https://mmistakes.github.io/minimal-mistakes/docs/quick-start-guide/)**

--------

#### For a local deployment of the documentation project (Jekyll + MMistakes template)

--------

- Install ruby, Jekyll

```bash
brew install ruby
gem install jekyll
```

- From your repo's root go to the `/docs` folder

```sh 
cd /docs
```

- Install setup (given the `Gemfile`, `Gemfile.lock` and `_config.yml` files)

```bash
gem install bundler
bundle
bundle install
bundle update
```


- Launch Jekyll server 

```bash
jekyll serve

# or if you want to run the docs server on another port
jekyll serve --port=4010
```

... then check in your browser : 

[`127.0.0.1:4010`](127.0.0.1:4010) 

