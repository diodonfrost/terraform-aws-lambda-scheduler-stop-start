FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    acl \
    ansible \
    curl \
    git \
    gnupg \
    iproute2 \
    iputils-ping \
    jq \
    less \
    libssl-dev \
    lsb-release \
    make \
    nano \
    openssh-client \
    procps \
    python3 \
    python3-pip \
    python3-venv \
    sudo \
    unzip \
    vim \
    wget \
    zip \
    zsh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN ansible-galaxy role install diodonfrost.ohmyzsh && \
    ansible-pull -U https://github.com/diodonfrost/ansible-role-ohmyzsh tests/test.yml -e "ohmyzsh_theme=powerlevel10k/powerlevel10k" -e '{"ohmyzsh_users": [vscode]}'

RUN ansible-galaxy role install diodonfrost.p10k && \
    ansible-pull -U https://github.com/diodonfrost/ansible-role-p10k tests/test.yml -e "zsh_plugin=ohmyzsh" -e '{"p10k_users": [vscode]}'
