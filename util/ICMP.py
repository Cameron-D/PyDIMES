"""
   A pure python ping implementation using raw socket.
   
   https://gist.github.com/pklaus/856268
   
   Note that ICMP messages can only be sent from processes running as root.
   
   
   Derived from ping.c distributed in Linux's netkit. That code is
   copyright (c) 1989 by The Regents of the University of California.
   That code is in turn derived from code written by Mike Muuss of the
   US Army Ballistic Research Laboratory in December, 1983 and
   placed in the public domain. They have my thanks.
   
   Bugs are naturally mine. I'd be glad to hear about them. There are
   certainly word - size dependenceies here.
   
   Copyright (c) Matthew Dixon Cowles, <http://www.visi.com/~mdc/>.
   Distributable under the terms of the GNU General Public License
   version 2. Provided with no warranties of any sort.
   
   Original Version from Matthew Dixon Cowles:
	 -> ftp://ftp.visi.com/users/mdc/ping.py
   
   Rewrite by Jens Diemer:
	 -> http://www.python-forum.de/post-69122.html#69122
   
   Rewrite by Johannes Meyer:
	 -> http://www.python-forum.de/viewtopic.php?p=183720
   
   
   Revision history
   ~~~~~~~~~~~~~~~~
   
   November 1, 2010
   Rewrite by Johannes Meyer:
	-  changed entire code layout
	-  changed some comments and docstrings
	-  replaced time.clock() with time.time() in order
	   to be able to use this module on linux, too.
	-  added global __all__, ICMP_CODE and ERROR_DESCR
	-  merged functions "do_one" and "send_one_ping"
	-  placed icmp packet creation in its own function
	-  removed timestamp from the icmp packet
	-  added function "multi_ping_query"
	-  added class "PingQuery"
   
   May 30, 2007
   little rewrite by Jens Diemer:
	-  change socket asterisk import to a normal import
	-  replace time.time() with time.clock()
	-  delete "return None" (or change to "return" only)
	-  in checksum() rename "str" to "source_string"
   
   November 22, 1997
   Initial hack. Doesn't do much, but rather than try to guess
   what features I (or others) will want in the future, I've only
   put in what I need now.
   
   December 16, 1997
   For some reason, the checksum bytes are in the wrong order when
   this is run under Solaris 2.X for SPARC but it works right under
   Linux x86. Since I don't know just what's wrong, I'll swap the
   bytes always and then do an htons().
   
   December 4, 2000
   Changed the struct.pack() calls to pack the checksum and ID as
   unsigned. My thanks to Jerome Poincheval for the fix.
   
   
   Last commit info:
   ~~~~~~~~~~~~~~~~~
   $LastChangedDate: $
   $Rev: $
   $Author: $
"""

import socket
import struct

# From /usr/include/linux/icmp.h; your milage may vary.
ICMP_ECHO_REQUEST = 8 # Seems to be the same on Solaris.

ICMP_CODE = socket.getprotobyname('icmp')
ERROR_DESCR = {
	1: ' - Note that ICMP messages can only be '
	   'sent from processes running as root.',
	10013: ' - Note that ICMP messages can only be sent by'
		   ' users or processes with administrator rights.'
	}

__all__ = ['create_packet', 'do_one', 'verbose_ping', 'PingQuery',
		   'multi_ping_query']


def checksum(source_string):
	# I'm not too confident that this is right but testing seems to
	# suggest that it gives the same answers as in_cksum in ping.c.
	chksum = 0
	count_to = (len(source_string) / 2) * 2
	count = 0
	while count < count_to:
		this_val = ord(source_string[count + 1])*256+ord(source_string[count])
		chksum = chksum + this_val
		chksum = chksum & 0xffffffff # Necessary?
		count = count + 2
	if count_to < len(source_string):
		chksum = chksum + ord(source_string[len(source_string) - 1])
		chksum = chksum & 0xffffffff # Necessary?
	chksum = (chksum >> 16) + (chksum & 0xffff)
	chksum = chksum + (chksum >> 16)
	answer = ~chksum
	answer = answer & 0xffff
	# Swap bytes. Bugger me if I know why.
	answer = answer >> 8 | (answer << 8 & 0xff00)
	return answer


def create_packet(pid):
	"""Create a new echo request packet based on the given "pid"."""
	# Header is type (8), code (8), checksum (16), pid (16), sequence (16)
	header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, pid, 1)
	data = 192 * 'Q'
	# Calculate the checksum on the data and the dummy header.
	my_checksum = checksum(header + data)
	# Now that we have the right checksum, we put that in. It's just easier
	# to make up a new header than to stuff it into the dummy.
	header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0,
						 socket.htons(my_checksum), pid, 1)
	return header + data
