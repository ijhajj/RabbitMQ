import pika
from ConnectLocal import do_connect


def consuming_callback(ch, method, body):
    message = body.decode()
    if "reject" in message:
        #setting basic_nack: "Not acknowledged" : implies message was not consumed
        #                   And needs to be requeued, this can be turned On/OFF
        #                   Default : Requeue
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        print("N-acked the message & Requeued")
    else:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("Message {0} is received correctly & successfully".format(message))

with do_connect() as channel:
    value =""
    while(value!="q"):
        #auto_ack: turns off auto acknowledgements and expect Explicit acks.
        (method, props, body) = channel.basic_get("pika_queue", auto_ack=False)
        if body:
            #if body exists consume the message
            consuming_callback(channel, method, body)
            #ask user to enter option to continue or quit
        value=raw_input("any key to continue, q to stop")
