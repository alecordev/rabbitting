import time
import datetime

import pika


def main():
    params = pika.ConnectionParameters(host="localhost", heartbeat=60, credentials=pika.PlainCredentials('rabbit', 'rabbit'))
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    # channel.exchange_declare(exchange='rabbit',
    #                          exchange_type='fanout')
    queue = channel.queue_declare(queue='example', exclusive=True)
    # channel.queue_bind(exchange='rabbit',
    #                    queue=queue.method.queue)

    counter = 0
    try:
        start = time.time()
        while 1:
            message = f"message-{datetime.datetime.utcnow().isoformat()}"
            channel.basic_publish(exchange='',
                                  routing_key='example',
                                  body=message)
            time.sleep(0.1)
            counter += 1
            print(f'Sent {counter} messages', end="\r")
            if time.time() - start > 3600:
                break
    finally:
        channel.close()
        connection.close()
        print('All closed.')


if __name__ == "__main__":
    main()
