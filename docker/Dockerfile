FROM ubuntu:18.04
LABEL name="upf" \
      version="u18" \
      description="Image for travelping upf based on VPP"

# Installing hyperscan library for upf plugin
#RUN apt-get update --fix-missing
RUN apt-get update
RUN apt-get install git tree sudo iptables wget tcpdump iproute2 python3 nano vim net-tools iputils-ping make build-essential htop python3 -y
RUN wget http://archive.ubuntu.com/ubuntu/pool/universe/h/hyperscan/libhyperscan4_4.7.0-1_amd64.deb \
    http://archive.ubuntu.com/ubuntu/pool/universe/h/hyperscan/libhyperscan-dev_4.7.0-1_amd64.deb
RUN dpkg -i *.deb

# Installing and configuring vpp
RUN git clone -b downstream https://github.com/travelping/vpp.git upf
COPY patches patches/
RUN patch -p1 -d    upf < patches/werror_disable.patch 
RUN git clone https://github.com/travelping/upg-vpp.git
RUN mv upg-vpp/upf/ upf/src/plugins/
#RUN patch -p1 -d upf < patches/0001-CI-and-build-infrastructure-adjustments.patch 
#RUN patch -p1 -d upf < patches/0002-Only-install-hyperscan-on-amd64.patch 
#RUN patch -p1 -d upf < patches/0003-Fix-bad-format_time_float-usage.patch 
#RUN patch -p1 -d upf < patches/0004-TEMP-Increase-reassembly-limit.patch 
#RUN patch -p1 -d upf < patches/0005-Bump-scapy-to-v2.4.4.patch 
#RUN patch -p1 -d upf < patches/0006-Add-downstream-marker.patch 
#RUN patch -p1 -d upf < patches/0007-ethernet-fix-Ethernet-DMAC-checks.patch 
RUN patch -p1 -d upf < patches/0008-Follow-symlinks-while-checking-timestamps-during-bui.patch 
RUN patch -p1 -d upf < patches/0008-vlib-decrement-counters.patch 
RUN patch -p1 -d upf < patches/0009-sparse-vector-fix-leak.patch
RUN patch -p1 -d upf < patches/00010-session_establishment_node_id.patch

RUN rm *.deb -r upg-vpp/
RUN touch /etc/apt/apt.conf.d/90forceyes
RUN echo  "APT::Get::Assume-Yes "true";" >> /etc/apt/apt.conf.d/90forceyes
RUN echo  "APT::Get::force-yes "true";" >> /etc/apt/apt.conf.d/90forceyes
RUN make install-dep build -C upf/
RUN make install-ext-dep build -C upf/
RUN groupadd vpp
#RUN mv upf/init.conf upf/init.conf.bkp
RUN touch upf/init.conf
COPY scripts scripts/
COPY configs configs/
COPY configs/init.conf.two_sgi upf/init.conf
COPY configs/run.sh /upf
COPY configs/startup_debug.conf /upf

# Installing go 1.13 for pfcp session injector
#RUN wget https://dl.google.com/go/go1.13.3.linux-amd64.tar.gz && tar -xvf go1.13.3.linux-amd64.tar.gz && mv go /usr/local
#ENV GOROOT=/usr/local/go
#RUN mkdir goproject
#ENV GOPATH=/goproject
#ENV PATH=$GOPATH/bin:$GOROOT/bin:$PATH

# Installing pfcp session injector
#RUN git clone https://github.com/fdangtran/pfcp-kitchen-sink.git
#RUN cd pfcp-kitchen-sink/ && go get  github.com/alvaroloes/enumer && go generate ./pkg/pfcp && go build -o pfcpclient cmd/pfcpclient/main.go
#RUN apt-get install python3-pip
#RUN pip3 install scapy
#COPY configs/sessions.yaml /pfcp-kitchen-sink/examples/session.yaml

# ENTRYPOINT ["./scripts/rc.local"]


# docker build -t vpp_upg:u18 docker/
# docker run  --privileged -ti vpp_upg:u18
# docker exec -it 2a9f009a5af9 /bin/bash
# ./scripts/rc.local
# ./pfcpclient -r 172.21.16.2:8805 -s examples/sessions.yaml i

ENTRYPOINT ./scripts/rc.local
