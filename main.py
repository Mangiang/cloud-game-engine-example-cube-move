import logging
import threading
import multiprocessing
import time
import json
import sys
from multiprocessing import Process, Queue
from flask_server import init_flask
from kafka_consumer import init_kafka_consumer
from kafka_producer import init_kafka_producer

to_produce = multiprocessing.Queue()
ps = [Process(target=init_flask, args=()),
      Process(target=init_kafka_consumer, args=(to_produce,)),
      Process(target=init_kafka_producer, args=(to_produce,))]

for p in ps:
    p.start()
for p in ps:
    p.join()

    if p.exception:
        error, traceback = p.exception
        print(traceback)
