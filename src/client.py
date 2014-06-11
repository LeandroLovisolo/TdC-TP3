#!/usr/bin/env python2
# coding: utf-8

from ptc import Socket, SHUT_WR
from struct import pack
from time import clock

msg = 'a' * 1000000

with Socket() as sock:
	sock.connect(('127.0.0.1', 6677))
	print 'is connected: ' + str(sock.is_connected())

	print 'sending file size: %d...' % len(msg)
	sock.send(pack('I', len(msg)))

	print 'sending file...'
	t0 = clock()
	sock.send(msg)
	t1 = clock()

	t = t1 - t0
	print 'took %f seconds' % t

	# Cerramos el stream de escritura pero podemos seguir recibiendo datos.
	sock.shutdown(SHUT_WR)
print 'all done'