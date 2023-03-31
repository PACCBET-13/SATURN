# Docker-образ P13.Tarvos Notifier

Данный репозиторий содержит описание Docker-образа P13.Tarvos Notifier
P13 docker registry (https://registry.p13.space).

#### **TAG_IMAGE**
Имя тэга (версии) продукта. Данная переменная используется тегирования целевого docker-образа.

#### **P13.Tarvos Notifier version**
Номер версии P13.Tarvos Notifier.

        Важно! Целевая версия P13.Tarvos Notifier должна быть собрана заранее.


## ENV-переменные Docker-образа

| Параметр               | Обязательное | Описание                                 | Пример значения   | Значение по умолчанию |
| :--------------------- | :----------- | :--------------------------------------- | :---------------- | :-------------------- |
| APP_HOST               | Нет          | Хост сервиса внутри контейнера           | 0.0.0.0           | 0.0.0.0               |
| APP_PORT_INTERNAL      | Нет          | Порт сервиса внутри контейнера           | 8000              | 8000                  |
| APP_PORT               | Нет          | Порт сервиса вне контейнера              | 8093              | 8000                  |
| APP_WORKERS            | Нет          | Количество воркеров                      | 1                 | 1                     |
| APP_LOG_LEVEL          | Нет          | Уровень логирования                      | info              | info                  |
| RABBITMQ_HOST          | Да           | Хост сервиса в сети(публичной/приватной) | rabbitmq          |                       |
| RABBITMQ_PORT          | Да           | Порт сервиса вне контейнера              | 5672              |                       |
| RABBITMQ_PORT_INTERNAL | Да           | Порт сервиса внутри контейнера           | 5672              |                       |
| RABBITMQ_NAME          | Да           | Имя виртуального брокера в контейнере    | rabbitmq          |                       |
| RABBITMQ_USER          | Да           | Имя пользователя                         | rabbitmq          |                       |
| RABBITMQ_PASSWORD      | Да           | Пароль пользователя                      | rabbitmq          |                       |
| SMTP_USERNAME          | Да           | Почта для рассылки                       | noreply@yandex.ru |                       |
| SMTP_PASSWORD          | Да           | Пароль для приложений к почте            | qwerty123         |                       |
| SMTP_SERVER            | Да           | Домен(Хост) сервиса рассылки             | smtp.yandex.ru    |                       |
| SMTP_PORT              | Да           | Порт сервиса рассылки                    | 465               |                       |
| SMTP_FROM_NAME         | Да           | Имя от кого будут приходить сообщения    | Tarvos            |                       |


## Использование

Файл *docker-compose.yml* содержит пример развертывания в контейнере приложения.

```yaml
version: '3.9'

x-app-port: &app-port ${APP_PORT:-8000}
x-app-port-internal: &app-port-internal ${APP_PORT_INTERNAL:-8000}

name: tarvos-notifier

services:
  backend:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    container_name: tarvos-notifier
    command: ['make', 'run']
    env_file:
      - ../${ENV_FILE}
    networks:
      - tarvos_rabbitmq
    ports:
      - target: *app-port-internal
        published: *app-port
        host_ip: 0.0.0.0
        protocol: tcp
        mode: host

networks:
  tarvos_rabbitmq:
    name: tarvos-rabbitmq
    external: true

```

Файл *rabbitmq-compose.yml* содержит пример развертывания в контейнере серивса RabbitMQ.

        Он отдельно, но может разворачиваться в одном compose файле,
        если все сервисы разворачиваются на одной машине

        !Сервис RabbitMQ должен подниматься в первую очередь, перед поднятием других сервисов
```yaml
version: '3.9'

name: tarvos-broker

services:
  rabbitmq:
    container_name: tarvos-rabbitmq
    environment:
      RABBITMQ_DEFAULT_USER: ${RABBITMQ_USER}
      RABBITMQ_DEFAULT_VHOST: ${RABBITMQ_NAME}
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASSWORD}
    image: rabbitmq:3.11-management-alpine
    networks:
      - tarvos-rabbitmq
    ports:
      - ${RABBITMQ_PORT}:${RABBITMQ_PORT_INTERNAL}
    volumes:
      - data:/var/lib/rabbitmq

networks:
  tarvos-rabbitmq:
    name: tarvos-rabbitmq
    driver: bridge

volumes:
  data:

```

Файл *env.example* содержит пример локального файла с переменными окружения для развертывания в контейнере.

```dotenv
# App
APP_HOST=0.0.0.0
APP_PORT_INTERNAL=8000
APP_PORT=8000
APP_WORKERS=1
APP_LOG_LEVEL=info


RABBITMQ_HOST=
RABBITMQ_PORT=
RABBITMQ_PORT_INTERNAL=
RABBITMQ_NAME=
RABBITMQ_USER=
RABBITMQ_PASSWORD=

SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_SERVER=
SMTP_PORT=
SMTP_FROM_NAME=

```