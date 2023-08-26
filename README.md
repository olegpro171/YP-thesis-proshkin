# FoodGram Project

## Информация о проекте
Проект доступен по адресу: https://foodgram53.servebeer.com/

- Информация для отладки и проверки (раздеел будет удален):

    - Суперпользователь:
        - Username: `1`
        - E-mail: `aa@aa.aa`
        - Password: `1`


## Описание

Проект FoodGram - это онлайн платформа для создания, поиска и обмена кулинарными рецептами. Пользователи могут регистрироваться, создавать собственные рецепты, добавлять их в избранное и список покупок, а также делиться своими кулинарными шедеврами с другими участниками.

## Инструкция по запуску

Для запуска проекта на вашей локальной машине, выполните следующие шаги:

1. Установить Docker: https://docs.docker.com/engine/install/
    
    a. Для работы проекта на удаленном сервере также понадобится учетная запись Docker

2. Клонировать репозиторий проекта
```
git clone https://github.com/olegpro171/foodgram-project-react
cd foodgram-project-react/infra
```

3. Запустить compose
```
sudo docker compose up --build
```

Также предусмотрен запуск на удаленном сервере (опционально):

4. Сбилдить и загрузить на Dockerhub образы `frontend` и `backend`:

```
sudo docker login

sudo docker build -t <имя пользователя>/foodgram_frontend ../frontend
sudo docker build -t <имя пользователя>/foodgram_backend ../backend
```

5. Настроить файл `docker-compose-production.yml`: задать имя образов backend и frontend. Пример:

```
backend:
    ...
    image: docker_username/foodgram_backend:latest
    ...
```

6. Создать файл `.env` и настроить его в соответствии с `.env.example`

7. Копировать удобным способом файлы `docker-compose-production.yml`, `nginx.conf` и `.env` на удаленный сервер в директорию `<директория проета>/infra/`

8. Выполнить команду на удаленном сервере:

```
docker compose -f </путь/до/docker-compose-production.yml> up -d
```

## Примеры запросов


Примеры запросов, которые можно выполнить в приложении FoodGram:

Регистрация нового пользователя:


    POST /api/auth/users/
    Content-Type: json

    {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "securepassword"
    }


Авторизация пользователя:


    POST /api/auth/token/login/
    Content-Type: application/json

    {
        "email": "newuser@example.com",
        "password": "securepassword"
    }

Создание нового рецепта:

    POST /api/recipes/
    Authorization: Token yourAuthToken
    Content-Type: application/json

    {
        "name": "Delicious Pasta",
        "text": "A tasty pasta recipe...",
        "cooking_time": 30,
        "tags": [1, 2, 3],
        "ingredients": [
            {"id": 1, "amount": 200},
            {"id": 2, "amount": 100}
        ]
    }   

## Использованные технологии

Проект FoodGram использует следующие технологии:

- Django: веб-фреймворк для разработки бэкенда
- Django REST framework: инструмент для создания API
- PostgreSQL: база данных для хранения данных
- Docker: контейнеризация приложения
- Nginx: веб-сервер для обработки HTTP-запросов
- HTML/CSS/JavaScript: фронтенд приложения

## Автор

Проект FoodGram разработан в рамках программы Яндекс.Практикум. Разботчик: Олег Прошкин. 

Вы можете связаться со мной по адресу oleg.pro171@gmail.com.