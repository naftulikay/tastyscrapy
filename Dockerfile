FROM centos:7

RUN yum install -y epel-release >/dev/null

RUN yum install -y python34 python34-devel openssl-devel libffi-devel \
        libxslt-devel libxml2-devel make gcc >/dev/null

WORKDIR /srv/

ENV LANG=en_US.UTF-8

# add required dingos
ADD buildout.cfg bootstrap.py setup.py /srv/

# run buildout first so it warms the cache
RUN python3.4 bootstrap.py
RUN mkdir -p src/tastyscrapy && bin/buildout

# add source files
ADD src/ /srv/src/

RUN useradd -u 1000 -M -d /srv tastyscrapy && \
    chown -R tastyscrapy:tastyscrapy /srv

# drop privileges
USER tastyscrapy

# run buildout
RUN bin/buildout

ENTRYPOINT ["bin/scrapy"]
