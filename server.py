#/usr/bin/env python3
from multiprocessing import Process
import iperf3
import MODELS


def start_servers(flow):
    server = iperf3.Server()
    server.port = flow 
    while True:
        result = server.run()
        mbps = round(result.received_Mbps, 2)
        print(f'From port {server.port} - {mbps} Mbps')

if __name__ == "__main__":
    for flow in MODELS.flows:
        p = Process(target=start_servers, args=(flow['port'],))
        p.start()
