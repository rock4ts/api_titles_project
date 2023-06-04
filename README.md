# API Titles

## Описание проекта

Проект API Titles собирает отзывы пользователей на произведения. Сами произведения в  не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка».

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.
<br><br>


## Технологии

* Python 3.7
* Django 2.2.16
* Django Rest Framework 3.12.4
* Simple JWT 5.2.1
<br><br>


## Как запустить проект:

**Клонировать репозиторий и перейти в него в командной строке:**
```
git clone git@github.com:rock4ts/api_.git
```
```
cd api_titles/
```
​
**Создать и активировать виртуальное окружение:**
```
python3 -m venv venv
```
```
. venv/bin/activate
```

**Обновить pip и установить зависимости из файла requirements.txt:**
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```

**Сгенерировать Django SECRET_KEY:**
```
python manage.py shell
```

В запущенном интерактивном режиме Django:

```
from django.core.management.utils import get_random_secret_key
```
```
get_random_secret_key()
```

Полученный ключ передайте в переменную SECRET_KEY в файле api_titles/settings.py .

**Cоздать и выполнить миграции:**
```
python manage.py makemigrations
```
```
python manage.py migrate
```

**Наполнить проект данными:**

В директории '/api_titles_project/api_titles' содержится файл fixtures.json с тестовыми данными.
Для единовременного заполнения базы данных:
```
python manage.py loaddata fixtures.json
```

В качестве альтернативы в проект добавлен пользовательский скрипт поочерёдного заполнения таблиц для каждой модели проекта.
csv-файлы c данными содержаться в папке `/api_titles_project/api_titles/static/data/`.
Для запуска скрипта из текущей дериктории выполните команду:
```
python3 manage.py populate_reviews --path ./static/data/<csv_file_name>
```

**Запустить проект:**
```
python3 manage.py runserver
```
<br><br>


## Ресурсы API

- Ресурс auth: аутентификация.
- Ресурс users: пользователи.
- Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.
<br><br>


## Пользовательские роли и права доступа

* Аноним — может просматривать описания произведений, читать отзывы и комментарии.

* Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.

* Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.

* Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

* Суперюзер Django должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.
<br><br>


## Самостоятельная регистрация новых пользователей

1. Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт `/api/v1/auth/signup/`.
2. Сервис Titles отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
3. Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен).

В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом. 
После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполнить поля в своём профайле (описание полей — в документации).
<br><br>


## Создание пользователя администратором

1. Пользователей создаёт администратор — через админ-зону сайта или через POST-запрос на специальный эндпоинт `api/v1/users/` (описание полей запроса для этого случая есть в документации). При создании пользователя не предполагается автоматическая отправка письма пользователю с кодом подтверждения. 
2. После этого пользователь должен самостоятельно отправить свой email и username на эндпоинт `/api/v1/auth/confirmation_code/`, в ответ ему должно прийти письмо с кодом подтверждения.
3. Далее пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен), как и при самостоятельной регистрации.
<br><br>


## Документация, эндпоинты, запросы

Каждый ресурс описан в документации redoc: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, когда это необходимо.
Для просмотра документации перейдите по ссылке после запуска проекта:
```
http://127.0.0.1:8000/redoc/
```
<br><br>

