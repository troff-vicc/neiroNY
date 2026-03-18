## Презентацию и видео прототим пожно найти в папке [docs](docs)

# Нейро Новый год

**Сервис генерации персонализированных новогодних поздравлений с мультимедиа**

![1.png](docs%2Fscreenshots%2F1.png)

## 🎄 О проекте

Нейро Новый год — это интеллектуальный сервис для создания уникальных новогодних поздравлений. Генерация текстов, фото и видео-открыток с использованием искусственного интеллекта.

**Основные возможности:**
- ✍️ **Генерация текста** — персонализированные поздравления на основе введенных данных
- 🖼️ **Генерация фото** — создание новогодних открыток с AI-изображениями
- 🎬 **Генерация видео** — анимированные поздравления с голосовым сопровождением

# 🛠 Используемые технологии

## Backend

-   Python
-   Django
-   Django REST Framework
-   OpenAI API
-   SQLite

## Frontend

-   React
-   Vite
-   JavaScript
-   CSS
-   React Router

------------------------------------------------------------------------

# 🚀 Быстрый запуск проекта

## 1. Клонировать репозиторий

    git clone https://github.com/troff-vicc/neiroNY.git
    cd neiroNY

------------------------------------------------------------------------

# ⚙️ Запуск Backend

## 1. Перейти в папку backend

    cd backend

## 2. Установить Python 3.12

Проект рекомендуется запускать на **Python 3.12**, так как некоторые
зависимости могут не работать на Python 3.14.

    python3.12 --version

Если Python 3.12 не установлен:

    brew install python@3.12
    brew link --overwrite python@3.12

## 3. Создать виртуальное окружение

    python3.12 -m venv env
    source env/bin/activate

## 4. Обновить pip

    pip install -U pip setuptools wheel

## 5. Установить зависимости

Перед установкой убедитесь, что в `requirements.txt` **нет строки**

    backports.zoneinfo

Затем:

    pip install -r requirements.txt

## 6. Создать файл .env

Создайте файл `.env` в папке `backend`.

    SECRET_KEY=django_secret_key
    DEBUG=True
    OPENAI_API_KEY=your_openai_api_key

## 7. Применить миграции

    python manage.py migrate

## 8. Запустить сервер

    python manage.py runserver

Backend:

    http://127.0.0.1:8000

------------------------------------------------------------------------

# 🎨 Запуск Frontend

Откройте новый терминал.

    cd frontend
    npm install
    npm run dev

Frontend:

    http://localhost:5173

------------------------------------------------------------------------



## 📸 Скриншоты


![2.png](docs%2Fscreenshots%2F2.png)

![3.png](docs%2Fscreenshots%2F3.png)

![4.png](docs%2Fscreenshots%2F4.png)

## 📁 Структура проекта

![5.png](docs%2Fscreenshots%2F5.png)

На Фронт-энде страницы хранятся в папке src/pages/ 

На Бэк-энде каждая функция (подраздел api) отдельное Django app и храниться в [backend](backend)
А оснавная логика в каждом в файле api/views.py

---

**Нейро Новый год — Ваши поздравления будут незабываемыми!** 🎅🎁✨

---
