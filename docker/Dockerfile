# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *-------------------------------------------------------------------------------
# * For more information about the OpenAirInterface (OAI) Software Alliance:
# *      contact@openairinterface.org
# */
#---------------------------------------------------------------------
#
# Dockerfile for the Open-Air-Interface AMF service
#   Valid for Ubuntu-18.04 (bionic)
#
#---------------------------------------------------------------------

#---------------------------------------------------------------------
# BUILDER IMAGE
#---------------------------------------------------------------------

FROM ubuntu:18.04 AS vpp-upf-builder

ARG NEEDED_GIT_PROXY

LABEL name="upf" \
      version="u18" \
      description="Image for travelping upf based on VPP"

# Installing hyperscan library for upf plugin
RUN apt update && apt install git sudo wget make build-essential -y
RUN wget http://archive.ubuntu.com/ubuntu/pool/universe/h/hyperscan/libhyperscan4_4.7.0-1_amd64.deb \
    http://archive.ubuntu.com/ubuntu/pool/universe/h/hyperscan/libhyperscan-dev_4.7.0-1_amd64.deb
RUN dpkg -i *.deb

# Some GIT configuration commands quite useful
RUN /bin/bash -c "if [[ -v NEEDED_GIT_PROXY ]]; then git config --global http.proxy $NEEDED_GIT_PROXY; fi"
RUN git config --global https.postBuffer 123289600
RUN git config --global http.sslverify false

# Installing and configuring vpp
RUN git clone -b downstream https://github.com/travelping/vpp.git upf
COPY docker/patches patches/
RUN patch -p1 -d    upf < patches/werror_disable.patch 
RUN git clone https://github.com/travelping/upg-vpp.git
RUN mv upg-vpp/upf/ upf/src/plugins/ 
RUN patch -p1 -d upf < patches/0008-Follow-symlinks-while-checking-timestamps-during-bui.patch 
RUN patch -p1 -d upf < patches/0008-vlib-decrement-counters.patch 
RUN patch -p1 -d upf < patches/0009-sparse-vector-fix-leak.patch

RUN rm *.deb -r upg-vpp/
RUN touch /etc/apt/apt.conf.d/90forceyes
RUN echo  "APT::Get::Assume-Yes "true";" >> /etc/apt/apt.conf.d/90forceyes
RUN echo  "APT::Get::force-yes "true";" >> /etc/apt/apt.conf.d/90forceyes
RUN make install-dep build -C upf/
RUN make install-ext-dep build -C upf/

#---------------------------------------------------------------------
# TARGET IMAGE
#---------------------------------------------------------------------
FROM ubuntu:bionic as vpp_upg
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get upgrade --yes && DEBIAN_FRONTEND=noninteractive apt-get install --yes \
    net-tools \
    tshark \
    openssl \
    libhyperscan-dev \
  && rm -rf /var/lib/apt/lists/*


WORKDIR /openair-upf/bin/
COPY --from=vpp-upf-builder /upf/build-root/install-vpp_debug-native/vpp/bin/vpp .
COPY --from=vpp-upf-builder /upf/build-root/install-vpp_debug-native/vpp/bin/vpp .
COPY docker/configs .

WORKDIR /openair-upf/scripts
COPY docker/scripts .

WORKDIR /usr/lib/x86_64-linux-gnu/
COPY --from=vpp-upf-builder /upf/build-root/install-vpp_debug-native/vpp/lib/ .

RUN ldconfig

RUN groupadd vpp

WORKDIR /openair-upf/bin

