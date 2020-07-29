# import asyncio
from flask import Flask
# import textwrap
import stomp
import time
# import time
# import re
# import sys
import json

# msgs = []


# def callback(ch, method, properties, body):
#     print(" [x] Received %r" % body)
#     string = body.decode('utf-8')
#     msgs.append(string)
#     p = re.compile(r"\[(\d+(\.\d+)?)\].*")
#     m = p.match(string)
#     print(f"found {m.group()} on {time.time_ns() / (10 ** 9)}")
#     timer = float(m.group(1))
#     print(f"elapsed: {time.time_ns() / (10 ** 9) - timer}")


print("variables")
user = "user"
password = "user"
addr = "rabbitmq.default.svc.cluster.local"
port = 61613


# def send():
#     credentials = pika.PlainCredentials(username=user, password=password)
#     connection = pika.BlockingConnection(
#         pika.ConnectionParameters(addr, '/rabbitmq/amqp', credentials))
#     channel = connection.channel()
#     channel.queue_declare(queue='hello')
#     channel.basic_publish(exchange='',
#                           routing_key='hello',
#                           body=f'[{time.time_ns() / (10 ** 9)}] Hello World!')
#     print(f"[{time.time_ns() / (10 ** 9)}] Sent 'Hello World!'")
#     connection.close()


# def broadcast_logs():
#     credentials = pika.PlainCredentials(username=user, password=password)
#     connection = pika.BlockingConnection(
#         pika.ConnectionParameters(addr, '/rabbitmq/amqp', credentials))
#     channel = connection.channel()
#     channel.exchange_declare(exchange='logs', exchange_type='fanout')

#     message = ' '.join(sys.argv[1:]) or "info: Hello World!"
#     channel.basic_publish(exchange='logs', routing_key='', body=message)
#     print(" [x] Sent %r" % message)
#     connection.close()


# def callback_broadcast(ch, method, properties, body):
#     print(" [x] %r" % body)


# def receive_broadcast():
#     credentials = pika.PlainCredentials(username=user, password=password)
#     connection = pika.BlockingConnection(
#         pika.ConnectionParameters(addr, 5672, '/', credentials))
#     channel = connection.channel()
#     channel.exchange_declare(exchange='logs', exchange_type='fanout')

#     result = channel.queue_declare(queue='', exclusive=True)
#     queue_name = result.method.queue

#     channel.queue_bind(exchange='logs', queue=queue_name)

#     print(' [*] Waiting for logs. To exit press CTRL+C')
#     channel.basic_consume(
#         queue=queue_name, on_message_callback=callback_broadcast, auto_ack=True)

#     channel.start_consuming()

print("connect_and_subscribe")


def connect_and_subscribe(conn):
    print("connecting to rabbitmq")
    conn.connect(user, password, wait=True)
    conn.subscribe(destination='/queue/connection', id=1, ack='auto')
    conn.subscribe(destination='/queue/input', id=2, ack='auto')
    print("connected to rabbitmq")


print("Building MyListener")


class MyListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_error(self, headers, body):
        print('received an error "%s"' % body)

    def on_message(self, headers, body):
        print(f'received a message {body}')
        json_body = json.loads(body)
        if headers["destination"] == "/queue/connection":
            if json_body["type"] == "connection":
                conn.send(destination='/queue/game_state', body=json.dumps(
                    {"type": "instantiate", "mesh": "box", "name": "Box", "scale": 4, "time": json_body["time"]}))
        elif headers["destination"] == "/queue/input":
            x = 0
            y = 0
            if "action" in json_body and json_body["action"] == "KEY_DOWN":
                if json_body["key"] == "ArrowUp":
                    y = 1
                elif json_body["key"] == "ArrowDown":
                    y = -1
                elif json_body["key"] == "ArrowRight":
                    x = 1
                elif json_body["key"] == "ArrowLeft":
                    x = -1
                conn.send(destination='/queue/game_state', body=json.dumps(
                    {"type": "translation", "vector": {"x": x, "y": y, "z": 0}, "name": "Box", "distance": 1, "time": json_body["time"]}))
        print('processed message')

    def on_disconnected(self):
        print('disconnected')
        connect_and_subscribe(self.conn)


# def receive():
    # credentials = pika.PlainCredentials(username=user, password=password)
    # connection = pika.BlockingConnection(
    #     pika.ConnectionParameters(addr, 80, 'rabbitmq.default.svc.cluster.local/amqp', credentials))
    # channel = connection.channel()
    # channel.queue_declare(queue='hello')
    # channel.basic_consume(queue='hello',
    #                       auto_ack=True,
    #                       on_message_callback=callback)
    # print('[*] Waiting for messages. To exit press CTRL+C')
    # channel.start_consuming()

print("Building Flask app")
app = Flask(__name__)
@app.route('/')
def index():
    return 'index'


print("Building connection")
conn = stomp.Connection([(addr, port)], heartbeats=(20000, 0))
conn.set_listener('', MyListener(conn))
connect_and_subscribe(conn)
print("waiting for connections")

# print("exiting")
# conn.disconnect()
app.run(debug=True, host='0.0.0.0', port=80)
