# Labeler Service

This is a *labeler service* build on Flask WSGI framework.

## Installation

### Production

&hellip;

### Development

**Create and activate virtual environment before installation!**

```shell
pip install -e .[dev] 
```

TODO Explain enviroment variables used with Flask.

```shell
FLASK_DEBUG=True
```

Run the server with debug mode on.

1. Call the Flask

    ```shell
    flask --app server run -p 8081
    ```

2. Call the script (module).

    ```shell
    python server.py
    ```

3. Call the console application defined in `setup.py`.

    ```shell
    
    ```