# Образ Docker для генератора документации Sphinx

Проект предоставляет авторам документации готовую среду Sphinx в Docker, чтобы не приходилось вручную устанавливать и настраивать Sphinx, LaTeX, поддержку русского языка и расширений. Результат — образ Docker и шаблон проекта для сборки HTML/PDF и локального предпросмотра документации.

Основывается на [sphinxdoc/sphinx-latexpdf](https://hub.docker.com/r/sphinxdoc/sphinx-latexpdf)
и дополнительно включает:

- поддержку русского языка;
- [sphinx-autobuild](https://github.com/executablebooks/sphinx-autobuild);  
- поддержку [PlantUML](https://plantuml.com/ru/)
  ([sphinxcontrib-plantuml](https://github.com/sphinx-contrib/plantuml));
- тему оформления [Read The Docs](https://sphinx-rtd-theme.readthedocs.io/en/stable/).

Рабочая папка Sphinx — `/docs`.

## Что потребуется

Для запуска образа нужен работающий Docker. Для команд шаблона также нужны GNU Make и стандартные средства GNU/Linux.

## Новый проект документации

Из корня этого репозитория скопируйте шаблон в отдельный каталог:

```bash
cp -R project-template ../my-docs
cd ../my-docs
```

Замените `my-docs` на имя своего проекта.

В файле `src/pages/conf.py` укажите название проекта, авторов и версию документации. Начальную страницу редактируйте в `src/pages/index.rst`. Остальные страницы добавляйте в `src/pages/` и включайте в оглавление начальной страницы.

### Сборка HTML и PDF

Выполните из каталога нового проекта:

```bash
make all
```

HTML будет находиться в `htdocs/index.html`, PDF — в `htdocs/document.pdf`.

Перед сборкой содержимое `htdocs` очищается, кроме файлов `.gitignore` и `robots.txt`. Храните исходные материалы за пределами этого каталога.

### Предпросмотр

Запустите сервер:

```bash
make start-server
```

Откройте `http://localhost:8000`. При сохранении исходных файлов сервер пересобирает документацию и обновляет страницу в браузере. Для остановки нажмите `Ctrl+C`.

## Запуск образа напрямую

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
