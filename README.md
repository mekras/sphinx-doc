# Образ Docker для генератора документации Sphinx

Основывается на [sphinxdoc/sphinx-latexpdf](https://hub.docker.com/r/sphinxdoc/sphinx-latexpdf)
и дополнительно включает:

- поддержку русского языка;
- [sphinx-autobuild](https://github.com/executablebooks/sphinx-autobuild);  
- поддержку [PlantUML](https://plantuml.com/ru/) ([sphinxcontrib-plantuml](https://github.com/sphinx-contrib/plantuml));
- тему оформления [Read The Docs](https://sphinx-rtd-theme.readthedocs.io/en/stable/).

Рабочая папка Sphinx — `/docs`.

Запуск сервера для разработки:

    docker run \
      -v /path/to/src:/docs \
      --rm -p 8000:8000 \
      -it mekras/sphinx-doc:latest \
      sphinx-autobuild --host 0.0.0.0 /docs /var/www/html/pages

Здесь:

- `/path/to/src` — путь к исходным файлам вашей документации;
- `-p 8000:8000` — первое число (**8000**:8000) задаёт порт для подключения к веб-серверу с машины разработчика.

После этого веб-сервер будет доступен по адресу `http://localhost:8000`.
