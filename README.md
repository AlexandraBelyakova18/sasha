# Система управления материалами "МОЗАИКА"

Веб-приложение для управления материалами производственной компании "МОЗАИКА", специализирующейся на выпуске керамической плитки.

## Описание системы

Система предназначена для эффективного управления материалами и поставщиками компании. Основные возможности:

- Просмотр и управление списком материалов
- Добавление и редактирование информации о материалах
- Отслеживание остатков на складе и минимальных запасов
- Автоматический расчет стоимости минимально необходимых партий
- Управление информацией о поставщиках
- Связывание материалов с поставщиками
- Анализ рейтингов поставщиков

## Технические требования

- Python 3.11+
- Flask
- SQLAlchemy
- Pandas для работы с Excel файлами
- Bootstrap 5 для интерфейса

## Установка и запуск

### 1. Подготовка окружения

Убедитесь, что у вас установлен Python 3.11 или выше:

```bash
python --version
```

### 2. Установка зависимостей

Все необходимые пакеты уже установлены в проекте:
- flask
- flask-sqlalchemy
- flask-wtf
- gunicorn
- pandas
- openpyxl
- psycopg2-binary
- sqlalchemy
- werkzeug
- wtforms
- email-validator

### 3. Запуск приложения

#### Вариант А: Через Gunicorn (рекомендуется)

```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

#### Вариант Б: Через Python напрямую

```bash
python main.py
```

#### Вариант В: Через app.py

```bash
python app.py
```

### 4. Доступ к приложению

После запуска приложение будет доступно по адресу:
- http://localhost:5000
- http://0.0.0.0:5000

## Структура проекта

```
├── app.py                 # Основная конфигурация Flask приложения
├── main.py               # Точка входа для Gunicorn
├── models.py             # Модели базы данных
├── routes.py             # Маршруты и контроллеры
├── forms.py              # Формы WTForms
├── data_import.py        # Импорт данных из Excel файлов
├── load_excel_data.py    # Скрипт загрузки данных
├── static/               # Статические файлы
│   ├── css/
│   │   └── style.css     # Стили приложения
│   ├── js/
│   │   └── main.js       # JavaScript функции
│   └── images/
│       └── logo.svg      # Логотип компании
├── templates/            # HTML шаблоны
│   ├── base.html         # Базовый шаблон
│   ├── index.html        # Главная страница
│   ├── materials.html    # Список материалов
│   ├── material_form.html # Форма добавления/редактирования
│   ├── suppliers.html    # Список поставщиков
│   └── error.html        # Страница ошибок
└── attached_assets/      # Excel файлы с данными
    ├── Material_type_import_*.xlsx
    ├── Suppliers_import_*.xlsx
    ├── Materials_import_*.xlsx
    └── Material_suppliers_import_*.xlsx
```

## Функциональность

### Материалы

- **Просмотр списка**: Отображение всех материалов с информацией о типе, количестве на складе, минимальных запасах
- **Расчет нехватки**: Автоматический расчет необходимого количества для закупки и стоимости партии
- **Добавление/редактирование**: Формы для управления информацией о материалах
- **Валидация**: Проверка корректности вводимых данных

### Поставщики

- **Список поставщиков**: Отображение всех поставщиков с рейтингами и контактами
- **Поставщики материала**: Просмотр поставщиков для конкретного материала
- **Статистика**: Анализ рейтингов и цен поставщиков

### Алгоритм расчета стоимости партии

Система рассчитывает минимально необходимую партию материала по следующему алгоритму:

1. Определяется нехватка: `нехватка = минимальное_количество - количество_на_складе`
2. Если нехватки нет, стоимость = 0
3. Рассчитывается количество упаковок: `упаковки = ceil(нехватка / количество_в_упаковке)`
4. Общее количество для покупки: `всего_единиц = упаковки × количество_в_упаковке`
5. Стоимость: `стоимость = всего_единиц × цена_за_единицу`

## Дизайн и стиль

Приложение следует корпоративному руководству по стилю:

- **Шрифт**: Comic Sans MS
- **Основной фон**: #FFFFFF (белый)
- **Дополнительный фон**: #ABCFCE (голубой)
- **Акцентный цвет**: #546F94 (синий)
- **Логотип**: Мозаичный узор компании "МОЗАИКА"

## База данных

Система использует SQLite базу данных с следующими таблицами:

- **material_types**: Типы материалов
- **suppliers**: Поставщики
- **materials**: Материалы с информацией о запасах и ценах
- **material_suppliers**: Связи между материалами и поставщиками

## Импорт данных

При первом запуске система автоматически импортирует данные из Excel файлов в папке `attached_assets/`. Если файлы недоступны, используются тестовые данные.

Для принудительного обновления данных:

```bash
python load_excel_data.py
```

## Переменные окружения

- `SESSION_SECRET`: Секретный ключ для сессий (по умолчанию: dev-secret-key-change-in-production)
- `DATABASE_URL`: URL базы данных (по умолчанию: sqlite:///materials.db)

## Режим отладки

Приложение запускается в режиме отладки для разработки. В продакшене рекомендуется отключить:

```python
app.run(debug=False)
```

## Поддержка

Система разработана в соответствии с техническим заданием демонстрационного экзамена по специальности "Информационные системы и программирование".

---

**Разработано для производственной компании "МОЗАИКА"**