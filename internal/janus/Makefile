all: rpm

rpm:
	docker build -t janus_fedora30 -f janus-fedora30.dockerfile  .
	docker run -i -v ${PWD}/built:/rpm janus_fedora30:latest /bin/bash -c "cp /root/rpmbuild/RPMS/x86_64/*.rpm /rpm"
