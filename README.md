# Backend и бот для игры "Cookie Clicker"

### Запуск
1. Скопировать `.env.example` как `.env` и заполнить
2. Запустить `docker compose up -d`
3. Войти в контейнер `docker exec -it backend /bin/bash`, создать админа `python3 manage.py createsuperuser`.

- **АДМИНКА** на /admin
- **OPENAPI** на /api/docs

### Авторизация
Для авторизации в WebApp необходимо получить JWT токен в обмен на WebApp.initData на эндпоинте /api/authorization/web-app.

### Задачи (на подписку)
- Старт выполнения задания идет на эндпоинте /api/v1/user-tasks/{user_tg_id}/start-completion/{task_id}.
- После этого у юзера в течении 5 минут есть возможность подписаться. Проверка со стороны бэкенда идет синхронно вместе с запросом на эндпоинт получения заданий.
