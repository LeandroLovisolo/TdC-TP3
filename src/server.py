#!/usr/bin/env python2
# coding: utf-8

from ptc import Socket
from struct import unpack

received = str()

with Socket() as sock:
    sock.bind(('127.0.0.1', 6677))
    sock.listen()

    print 'waiting for a client...'
    
    sock.accept()

    print 'client connected'

    size_str = sock.recv(4)
    size = unpack('I', size_str)[0]

    print 'receiving %d bytes...' % size

    while len(received) < size:
    	received += sock.recv(size - len(received))

    print 'closing socket...'
    
    sock.close()

#print 'received: %s' % received

print 'all done'