##
## Образ Docker для генератора документации Sphinx.
##
## See https://github.com/mekras/sphinx-doc
##

FROM debian:buster

## Основные пакеты Sphinx.
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    graphviz \
    python-pip \
    python-setuptools \
    python3-sphinx \
    python3-sphinx-rtd-theme \
    python3-sphinxcontrib.bibtex \
    python3-stemmer \
    sphinx-intl \
    && pip install --upgrade pip \
    && hash -r \
    && pip install --upgrade sphinx-autobuild \
    && rm -r /var/lib/apt/lists/*

## Отдельно ставим PlantUML, т. к. он тянет много зависимосетй.
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3-sphinxcontrib.plantuml \
    && rm -r /var/lib/apt/lists/*

## Пакеты для создания PDF.
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    lmodern \
    luatex \
    tex-common \
    texlive \
    texlive-binaries \
    texlive-extra-utils \
    texlive-fonts-extra \
    texlive-full \
    texlive-lang-cyrillic \
    texlive-latex-base \
    texlive-latex-base-doc \
    texlive-latex-extra \
    texlive-latex-recommended \
    texlive-luatex \
    texlive-pstricks \
    texlive-science \
    texlive-xetex \
    ttf-dejavu \
    && pip install --upgrade pip \
    && hash -r \
    && pip install --upgrade sphinx-autobuild \
    && rm -r /var/lib/apt/lists/*
