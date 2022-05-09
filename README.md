# iPerf3 Python Wrapper

The original iperf3-python wrapper at https://iperf3-python.readthedocs.io/en/latest/ had some missing features.
I modified the wrapper to add DSCP / TOS options. 
The Client/Server python scripts are an example of using multiprocessing for parallel stream testing.
There was an issue with iPerf and multithreading *possibly due to GIL.

## Make sure iperf3 is installed
- Ubuntu:
```
sudo apt install iperf3
```
## Server
```
>>> import iperf3
>>> server = iperf3.Server()
>>> result = server.run()
```

## Client with DSCP EF set
We must use the ToS(hex) value to set the client (Sender) side DSCP bits
```
>>> import iperf3
>>> client = iperf3.Client()
>>> client.duration = 5 
>>> client.server_hostname = '127.0.0.1'
>>> client.port = 5201
>>> client.tos = 0xB8
>>> result = client.run()
```
