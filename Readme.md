<h1 align="center">Приложение "Электронная библиотека"</h1>
<p align="center">
<img src="https://img.shields.io/badge/created_by-flask-green">
<img src="https://img.shields.io/badge/based%20on%20postgresql-8A2BE2">
<img src="https://img.shields.io/badge/served_by-gunicorn-blue">
<img src="https://img.shields.io/badge/deploy by-docker-yellow">
</p>

<p align="center">
<img src="readme_pic.png" width="70%">
</p>

<h2 align="center">Описание проекта</h2>
<p>Это pet-проект имитирующий электронную библиотеку книг, с возможностью создания, редактирования и скачивания
файлов книг, для последующего их прочтения. Так же в проекте реализована авторизация пользователей с разграничением прав.
В проекте использованы фикстуры данных для быстрого развертывания и демонстрации возможностей.
По умолчанию добавлен супер пользователь с логином "admin", пароль "admin".
</p>

<h2 align="center">Технологии проекта</h2>
Проект выполнен с использованием следующих библиотек и баз данных:

- Flask
- docker compose
- gunicorn
- Postgresql

<h2 align="center">Развернуть проект локально</h2>
- скачиваем проект с репозитория командой git clone https://github.com/Artromterra/flask-project.git
- собираем, запускаем проект командой `docker compose build`, `docker compose up -d`
- приложение будет доступно по адресу http://localhost:8000
- для запуска тестов необходимо в файле "main/__init__.py" раскомментировать строку с тест конфигом,
и из директории test запустить команду в консоли pytest -v test.py
