
from kafka import KafkaConsumer
import json


def init_kafka_consumer(to_produce):
    print("Building Kafka Consumer", flush=True)
    user = "user"
    password = "user"
    addr = "kafka-headless.default.svc.cluster.local"
    port = 9092
    consumer = KafkaConsumer(bootstrap_servers=f'{addr}:{port}',
                             group_id="gameplay_script",
                             sasl_mechanism="PLAIN",
                             security_protocol="SASL_PLAINTEXT",
                             sasl_plain_username=user,
                             sasl_plain_password=password)
    consumer.subscribe(['input', 'connection'])
    print(f'Did subscribe to {consumer.subscription()}', flush=True)

    for message in consumer:
        print(message, flush=True)
        message_value = str(message.value) if type(
            message.value) is not bytes else message.value.decode("utf-8")
        print(message_value, flush=True)

        message_json = json.loads(message_value)

        if message.topic == "connection":
            to_produce.put({"type": "instantiate", "mesh": "box",
                            "name": "Box", "scale": 4, "time": message_json["time"]})
        elif message.topic == "input":
            x = 0
            y = 0
            if "action" in message_json and message_json["action"] == "KEY_DOWN":
                if message_json["key"] == "ArrowUp":
                    y = 1
                elif message_json["key"] == "ArrowDown":
                    y = -1
                elif message_json["key"] == "ArrowRight":
                    x = 1
                elif message_json["key"] == "ArrowLeft":
                    x = -1
                to_produce.put({"type": "translation", "vector": {
                               "x": x, "y": y, "z": 0}, "name": "Box", "distance": 1, "time": message_json["time"]})
