FROM ubuntu:18.04
MAINTAINER Leonardo Edgar

ARG USER
ARG GROUP
ARG UID
ARG GID

# Install core linux tools
RUN apt-get update && apt-get install -y --no-install-recommends \
	apt-utils lsb-release sudo unzip wget ssh vim curl ca-certificates gnupg git \
	&& rm -rf /var/lib/apt/lists/* 

# Install python
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y python3-dev python3-opencv \ 
	python3-pytest python3-pytest-mock python3-pytest-cov make python3-yaml python3-pip \
	python3-setuptools --no-install-recommends \ 
	&& rm -rf /var/lib/apt/lists/* 

# Install dev dependencies
RUN pip3 install coveralls

# User and permissions
ARG HOME=/home/${USER}
RUN mkdir -p /etc/sudoers.d \
    && groupadd -g ${GID} ${GROUP} \
    && useradd -d ${HOME} -u ${UID} -g ${GID} -m -s /bin/bash ${USER} \
    && echo "${USER} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/sudoers_${USER}
USER ${USER}
RUN sudo usermod -a -G video ${USER}

WORKDIR ${HOME}
