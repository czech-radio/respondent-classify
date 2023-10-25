# Labeler Service

This is a *labeler service* build on Flask WSGI framework.

## Installation

### Production

&hellip;

### Development

**Create and activate virtual environment before installation!**

For development install package dependencies with command bellow.

```shell
pip install -r requirements.txt
```

Install package in editable mode.

```shell
pip install -e .
```

TODO Explain enviroment variables used with Flask.

```shell
FLASK_DEBUG=True
```

Run the server with debug mode on.

1. Call the Flask

    ```shell
    flask --app server run -p 8081 (obsolete?)
    ```

2. Call the console application defined in `setup.py`.

    ```shell
    labeler-server
    ```
