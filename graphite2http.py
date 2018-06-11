#!/usr/bin/env python
import logging
import socket
import ConfigParser
import requests
from requests.auth import HTTPBasicAuth

log = logging.getLogger('udp_server')


def udp_server(host='127.0.0.1', port=2003):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #log.info("Listening on udp %s:%s" % (host, port))
    s.bind((host, port))
    while True:
        (data, addr) = s.recvfrom(128*1024)
        yield data


FORMAT_CONS = '%(asctime)s %(name)-12s %(levelname)8s\t%(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT_CONS)

config = ConfigParser.RawConfigParser()
config.read('/etc/graphite2http.cfg')
token = config.get('general', 'token')
key = config.get('general', 'key')

auth = HTTPBasicAuth(token, key)

for data in udp_server():
    url = "https://graphapi.lunasys.fr/raw?%s" % "&".join(["value=" + line.replace(" ", ":") for line in data.split("\r\n")])
    r = requests.post(url, auth=auth)
