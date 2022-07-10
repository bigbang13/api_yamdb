# api_yamdb

### API YAMDB
API для проекта YAMDB. Проект YAMDB собирает отзывы пользователей о различных произведениях и на основании их оценок выставляет средний балл.

## Как запустить проект:

1. Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:bigbang13/api_yamdb.git
cd api_YAMDB
```
2. Cоздать и активировать виртуальное окружение:
```
python -m venv venv
source venv/bin/activate
```
3. Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
4. Выполнить миграции:
```
python manage.py migrate
```
5. Запустить проект:
```
python manage.py runserver
```
Документация после запуска доступна по адресу ```http://127.0.0.1:8000/redoc/```.

В проекте реализована эмуляция почтового сервера, письма сохраняются в папке /sent_emails в головной директории проекта.

## Технологии
- Python 3.7
- Django 2.2.16
- Django REST Framework 3.12.4

### Авторы

_Рябов В.С._
_email: ryabov.v.s@yandex.ru_
_github: https://github.com/bigbang13_

_Пацей П._
_github: https://github.com/PavelPatsey_

_Комиссаров А._
_github: https://github.com/mrsalbey_
