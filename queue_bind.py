import pika
import sys
import ConnectLocal

""" This module creates a queue : simple_bind and uses default binding """
bind_simple = True
if len(sys.argv)>1:
    bind_simple = False

#connect
channel = ConnectLocal.do_connect()

if bind_simple:
    channel.queue_declare("simple_bind")
    print("Implicit binding is done, check the Web UI")
else:
    channel.queue_declare("direct_bind")
    channel.queue_bind(queue="direct_bind", exchange="amq.direct",
                        routing_key="demonstrate")
    print("bound queue 'direct_bind' to exchange 'amq.direct' with key 'demonstrate'")
#close Connection
channel.close()
