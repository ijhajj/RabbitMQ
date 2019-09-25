from kombu import Exchange, Connection, Queue
from kombu.mixins import ConsumerMixin


class Worker(ConsumerMixin):
    """ Need to have connection attribute """
    def __init__(self, connection,queues):
        self.connection = connection
        self.queues = queues

    def on_message(self, body, message):
        """ callback consumer function """
        print('Got message : {0}'.format(body))
        message.ack()

    #@override
    def get_consumers(self, Consumer, channel):
        """ Returns a list of consumers the worker will use """
        return [Consumer(queues=self.queues, callbacks=[self.on_message])]

rabbit_url = "amqp://guest:guest@localhost:5672"
exchange = Exchange("example-exchange", type="direct")
queues = [Queue(name="example-queue", exchange=exchange, routing_key="IP")]

with Connection(rabbit_url, heartbeat=4) as conn:
    worker = Worker(conn, queues)
    #run function internally keeps checking with heartbeat_check and
    #keeps looping till connection is stopped
    worker.run()
