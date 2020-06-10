# Образ Docker для генератора документации Sphinx

Основывается на [sphinxdoc/sphinx-latexpdf](https://hub.docker.com/r/sphinxdoc/sphinx-latexpdf) и дополнительно
включает:

- поддержку русского языка;
- поддержку [PlantUML](https://plantuml.com/ru/) ([sphinxcontrib-plantuml](https://github.com/sphinx-contrib/plantuml));
- тему оформления [Read The Dics](https://sphinx-rtd-theme.readthedocs.io/en/stable/).

Рабочая папка Sphinx — `/docs`.

Запуск сервера для разработки:

    sphinx-autobuild --poll -H 0.0.0.0 /docs /var/www/html/pages
