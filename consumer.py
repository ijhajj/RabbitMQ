from kombu import Connection, Exchange, Queue, Consumer
import socket

rabbit_url = "amqp://guest:guest@localhost:5672"

conn = Connection(rabbit_url,heartbeat=10)

exchange = Exchange("example-exchange", type="direct")

queue = Queue(name="example-queue", exchange=exchange, routing_key="IP")

def process_message(body, message):
  print("The body is {}".format(body))
  message.ack()

def consume():
        try:
            conn.drain_events(timeout=2)
        except socket.timeout:
            print("Time out...")

def establish_connection():
    #creates the connection again with same parameters as before
    revived_connection = conn.clone()
    #create connection as before
    revived_connection.ensure_connection(max_retries=3)
    channel = revived_connection.channel()
    #consumer still pointed to last connection so we refresh
    consumer.revive(channel)
    consumer.consume()
    return revived_connection

with Consumer(conn, queues=queue, callbacks=[process_message], accept=["text/plain"]):
        try:
            consume()
        except conn.connection_errors:
            conn.heartbeat_check()
            print('connection error.. Revival in progress')
            new_connection = establish_connection()
