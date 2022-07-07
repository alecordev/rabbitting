import time
from functools import wraps

import amqpstorm


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time.perf_counter()
        result = f(*args, **kw)
        te = time.perf_counter()
        print("func:%r args:[%r, %r] took: %.6f sec" % (f.__name__, args, kw, te - ts))
        return result

    return wrap


@timing
def main():
    with amqpstorm.Connection("localhost", "rabbit", "rabbit") as connection:
        with connection.channel() as channel:
            channel.queue.declare("fruits")
            message = amqpstorm.Message.create(
                channel,
                body="Hello RabbitMQ!",
                properties={"content_type": "text/plain"},
            )
            message.publish("fruits")


if __name__ == "__main__":
    main()
