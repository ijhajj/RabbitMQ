# This is the server Side processing
import pika
import ConnectLocal as locale


with locale.do_connect() as channel:
    #declare queue
    channel.queue_declare("request_queue", durable=True)
    #bind queue to Exchange : amq.direct
    channel.queue_bind("request_queue", "amq.direct", routing_key="request")


    def callback(ch, method, props, body):
        """This is the callback function of the consumer"""
        """But, as it also needs to send back a response, it will also have Publishing logic"""
        print("This is the Callback function on Server Side (Consumer)...")
        # in consumer publish to reply_to tag
        #pick the queue from reply_to properties
        # Exchange will be defaulty bound
        ch.basic_publish(routing_key=props.reply_to, exchange="",
            body="response to the request: {0}".format(body))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    #This is consuming the message received from Producer/Request
    channel.basic_consume("request_queue", callback)
    channel.start_consuming()
