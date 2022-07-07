# notify

import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
try:
    channel = connection.channel()

    queue = channel.queue_declare("order_notify")
    queue_name = queue.method.queue

    channel.queue_bind(
        exchange="order",
        queue=queue_name,
        routing_key="order.notify",
    )

    def callback(ch, method, properties, body):
        payload = json.loads(body)
        print(f'- Notifying {payload["user_email"]}')
        print("- Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(on_message_callback=callback, queue=queue_name)
    print(" [*] Waiting for notify messages. CTRL-C to exit.")

    channel.start_consuming()
except Exception as e:
    print(e)
finally:
    connection.close()
