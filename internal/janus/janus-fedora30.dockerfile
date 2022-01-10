FROM fedora:30
RUN dnf install -y make wget redhat-rpm-config rpm-build systemd-rpm-macros git gcc

ENV RPMBUILDPATH /root/rpmbuild
ENV GOROOT /root/bin/go
ENV GOPATH /root/go

RUN mkdir -p ${GOROOT}
RUN mkdir -p ${GOPATH}/src

WORKDIR /root/bin
RUN wget https://dl.google.com/go/go1.16.2.linux-amd64.tar.gz
RUN tar zxvf go1.16.2.linux-amd64.tar.gz
ENV PATH=${GOROOT}/bin:$PATH

RUN wget https://nodejs.org/dist/v16.13.0/node-v16.13.0-linux-x64.tar.xz
RUN tar xvf node-v16.13.0-linux-x64.tar.xz
ENV PATH=/root/bin/node-v16.13.0-linux-x64/bin:$PATH

RUN mkdir -p ${RPMBUILDPATH}/SPECS
RUN mkdir -p ${RPMBUILDPATH}/SOURCES
RUN mkdir -p ${RPMBUILDPATH}/BUILD
RUN mkdir -p ${RPMBUILDPATH}/BUILDROOT
RUN mkdir -p ${RPMBUILDPATH}/RPMS
RUN mkdir -p ${RPMBUILDPATH}/SRPMS

ADD janus ${RPMBUILDPATH}/BUILD/janus
ADD janus.service ${RPMBUILDPATH}/BUILD/janus
ADD janus.spec ${RPMBUILDPATH}/SPECS/

WORKDIR ${RPMBUILDPATH}

RUN env

RUN rpmbuild -ba ${RPMBUILDPATH}/SPECS/janus.spec
RUN find ${RPMBUILDPATH}/RPMS/ -name '*.rpm' -exec chmod 666 '{}' \;
