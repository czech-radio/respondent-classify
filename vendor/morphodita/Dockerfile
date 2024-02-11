FROM alpine

COPY build.sh .

RUN apk add --no-cache git;\
    apk add --no-cache openssh;\
    apk add --no-cache bash;\
    apk add --no-cache make;\
    apk add --no-cache curl;\
    apk add --no-cache g++;\
    bash build.sh

COPY run.sh .

CMD ["bash", "run.sh", "3000"]
