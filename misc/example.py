import time
import json
import threading

import pika


def process_export():
    print('Long running process in thread')
    time.sleep(10)


def data_handler(channel, method, properties, body):
    # body = json.loads(body)
    print('Message received! Will do some work...')

    thread = threading.Thread(target=process_export, args=())
    thread.start()
    while thread.is_alive():  # Loop while the thread is processing
        channel._connection.sleep(1.0)

    print("Back from thread")
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    params = pika.ConnectionParameters(
        host="localhost",
        heartbeat=60,
        credentials=pika.PlainCredentials("rabbit", "rabbit"),
    )
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    # channel.queue_declare(queue="some_queue", durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_message_callback=data_handler, queue="example")
    try:
        print('Consuming...')
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    channel.close()
    connection.close()


if __name__ == "__main__":
    main()
