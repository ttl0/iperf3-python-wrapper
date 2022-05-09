#!/usr/bin/env python3
import iperf3
from multiprocessing import Process
from queue import Queue
import time

def start_stream(flow):
    client = iperf3.Client()
    client.duration = 9 
    client.server_hostname = '192.168.138.129'
    # 1MBps
    client.bandwidth = flow['bw'] 
    client.port = flow['port'] 
    #expressed in 0x## 
    client.tos = 0xC0

    print('Connecting to {0}:{1}'.format(client.server_hostname, client.port))
    result = client.run()

    if result.error:
        print(result.error)
    else:
        print('')
        print('Test completed:')
        print('  started at         {0}'.format(result.time))
        print('  bytes transmitted  {0}'.format(result.sent_bytes))
        print('  retransmits        {0}'.format(result.retransmits))
        print('  avg cpu load       {0}%\n'.format(result.local_cpu_total))
        mbps = round(result.sent_Mbps,2) 
#        print('  MegaBytes per second (MB/s)  {0}'.format(result.sent_MB_s))
        print('  Megabits per second (Mbps)  {0}'.format(mbps))
    print(f'Done with stream {client.port}')


if __name__ == "__main__":
    flows = [
            {'port':5204, 'bw': 3000000, 'dscp': 'ef'},
            {'port':5205, 'bw': 2000000, 'dscp': 'cs1'},
            {'port':5206, 'bw': 1000000, 'dscp': 'cs1'}
            ]
    # Even if networking is IO bound, we use multiprocessing due to
    # iPerf restrictions on GIL
    for _ in range(1):
        for i, flow in enumerate(flows):
            p = Process(target=start_stream, args=(flow,))
            p.start()
        time.sleep(10)



