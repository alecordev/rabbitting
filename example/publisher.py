import pika
import json
import uuid

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
try:
    channel = connection.channel()

    channel.exchange_declare(
        exchange='order',
        exchange_type='direct'
    )

    order = {
        'id': str(uuid.uuid4()),
        'user_email': 'email@email.com',
        'product': 'Product 1',
        'quantity': 1,
    }

    channel.basic_publish(
        exchange='order',
        routing_key='order.notify',
        body=json.dumps({'user_email': order['user_email']}).encode()
    )
    print('- Sent notify message')

    channel.basic_publish(
        exchange='order',
        routing_key='order.report',
        body=json.dumps(order).encode(),
    )
    print('- Sent report message')
except Exception as e:
    print(e)
finally:
    connection.close()
