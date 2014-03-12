# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import socket

from xdrlib import Packer

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


SLOPE = {
    'zero': 0,
    'positive': 1,
    'negative': 2,
    'both': 3,
    'unspecified': 4
}


class GMetric(object):
    def __init__(self, url):
        parsed = urlparse(url)
        if parsed.scheme not in ('udp', 'multicast'):
            raise ValueError("Invalid protocol")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if parsed.scheme == 'multicast':
            self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)
        self.address = (socket.gethostbyname(parsed.hostname), parsed.port or 8670)

    def send(self, **kwargs):
        meta, data = self.pack(kwargs)
        self.socket.sendto(meta, self.address)
        self.socket.sendto(data, self.address)

    def pack(self, values):
        metric = {
            'hostname': '',
            'spoof': 0,
            'units': '',
            'slope': 'both',
            'tmax': 60,
            'dmax': 0
        }
        metric.update(values)

        if metric.get('spoof', False):
            metric['spoof'] = 1
        else:
            metric['spoof'] = 0

        metric['slope'] = SLOPE[metric['slope']]

        for key in ('name', 'value', 'type'):
            if key not in metric:
                raise KeyError("Missing {0}".format(key))

        if metric['type'] not in ('string', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'float', 'double'):
            raise TypeError("Invalid metric type")

        convert = lambda v: v.encode() if isinstance(v, str) else v
        metric = {key: convert(value) for key, value in metric.items()}

        # Metadata
        meta = Packer()
        meta.pack_int(128)
        meta.pack_string(metric['hostname'])
        meta.pack_string(metric['name'])
        meta.pack_int(int(metric['spoof']))
        meta.pack_string(metric['type'])
        meta.pack_string(metric['name'])
        meta.pack_string(metric['units'])
        meta.pack_int(metric['slope'])
        meta.pack_uint(int(metric['tmax']))
        meta.pack_uint(int(metric['dmax']))

        # Group support
        if 'group' in metric:
            meta.pack_int(1)
            meta.pack_string(b"GROUP")
            meta.pack_string(metric['group'])
        else:
            meta.pack_int(0)

        # Data
        data = Packer()
        data.pack_int(128 + 5)
        data.pack_string(metric['hostname'])
        data.pack_string(metric['name'])
        data.pack_int(int(metric['spoof']))
        data.pack_string(b"%s")
        data.pack_string(bytes(metric['value']))

        return meta.get_buffer(), data.get_buffer()
