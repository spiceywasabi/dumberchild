FROM alpine:latest

RUN apk update && apk --no-cache add zip unzip python3 python3-dev py3-setuptools py3-pip wget bash
# oof, once discord.py bug is fixed we can remove this
RUN apk --no-cache add alpine-sdk
# continue as normal below
RUN pip3 install --upgrade pip && pip3 install nextcord requests
RUN wget https://github.com/weddige/pyaiml3/archive/refs/heads/master.zip -O pythonaiml.zip \
  && unzip pythonaiml.zip && cd pyaiml3-master && python3 setup.py install

COPY entrypoint.sh /

WORKDIR /opt/
COPY dumberchild.py /opt/
COPY standard.zip /opt/

RUN chmod +x /opt/*.py /*.sh && unzip /opt/standard.zip -d /opt/

ENV BOTINCONTAINER 1

ENTRYPOINT ["/entrypoint.sh"]
