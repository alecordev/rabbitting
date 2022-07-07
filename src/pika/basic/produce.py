import time
import datetime

import pika


def main():
    params = pika.ConnectionParameters(
        host="localhost",
        heartbeat=60,
        credentials=pika.PlainCredentials("rabbit", "rabbit"),
    )
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue="example")

    try:
        counter = 0
        while 1:
            message = f"Message - {datetime.datetime.utcnow().isoformat()}"
            channel.basic_publish(
                exchange="", routing_key="example", body=message.encode()
            )
            counter += 1
            time.sleep(0.1)
            print(f"Sent {counter} messages.", end="\r")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
