#!/usr/bin/env python3
import iperf3
from multiprocessing import Process
from queue import Queue
import time
import MODELS


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
        
def start_stream(flow):
    client = iperf3.Client()
    #
    client.duration = 9 
    client.server_hostname = '192.168.138.129'
    # 1MBps
    client.bandwidth = flow['bw'] 
    client.port = flow['port'] 
    dscp = flow['dscp']
    client.tos = TOSTOHEX[dscp]

    print('Connecting to {0}:{1}'.format(client.server_hostname, client.port))
    result = client.run()

    if result.error:
        print(result.error)
    else:
        print('')
        print('Test completed:')
        print('  Started at         {0}'.format(result.time))
        mbps = round(result.sent_Mbps,2)
        print('  Megabits per second (Mbps) {0}'.format(mbps))
        print('  Sent with DSCP {0}'.format(dscp.upper()))
    print(f'Done with stream {client.port}')


if __name__ == "__main__":
    # Even if networking is IO bound, we use multiprocessing due to
    # iPerf restrictions on GIL
    for _ in range(1):
        for i, flow in enumerate(MODELS.flows):
            p = Process(target=start_stream, args=(flow,))
            p.start()
        time.sleep(10)



