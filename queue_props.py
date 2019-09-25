import pika
import ConnectLocal as conn

#Auto_delete : Queue is automatically deleted once consumer cancels/disconnects
queue_name1 = "auto_delete"
# durable survives the reboot of a broker
queue_name2 = "non_durable"
#only allow access to current connection
queue_name3 = "exclusive"

def callback(channel, method, body, prop):
    pass
# exist check without creating a queue
with conn.do_connect() as channel:
    #It will not create the queue but check if it already exists
    queue_ok_result = channel.queue_declare("pika_queue", passive=True)
    print(queue_ok_result.method)

with conn.do_connect() as channel:
    #Creating a queue with "auto_delete" property
    queue_ok_result = channel.queue_declare(queue_name1, auto_delete=True)
    channel.queue_declare(queue_name2, durable=False)
    print("Declared auto_delete and non_durable queues, check UI")
# below is going to consume the message and once its done, queue is deleted
    channel.basic_consume(queue_name1, callback)
