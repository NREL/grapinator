FROM python:3
USER root

ENV SERVICE_HOME /opt/gqlapi_service
ENV ORCL_BIN instantclient-basic-linux.x64-19.3.0.0.0dbru.zip
ENV LD_LIBRARY_PATH /opt/oracle/instantclient_19_3

# set local docker resources relative path
ENV DOCKER_RESOURCES docker/resources

# Set the working directory to SERVICE_HOME
WORKDIR $SERVICE_HOME

# copy service code to SERVICE_HOME
COPY $DOCKER_RESOURCES/gqlapi_service.sh \
$DOCKER_RESOURCES/$ORCL_BIN \
README.md \
requirements.txt \
setup.py $SERVICE_HOME/

COPY gqlapi/ $SERVICE_HOME/gqlapi 

# update and install requirements
RUN apt-get update && apt-get install -y libaio1 \
    && mkdir -p /opt/oracle \
    && (cd /opt/oracle;unzip $SERVICE_HOME/$ORCL_BIN) \
    && rm $SERVICE_HOME/$ORCL_BIN \
    && echo $LD_LIBRARY_PATH > /etc/ld.so.conf.d/oracle-instantclient.conf \
    && ldconfig \
    && pip install -r requirements.txt \
    && python setup.py develop 

EXPOSE 8443

ENTRYPOINT ["/bin/sh", "-c", "$SERVICE_HOME/gqlapi_service.sh"]

# for debugging only!
#ENTRYPOINT ["/bin/bash"]
