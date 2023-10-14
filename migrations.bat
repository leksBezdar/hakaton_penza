@echo off


rem Обнуление таблиц
alembic downgrade -1

rem Миграции
alembic upgrade head

rem Ожидание нажатия любой клавиши перед закрытием окна
pause