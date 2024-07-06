Приложение для бронирования комнат в отеле
### Требования:

- ~~Для комнат должны быть поля: номер/название, стоимость за сутки, количество мест.~~
- ~~Пользователи должны уметь фильтровать и сортировать комнаты по цене, по количеству мест.~~
- ~~Пользователи должны уметь искать свободные комнаты в заданном временном интервале.~~
- ~~Пользователи должны уметь забронировать свободную комнату.~~
- ~~Суперюзер должен уметь добавлять/удалять/редактировать комнаты и редактировать записи о бронях через админ панель Django.~~
- ~~Брони могут быть отменены как самим юзером, так и суперюзером.~~
- ~~Пользователи должны уметь регистрироваться и авторизовываться (логиниться).~~
- ~~Чтобы забронировать комнату пользователи должны быть авторизованными.~~
- ~~Просматривать комнаты можно без логина.~~
- ~~Авторизованные пользователи должны видеть свои брони.~~
### Стек:
- Django;
- DRF;
- СУБД предпочтительно PostgreSQL, но не обязательно. Главное не SQLite;
- При необходимости можно добавлять другие библиотеки.
#### Приветствуется:
- ~~Автотесты;~~
- Аннотации типов;
- ~~Линтер;~~ использовал flake8
- ~~Автоформатирование кода;~~ Использовал fback и isort
- ~~Документация к API;~~
- ~~Инструкция по запуску приложения.~~

-------------------------------
### Инструкция по запуску Django приложения

#### 1. Клонирование репозитория
```bash
git clone https://github.com/matthew-mal/hotel_booking.git
cd booking
```

#### 2. Настройка виртуального окружения
```bash
python -m venv .venv
source .venv/bin/activate  # Для Linux/Mac
.\.venv\Scripts\activate  # Для Windows
```

#### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

#### 4. Настройка базы данных
```bash
python manage.py migrate
```

#### 5. Создание суперпользователя
```bash
python manage.py createsuperuser
```

#### 6. Запуск сервера разработки
```bash
python manage.py runserver
```

Откройте браузер и перейдите по адресу `http://127.0.0.1:8000/` для доступа к приложению.
Админ-панель будет доступна по адресу `http://127.0.0.1:8000/admin/`.
Документация будет доступна по адресу `http://127.0.0.1:8000/swagger/`.
Фильтрация по датам `http://127.0.0.1:8000/api/rooms/?start_date=2024-07-05&end_date=2024-07-25&`.
Фильтрация по датам и комнате `http://127.0.0.1:8000/api/rooms/?start_date=2024-07-05&end_date=2024-07-25&name=21`.
