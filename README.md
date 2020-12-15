# SEQTOOLS in Flask

## Getting started

Get set up locally in two steps:

### Environment Variables

Replace the values in **.env.example** with your values and rename this file to **.env**:

* `FLASK_APP`: Entry point of your application; should be `wsgi.py`.
* `FLASK_ENV`: The environment in which to run your application; either `development` or `production`.
* `SECRET_KEY`: Randomly generated string of characters used to encrypt your app's data.


*Remember never to commit secrets saved in .env files to Github.*

### Installation
Get up and running with `make deploy`:

```shell
$ git clone https://github.com/polentozer/seqflask.git
$ cd seqflask
$ make deploy
```
