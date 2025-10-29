## Описание
Простая реляционная база данных, реализованная на Python с использованием файловой системы для хранения данных. Проект разработан для освоения принципов работы с базами данных, CRUD-операций.

## Функции
Полный набор CRUD операций: Create, Read, Update, Delete
SQL-подобный синтаксис
Автоматическая генерация ID
Валидация типов данных:  int, str, bool
Файловое хранение: Данные сохраняются в JSON-файлах
Красивый вывод: Табличное отображение данных через PrettyTable
Обработка ошибок: Информативные сообщения об ошибках

## Требования
Python 3.8 или выше

Poetry для управления зависимостями

## Установка

# Клонируйте репозиторий
git clone <git@github.com:Anastasia783/project_2_Anastasiya_Pankratova_M25-555.git>
cd primitive-db

# Установите зависимости через Poetry
poetry install
# Или используйте Makefile
make install

## Запуск

# Запуск базы данных
poetry run database
# Или через Makefile
make run

## Демонстрация работы
https://asciinema.org/a/Ngnappl2WTOcaEQMTz0F0WAeb

Для просмотра демонстрации нажмите на изображение выше

## Доступные команды
Создание таблицы
sql

CREATE TABLE имя_таблицы (столбец1 тип1, столбец2 тип2, ...)


## Вставка данных
sql
INSERT INTO имя_таблицы VALUES (значение1, значение2, ...)

## Выборка данных
sql
SELECT FROM имя_таблицы [WHERE условие]


## Обновление данных
sql
UPDATE имя_таблицы SET столбец=новое_значение [WHERE условие]


## Удаление данных
sql
DELETE FROM имя_таблицы [WHERE условие]

## Информация о таблице
sql
INFO имя_таблицы


## Архитектура проекта
text
primitive_db/
├── src/primitive_db/
│   ├── __init__.py
│   ├── main.py             
│   ├── engine.py          
│   ├── core.py             
│   ├── utils.py             
│   ├── parser.py           
│   ├── decorators.py        
│   └── constants.py       
├                
├── data/                  
├── pyproject.toml           
├── README.md               
└── Makefile                

## Запуск линтера

poetry run ruff check .


## Очистка проекта

make clean

## Автор
Анастасия Панкратова
Студентка группы M25-555