##
## Образ Docker для генератора документации Sphinx.
##
## See https://github.com/mekras/sphinx-doc
##

FROM sphinxdoc/sphinx-latexpdf:8.2.3

RUN set -eux ;\
    mkdir --parents /usr/share/man/man1 ;\
    apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --assume-yes -f --no-install-recommends \
      plantuml \
      texlive-lang-cyrillic \
      fonts-dejavu \
    ;\
    rm -r /var/lib/apt/lists/* ;\
    rm --recursive --force /usr/share/man ;\
    pip install \
        sphinx-autobuild \
        sphinx-rtd-theme \
        sphinxcontrib-plantuml
