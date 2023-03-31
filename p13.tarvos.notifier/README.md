# P13.Tarvos.Notifier

## Микросервис для рассылок/уведомлений

Для работы локально
=
Развернуть сеть и брокер RabbitMQ
-
> make broker-compose-up

В других развернутых серивсах добавить внешнюю сеть RabbitMQ

```yaml
    networks:
        - tarvos_rabbitmq
...
tarvos_rabbitmq:
    name: tarvos-rabbitmq
    external: true
```
Развернуть приложение через контейнер
-
> make compose-up

Развернуть приложение не в контейнере
(gunicorn не работает на Windows, заменить на uvicorn [пример](https://gitlab.p13.space/mma0603/fastapi.template/-/blob/main/make/run.Makefile))
-
> make run

Сделать билд образа приложения
-
> make compose-build

Остановить и удалить контейнер
-
> make compose-down

Логи
-
> make compose-logs

Полный список команд заложен [здесь](/make)
-
