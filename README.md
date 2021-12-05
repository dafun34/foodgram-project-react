![example workflow](https://github.com/dafun34/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# Foodgram
## Краткое описание
Foodgram - сервис для обмена рецептами.  
Каждый жедающий может ознакомиться с доступными рецептами, отфильтровать весь список по доступным тэгам, посмотреть выбранный рецепт, зарегистрироваться и получить доступ к расширеным возможностям.  

Аутентифицированный пользователь может:
*  Писать и редактировать свои рецепты.
*  Подписываться на других авторов.
* Добавлять рецепты в избранное 
* Добавлять рецепты в корзину
* Скачивать список с нужным количеством ингредиентов из добавленных в корзину рецептов
* Менять свой пароль  

## Технологии
* Python 3
* Django 3.2
* PostgreSQL
* Django REST Framework
* Joser
* Docker
* Nginx
* Яндекс.Облако(ubuntu 20.04)

## Установка

Для начала следует [установить Docker](https://docs.docker.com/engine/install/) на вашу ОС.  

Клонируйте репозиторий: 
    
    https://github.com/dafun34/foodgram-project-react.git
Перейдите в папку *infra* из корневой директории:  
    
    cd .\infra\

Из этой папки запустите сборку контейнеров:  

    docker-compose up -d --build
    
После упешной сборки контейнеров создайте и примените миграции при помощи:  
    
    docker-compose exec app python manage.py makemigrations --noinput
    docker-compose exec app python manage.py migrate --noinput

Создайте "Суперюзера"(потребуется придумать логин и пароль):  

    docker-compose exec app python manage.py createsuperuser

Соберите всю статику:  

    docker-compose exec app python manage.py collectstatic --no-input
## Вход
Сервис будет доступен по адресу:

    http://localhost/

Страница администратора будет доступна по адресу:

    http://localhost/admin/

## Документация
доступна по:

    http://localhost/api/docs/
