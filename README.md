# Web-сервис расписания электричек


## Содержание
* [Краткое описание](#краткое-описание)
* [Развертывание](#развертывание)
* [Настройка](#настройка)
* [Пример работы](#пример-работы)
  * [Страница авторизации](#Страница-авторизации)
  * [Поиск рейсов](#Поиск-рейсов)
  * [Результат-поиска](#Результат-поиска)
  * [Данные о рейсе](#Данные-о-рейсе)
* [Общая-схема-работы](#Общая-схема-работы)
* [Зависимости](#зависимости) 
* [Яндекс.API](#Яндекс.API)


## Краткое описание
Этот Web-сервис позволяет искать информацию о расписании электричек Москвы и Московской области.

С помощью API Яндекса также можно узнать ближайшие станции к пользователю.

## Развертывание
```
$ git clone https://github.com/JohnTer/train-schedule-server.git
$ cd train-schedule-server
$ python3 server.py
```

## Настройка
Файл настроек расположен в projsettings.py
```
YA_API_KEY # API ключ Яндекс
DBNAME # Имя базы данных с данными о расписании
DB_USER # Имя пользователя для подключение к БД
DB_PASSWORD # Имя пользователя для подключение к БД
DB_HOST # Адрес для подключение к БД

```

## Пример работы
### Страница авторизации

![login](https://user-images.githubusercontent.com/36763228/87179235-12640480-c2e7-11ea-966d-78220f16050b.png)

### Поиск рейсов

![search](https://user-images.githubusercontent.com/36763228/87179269-20198a00-c2e7-11ea-90d4-3d1bbf9b6a69.png)

### Результат поиска

![trainlist](https://user-images.githubusercontent.com/36763228/87179343-417a7600-c2e7-11ea-94a0-4f71cc48d5e8.png)


### Данные о рейсе

![train](https://user-images.githubusercontent.com/36763228/87179300-2f003c80-c2e7-11ea-9cb4-895a2b7adf03.png)

## Общая схема работы

![dia](https://user-images.githubusercontent.com/36763228/87179139-e9dc0a80-c2e6-11ea-8052-b980ae536fa0.png)


## Зависимости
Необходимые библиотеки для python:
+ Flask==1.1.1
+ Flask-Login==0.4.1
+ Flask-RESTful==0.3.7
+ Jinja2==2.10.1
+ lxml==4.4.1
+ psycopg2==2.7.7
+ requests==2.22.0
+ selenium==3.141.0

## Яндекс.API
Также сервис имеет функцию поиска ближайших станций к пользователю. В этом случае, с помощью специальной кнопки на сервер отправляется его геопозиция. Сервер возвращает первые пять станций, которые наиболее близко расположены к пользователю (с указанием расстояния в километрах), а также карту с указанием пользователя и найденных станций. Данный функционал использует API Яндекс.Карты и Яндекс.Электрички
