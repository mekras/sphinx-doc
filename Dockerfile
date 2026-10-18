##
## Образ Docker для генератора документации Sphinx.
##
## See https://github.com/mekras/sphinx-doc
##

FROM sphinxdoc/sphinx-latexpdf:8.2.3@sha256:8fc7894c1961018ceaedf79d5dc3c4d74c1b0ea9c6a267ed65efa9596d3d17d0

RUN set -eux ;\
    mkdir --parents /usr/share/man/man1 ;\
    apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --assume-yes -f --no-install-recommends \
      plantuml \
      texlive-lang-cyrillic \
      fonts-dejavu \
    ;\
    rm -r /var/lib/apt/lists/* ;\
    rm --recursive --force /usr/share/man

COPY requirements.txt /tmp/sphinx-requirements.txt

RUN pip install --no-cache-dir --requirement /tmp/sphinx-requirements.txt \
    && pip check \
    && rm /tmp/sphinx-requirements.txt
