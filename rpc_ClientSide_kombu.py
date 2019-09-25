from kombu import Connection, Exchange, Producer, Queue, Consumer

#Establish Connection
conn = Connection("amqp://guest:guest@localhost:5672")
#Create Exchange
exchange = Exchange("rpc", type="direct")

#callback function
def process_message(body, message):
    print("Response %s" %body)
    message.ack()

#Set up Queue
reply_queue = Queue(name="amq.rabbitmq.reply-to")

with Consumer(conn, reply_queue, callbacks=[process_message], no_ack=True):
    producer = Producer(exchange=exchange, channel=conn, routing_key="request")
    properties = {"reply_to":"amq.rabbitmq.reply-to",}
    producer.publish("Hello World",**properties)
    conn.drain_events()
