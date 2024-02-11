FROM python:3.11-slim

COPY model/ /home/model
COPY server/ /home/server
WORKDIR /home
RUN python -m pip install --upgrade pip setuptools;\
    python -m pip install -e model;\
    python -m pip install -e server

WORKDIR /home/server

EXPOSE 8081
CMD ["flask", "run", "-p", "8081"]
