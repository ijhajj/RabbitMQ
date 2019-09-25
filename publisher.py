from kombu import Connection, Exchange, Producer, Queue

#set up connection
rabbit_url = "amqp://guest:guest@localhost:5672"
conn = Connection(rabbit_url)
#set up channel
channel = conn.channel()
#set up exchange
exchange = Exchange("example-exchange", type='direct')
#set up Producer
producer = Producer(exchange=exchange, channel=channel, routing_key="IP")
#Create a Queue
queue=Queue(name="example-queue", exchange=exchange, routing_key="IP")
#Bind the queue to the Exchange
queue.maybe_bind(conn)
queue.declare()
#Send the message
producer.publish("Hello There")
