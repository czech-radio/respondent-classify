# service

This is a REST *service* build on top of Flask WSGI framework.

## Installation

### Production

&hellip;

### Development

Create and activate virtual environment before installation.

For development install the package development dependencies with command bellow.

```shell
python -m pip install -r requirements.txt
```

Then install package itself in editable mode.

```shell
python -m pip install -e .
```

TODO Explain enviroment variables used with Flask.

```shell
FLASK_DEBUG=True
```

Run the server with debugging turned on.

```shell
flask run -p 8081
```
