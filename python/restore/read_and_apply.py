import json
import socket
from time import sleep

import requests


s = socket.socket()
s.connect(("localhost", 14460))

def send(metric, time, value):
    line = metric + " " + str(time) + " " + str(value)
    print line
    s.send("put " + line + "\n")

url = "http://localhost:4242/api/query/exp"

payload = """
{
   "time": {
       "start": "1m-ago",
       "end": "1ms-ago",
       "aggregator":"sum"
   },
   "filters": [
       {
           "tags": [
               {
                   "type": "literal_or",
                   "tagk": "source",
                   "filter": "factory2",
                   "groupBy": true
               }
           ],
           "id": "f1"
       }
   ],
   "metrics": [
       {
           "id": "t",
           "metric": "temperature",
           "filter": "f1",
           "fillPolicy":{"policy":"nan"}
       },
       {
           "id": "p",
           "metric": "pressure",
           "filter": "f1",
           "fillPolicy":{"policy":"nan"}
       }
   ],
   "expressions": [
       {
           "id": "temperature",
           "expr": "t"
       },
       {
           "id": "pressure",
           "expr": "p"
       }
    ],
    "outputs":[
      {"id":"temperature"},
      {"id":"pressure"}
    ]
 }
"""
payload_dict = json.loads(payload)
payload_time = payload_dict["time"]

headers = {
    'Content-Type': "application/json",
    'Cache-Control': "no-cache",
    'Postman-Token': "542a1ff7-2cfe-4f85-8559-de2ec8928718"
    }

end = 0

while end < 72:
    # end being zero will result in an OpenTSDB error. So don't use it for
    # the first iteration.
    payload_time["start"] = "%dh-ago" % (end + 1)
    payload = json.dumps(payload_dict)
    response = requests.request("POST", url, data=payload, headers=headers)
    outputs = response.json()["outputs"]

    if not outputs:
        break

    sent = 0
    for output in outputs:
        metric = output["id"]
        for dp in output["dps"]:
            sent += 1
            send(metric, *dp)

    end += 1
    payload_time["end"] = "%dh-ago" % end
    sleep(5)

print sent

