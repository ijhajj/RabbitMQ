import pika
import ConnectLocal as locale


def consume_response(ch, method, props, body):
    print('Consume the response...')
    print(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

with locale.do_connect() as channel:
    #create temporary or anonymous queue - will carry response from consumer
    #Exclusive Queue: can be used by multiple clients
    #Each request is correlated/tracked by correlation ID copied from
    #Request to response
    # x-expires: deletes after 30 seconds
    ok_result = channel.queue_declare("", exclusive=True, arguments={'x-expires':30000})
    #Queue created
    reply_to = ok_result.method.queue
    #Print out the name of the Queue we created
    print("queue name {0}".format(reply_to))
    #reply_to sends the address of the callback queue where the Server will
    #send its response back to Client
    # can send Correlation ID as well as part of properties
    properties = pika.BasicProperties(reply_to=reply_to)
    #publish the message with :
    # message , routing_key, callback queue
    # Exchange : "amq.direct"
    channel.basic_publish("amq.direct", routing_key="request",
        properties=properties, body="our request waits on {0}".format(reply_to))
    # The Response received from Server will need to be consumed
    # reply_to : queue details, callback function to consume the response
    channel.basic_consume(reply_to, consume_response)
    #Consume the message
    channel.start_consuming()
