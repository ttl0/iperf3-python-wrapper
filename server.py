#/usr/bin/env python3
from multiprocessing import Process, Manager
import iperf3
import MODELS


def start_servers(flow, output):
    server = iperf3.Server()
    server.port = flow['port']
    result = server.run()
    received = round(result.received_Mbps, 2)
    return_dict = {}
    return_dict['name'] = flow['name']
    return_dict['received'] = received 
    output.append(return_dict)


if __name__ == "__main__":
    manager = Manager()
    output = manager.list()
    processes = [] 
    for flow in MODELS.flows:
        p = Process(target=start_servers, args=(flow, output))
        processes.append(p)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    print(output)
