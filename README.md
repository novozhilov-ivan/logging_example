# Пример Логирования

Демонстрационный проект, показывающий расширенные возможности логирования в Python с использованием dataclasses, аннотаций типов и объектно-ориентированного дизайна.

## Возможности

- Пользовательский форматировщик логов с подробным выводом, включающим:
  - Временную метку в формате ISO 8601
  - Имя логгера
  - Уровень логирования
  - Исходный файл
  - Имя функции
  - Сообщение
  - Информацию об исключениях
  - Трассировку стека (при наличии)
- Вывод логов как в консоль, так и в файл
- Разные уровни логирования для файла (DEBUG) и консоли (INFO)

## Структура проекта

```
logging_example/
├── app/
│   ├── __init__.py
│   └── example.py       # Пример кода, демонстрирующий использование логирования
├── config.py            # Конфигурация логирования с пользовательским форматировщиком
├── main.py              # Точка входа
├── pyproject.toml       # Зависимости проекта
└── README.md            # Этот файл
```

## Использование

   - В консоли (уровень INFO и выше)
   - В файле log.log (уровень DEBUG и выше)

## Конфигурация

Система логирования настроена в файле `config.py` со следующими компонентами:

- `CustomFormatter`: Форматирует сообщения логов с подробной контекстной информацией
- `BaseHandlerConfig`: Абстрактный базовый класс для конфигураций обработчиков
- `FileHandlerConfig`: Конфигурация для файлового логирования
- `ConsoleHandlerConfig`: Конфигурация для вывода в консоль
- `LoggingConfig`: Общая конфигурация логирования
- `get_logging_config()`: Создает и возвращает конфигурацию логирования
- `setup_logging()`: Применяет конфигурацию с помощью dictConfig из Python

## Пример

Файл `app/example.py` демонстрирует различные уровни логирования и обработку исключений:

- Базовые информационные сообщения и сообщения уровня debug
- Захват ошибок с подробностями об исключениях
- Различные способы логирования исключений
- Вывод трассировки стека
