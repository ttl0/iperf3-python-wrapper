#!/usr/bin/env python3
from multiprocessing import Process
import iperf3


def start_servers(flow):
    server = iperf3.Server()
    server.port = flow 
    while True:
        result = server.run()
        mbps = round(result.received_Mbps, 2)
        print(f'From port {server.port} - {mbps} Mbps')

if __name__ == "__main__":
    flows = [5204, 5205, 5206]
    for flow in flows:
        p = Process(target=start_servers, args=(flow,))
        p.start()
