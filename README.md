# Образ Docker для генератора документации Sphinx

Рабочая папка Sphinx — `/opt/docs`.

Запуск сервера для разработки:

    sphinx-autobuild --poll -H 0.0.0.0 /opt/docs /var/www/html/pages
