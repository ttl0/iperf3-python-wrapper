#!/usr/bin/env python3
import iperf3
from tabulate import tabulate
from operator import itemgetter
from multiprocessing import Process, Manager
from queue import Queue
import time
import MODELS

# mapping to get DSCP values
TOSTOHEX = { 
        'cs7': 0xE0,
        'cs6': 0xC0,
        'ef': 0xB8,
        'cs5': 0xA0,
        'af43': 0x98,
        'af42': 0x90,
        'af41': 0x88,
        'cs4': 0x80,
        'af33': 0x78,
        'af32': 0x70,
        'af31': 0x68,
        'cs3': 0x60,
        'af23': 0x58,
        'af22': 0x50,
        'af21': 0x48,
        'cs2': 0x40,
        'af13': 0x38,
        'af12': 0x28,
        'cs1': 0x20
        }
        
def start_stream(flow, output):
    client = iperf3.Client()
    client.duration = 10
    client.server_hostname = '10.0.1.31'
    # 1MBps
    client.bandwidth = flow['bw'] 
    client.port = flow['port'] 
    dscp = flow['dscp']
    client.tos = TOSTOHEX[dscp]

#    print('Connecting to {0}:{1}'.format(client.server_hostname, client.port))
    result = client.run()

    if result.error:
        print(result.error)
    else:
        return_dict = {}
        sent = round(result.sent_Mbps,2)
        received = round(result.received_Mbps,2)
        return_dict['name'] = flow['name']
        return_dict['dscp'] = flow['dscp']
        return_dict['sent'] = sent
        return_dict['received'] = received
        del client
        output.append(return_dict)


if __name__ == "__main__":
    # Even if networking is IO bound, we use multiprocessing due to
    # iPerf restrictions on GIL
    for i in range(100):
        manager = Manager()
        output = manager.list()
        processes = []
        for flow in MODELS.flows:
            p = Process(target=start_stream, args=(flow, output))
            processes.append(p)

        for process in processes:
            process.start()

        for process in processes:
            process.join()
        
        sorted_output = sorted(output, key=lambda d: d['name']) 
        print("Count: {}".format(i+1))
        print(tabulate(sorted(sorted_output, key=itemgetter("name", "dscp", "sent", "received")), headers="keys"))
        print("\033[F"*(len(sorted_output)+4))

