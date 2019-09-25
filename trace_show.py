import pika
import ConnectLocal

channel = ConnectLocal.do_connect()

body="from tracing published"
while True:
    channel.basic_publish("amq.direct", "pika_queue", body)
    v = raw_input("Enter c to continue and q to exit")
