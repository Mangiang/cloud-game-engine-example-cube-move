
from kafka import KafkaProducer
import json


def init_kafka_producer(to_produce):
    print("Building Kafka Producer", flush=True)
    user = "user"
    password = "user"
    addr = "kafka-headless.default.svc.cluster.local"
    port = 9092
    producer = KafkaProducer(bootstrap_servers=f'{addr}:{port}',
                             sasl_mechanism="PLAIN",
                             security_protocol="SASL_PLAINTEXT",
                             sasl_plain_username=user,
                             sasl_plain_password=password)

    while True:
        to_produce_str = json.dumps(to_produce.get())
        to_produce_bytes = to_produce_str.encode("utf-8")
        producer.send('game_state', to_produce_bytes)
