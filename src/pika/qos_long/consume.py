import time
import random
import datetime

import pika


def main():
    params = pika.ConnectionParameters(
        host="localhost",
        heartbeat=60,
        credentials=pika.PlainCredentials("admin", "admin"),
    )
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.basic_qos(
        prefetch_count=1
    )  # tell RabbitMQ not to give more than one message to a worker at a time.
    channel.queue_declare(queue="example")

    def callback(ch, method, properties, body):
        wait = random.randint(20, 120)
        print(
            f"[{datetime.datetime.utcnow().isoformat()}] Received {body.decode()}. Running for {wait}"
        )
        time.sleep(wait)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue="example", on_message_callback=callback)

    try:
        print(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
    finally:
        channel.close()
        connection.close()


if __name__ == "__main__":
    main()
