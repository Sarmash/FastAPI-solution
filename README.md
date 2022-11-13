# Проектная работа 5 спринта

### Описание:
Асинхронный API для кинотеатра

### О проекте:
В данной версии сервиса пользователи могут получить информацию о кинопроизведениях: название, описание, жанр или жанры, 
к которым относится произведение, список актеров, принимающих участие в фильме, режиссера, сценаристов. В разделе с жарнрами
можно увидеть популярные фильмы в этом жанре, а также в разделе с персонами можно найти информацию по конкретной персоне.
Код сервиса покрыт тестами.
#### Доступ к конкретному фильму осуществляется при помощи jwt и сервиса авторизации:
https://github.com/Woodsst/Auth_sprint_1
Пользователь может иметь 3 варианта роли:

- All - не зарегестрированный пользователь
- User - зарегистрированный пользователь
- Subscriber - пользователь с оплаченной подпиской

Фильмы имеют категорию доступа и перед получением данных фильма, сервис проверяет уровень доступа пользователя,
если пользователь не имеет необходимого уровня доступа, данные ему не показываются.
В случае если jwt пользователя истек, подразумевается, что фронт перенаправляет пользователя в Auth сервис для обновления токена.

endpoint : https://github.com/Sarmash/FastAPI-solution/blob/master/fastapi-solution/src/api/v1/films.py#L29

### Технологии:
- Код приложения написан на Python + FastAPI
- Приложение запускается под управлением сервера ASGI(uvicorn)
- В качестве хранилища используется ElasticSearch
- Для кеширования данных используется Redis Cluster.
- Все компоненты системы запускаются через Docker.
- Взаимодействие с пользователем настроено через Nginx,
он находится в репозитории с [ETL](https://github.com/Woodsst/new_admin_panel_sprint_3)
и запускается автоматически при запуске контейнеров.
- Код покрыт тестами, использована библиотека Pytest

**Ссылка на репозитарий [FastAPI-solution](https://github.com/Sarmash/FastAPI-solution).**

**Ссылка на репозитарий [ETL](https://github.com/Woodsst/new_admin_panel_sprint_3).**

### Чтобы развернуть проект локально необходимо:
* Примечание: Необходимо запускать сервисы в опредленной последовательности:
сначала [FastAPI](https://github.com/Sarmash/FastAPI-solution), потом [ETL](https://github.com/Woodsst/new_admin_panel_sprint_3)
1. Создать сеть для связи между контейнерами:
   ```commandline
    docker network create api_network
   ```
2. Склонировать репозитрий **[FastAPI-solution](https://github.com/Sarmash/FastAPI-solution)**:
   ```commandline
   git clone git@github.com:Sarmash/FastAPI-solution.git
   ```
3. В репозитарии **[FastAPI-solution](https://github.com/Sarmash/FastAPI-solution)** запустить сборку контейнеров:
   ```commandline
    docker compose up --build
   ```
4. Склонировать репозитрий **[ETL](https://github.com/Woodsst/new_admin_panel_sprint_3)**:
   ```commandline
   git clone git@github.com:Woodsst/new_admin_panel_sprint_3.git
   ```
5. В репозитарии **[ETL](https://github.com/Woodsst/new_admin_panel_sprint_3)** запустить сборку контейнеров:
   ```commandline
    docker compose up --build
   ```
6. Осуществить вход в **[swagger](http://localhost/api/openapi)**.

### Основные URL:

1. Главная страница. На ней выводятся популярные фильмы.

```
http://localhost/api/v1/films?sort=-imdb_rating
```
2. Список жанров.
```
http://localhost/api/v1/genres/
```
3. Страница персонажа, где uuid - UUID персонажа
```
http://localhost/api/v1/persons/<uuid:UUID>/
```
4. Страница жанра, где uuid - UUID жанра
```
http://localhost/api/v1/genres/<uuid:UUID>/
```
5. Страница фильма, где uuid - UUID фильма
```
http://localhost/api/v1/films/<uuid:UUID>/
```
6. Поиск по фильмам.
```
http://localhost/api/v1/films/search/
```
7. Поиск по персонам.
```
http://localhost/api/v1/persons/search/
```
8. Фильмы по персоне, где uuid - UUID персонажа
```
http://localhost/api/v1/persons/<uuid:UUID>/film/
```
9. Документация к API
```
http://localhost/api/openapi/
```
### Авторы проекта

* [**Николай Филиппов - тимлид проекта**](https://github.com/Sarmash)
* [**Шебуняев Иван**](https://github.com/Woodsst)
* [**Останин Алексей**](https://github.com/A1exit)
