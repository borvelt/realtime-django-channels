# Chat app with django-channels

*[djago channels](https://channels.readthedocs.io/en/latest/) help you to have socket programming experince with django routers, it's incredible, isn't it?*

First of all you should know that this project is a light sample chat application, but it not mean that codes are ugly or experimental.

## Installation

Make sure your python version is 3 or later. Clone or download repository and then:

```bash
# bash
virtualenv .env
source .env/bin/activate
```

Now install packages.

```bash
# bash
$ pip install -r requirements.txt
```

Install [redis server](https://redis.io/download) or some thing like redis(if your not using redis or use on different port see `CHANNEL_LAYERS` in `chatApp/settings.py` )

Database Migration:

```bash 
$ python manage.py migrate
```

You should serve websocket part of your project with [daphne](https://github.com/django/daphne), just like this:

```bash
$ daphne chatApp.asgi:channel_layer -p 8000 -b localhost -v2
```

This command will run websocket interface of your project with `daphne`.
You should handle HTTP requests, so simply run this command:

```bash 
$ python manage.py runworker -v2
```

## Usage

Application just work in `/chat` url that this url need authentication, create superuser with `manage.py` interface.

## Test

This project doesn't have any unit tests, Please help me.

## License

*MIT*
