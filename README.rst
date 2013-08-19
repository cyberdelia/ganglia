=======
Ganglia
=======

A library to send metric to Ganglia in python.
Supports UDP, multicast, group and spoofing.

Installing
==========

To install : ::

    pip install ganglia


Usage
=====

Sending metric over UDP: ::

    ganglia = GMetric("udp://127.0.0.1")
    ganglia.send({
        'name': 'hits',
        'units': 'req/sec',
        'type: 'uint8',
        'value': 200,
        'tmax': 60,
        'dmax': 300,
        'group': 'web'
    })
