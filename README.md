# test-o-parser
Тестовое задания на вакансию на POPSO.ru
### Описание
приложение с REST API для парсинга информации о товарах магазина по ссылке с сайта Ozon и сохранения полученных данных о товарах в базу данных. С оповещением о завершении парсинга через Telegram бота.
### Технологии
Python 3.9
Django 3.2.20
Django Rest Framework: 3.14.0
Celery: 5.3.1

### Запуск проекта 
git clone https://github.com/pro911pc/test-o-parser.git

cd test-o-parser/o_parser
```

Windows:

```
python -m venv venv

source venv/Scripts/activate
```

Mac, Linux:

```
python3 -m venv venv

. venv/bin/activate
```

Далее:

```
pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic

python manage.py runserver

Для работы celery нужен redis-server:


python -m celery -A o_parser worker -l info




```
```
### Автор
Углов Дмитрий
https://t.me/Duglov