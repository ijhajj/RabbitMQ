import pika

def _create_channel(conn_param):
    connection = pika.BlockingConnection(conn_param)
    #get channel
    channel = connection.channel()
    return channel

def do_connect():
    """ Passes the credentials, sets up a connection and returns a channel """
    credentials = pika.PlainCredentials("guest","guest")
    conn_param = pika.connection.ConnectionParameters(credentials=credentials)

    connection = pika.BlockingConnection(conn_param)

    channel = connection.channel()

    return channel

def connect_heartbeat():
    credentials = pika.PlainCredentials("guest", "guest")
    conn_param = pika.ConnectionParameters(heartbeat=1500, credentials=credentials)
    #Establish TCP connection
    return _create_channel(conn_param)
