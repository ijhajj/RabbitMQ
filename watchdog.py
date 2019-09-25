import requests
import pika
from requests.auth import HTTPBasicAuth as auth
import time

_status = "backing_queue_status"
_argumets = "arguments"
_mode = "mode"

url = "http://localhost:15672/api/queues/%2F/new_queue"
while True:
    response = requests.get(url, auth=auth("guest", "guest"))
    queue = response.json()

    try:
        is_lazy=False
        if _status in queue:
            is_lazy = queue[_status][_mode] == 'lazy'
        elif _argumets in queue:
            is_lazy = queue[_argumets][_mode] = 'lazy'

        if is_lazy:
            print("All is well")
        else:
            raise Exception
    except:
        print("Lazy mode is unavailable")

    time.sleep(10)
