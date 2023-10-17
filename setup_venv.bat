@echo off

rem Создание и активация виртуального окружения
python -m venv venv
call venv\Scripts\activate

rem Установка зависимостей из файла requirements.txt
pip install -r requirements.txt

rem Миграции
alembic upgrade head

rem Запуск сервера uvicorn
uvicorn src.main:app --reload

rem Ожидание нажатия любой клавиши перед закрытием окна