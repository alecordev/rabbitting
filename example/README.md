# RabbitMQ

Simple example with a producer that generates 2 messages (notification and report) and 2 consumers one for each message type.

1. Create your local RabbitMQ instance with Docker:

- `docker run --rm -it --hostname rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management`

2. Run the `publisher.py` and both workers (`worker_notify.py` and `worker_report.py`)
