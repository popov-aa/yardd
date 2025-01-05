from steamcmd/steamcmd:ubuntu-24

RUN apt -y update && apt install -y python3

ENV SERVER_IDENTITY=my_server_identity

ADD run.py /run.py

ENTRYPOINT ["/usr/bin/python3", "/run.py"]
