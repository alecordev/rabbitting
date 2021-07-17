import time
import random
import datetime

import pika


def main():
    params = pika.ConnectionParameters(host="localhost", heartbeat=60, credentials=pika.PlainCredentials('rabbit', 'rabbit'))
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue='example')

    def callback(ch, method, properties, body):
        wait = random.randint(20, 120)
        print(f"[{datetime.datetime.utcnow().isoformat()}] Received {body.decode()}. Running for {wait}")
        time.sleep(wait)

    channel.basic_consume(queue='example', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    main()
