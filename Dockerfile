##
## Образ Docker для генератора документации Sphinx.
##
## See https://github.com/mekras/sphinx-doc
##

FROM sphinxdoc/sphinx-latexpdf

### Основные пакеты Sphinx.
#RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
#    python-pip \
#    python-setuptools \
#    python3-sphinxcontrib.bibtex \
#    python3-stemmer \
#    sphinx-intl \
#    && pip install --upgrade pip \
#    && hash -r \
#    && pip install --upgrade sphinx-autobuild \
#    && rm -r /var/lib/apt/lists/*

RUN set -eux; \
    mkdir --parents /usr/share/man/man1; \
    apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --assume-yes -f --no-install-recommends \
    plantuml \
    texlive-lang-cyrillic \
    && rm -r /var/lib/apt/lists/*; \
    rm --recursive --force /usr/share/man; \
    pip install \
        sphinxcontrib-plantuml \
        sphinx-rtd-theme

## Пакеты для создания PDF.
#RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
#    lmodern \
#    luatex \
#    tex-common \
#    texlive \
#    texlive-binaries \
#    texlive-extra-utils \
#    texlive-full \
#    texlive-latex-base \
#    texlive-latex-base-doc \
#    texlive-pstricks \
#    texlive-science \
#    ttf-dejavu \
#    && rm -r /var/lib/apt/lists/*
