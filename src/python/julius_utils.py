import socket
import julius_conf as conf

def makeConnection():
        print('make connection... host: ' + conf.host + ' port: ' + str(conf.port))
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((conf.host, conf.port))
        return client

