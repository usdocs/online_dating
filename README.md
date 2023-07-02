# online_dating
Тестовое задание
online_dating - бекэнд для сайта (приложения) знакомств.

## Технологический стек
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)

# Эндпоинты:

## 1. Создание пользователя   
Адрес http://158.160.49.4/api/clients/create/coordinates/
Метод POST
Для регистрации необходимы следующие данные:   
profile_picture 'Аватарка'
sex 'Пол'
first_name 'Имя'
last_name 'Фамилия'
email
username 'Никнейм'
password

При регистрации нового участника на аватарку накладывается водяной знак

Также для каждого пользователя нужно созадть "текущие координаты" Широту и долготу:
http://158.160.49.4/api/clients/create/coordinates/
Метод POST
Работает только для авторизованного пользователя.
Данные:
longitude
latitude

## 2. Авторизация и разлогинивание
Адрес http://158.160.49.4/api/clients/auth/login/
Метод POST
Данные:
email
password

Получаем токен. Этот токен надо будет передавать в заголовке каждого запроса, в поле Authorization. Перед самим токеном должно стоять ключевое слово Token

Адрес http://158.160.49.4/api/clients/auth/logout/
Метод POST

Удаляет токен авторизации. Работает только для авторизованного пользователя.

## 3. Получение данных об участнике
Работает только для авторизованного пользователя.
Адрес http://158.160.49.4/api/clients/{id}/ (http://158.160.49.4/api/clients/3/)
Метод GET

## 4. Оценивание участником другого участника:
Работает только для авторизованного пользователя.
Адрес http://158.160.49.4/api/clients/{id}/match
Метод POST

В случае, если возникает взаимная симпатия, то отправляются письма на почты участников: «Вы понравились <имя>! Почта участника: <почта>».       

## 5. Cписок участников:
Адрес http://158.160.49.4/api/list.
Метод GET

Реализована возможность фильтрации списка по полу, имени, фамилии и расстоянии до участника.

Фильтрация по расстоянию реализована 2-мя методами distance и distance2

Доступные значения:    
sex=(F,M) Фильтр по полу - Female, Male    
distance=<число>.    
first_name=<Имя>    
last_name=<Фамилия>
