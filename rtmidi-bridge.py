#!/usr/bin/env python
#
# midiin_callback.py
#
"""Show how to receive MIDI input by setting a callback function."""

from __future__ import print_function
from zeroconf import ServiceBrowser, Zeroconf

import logging
import sys
import time

from rtmidi.midiutil import open_midiinput
from rtmidi.midiutil import open_midioutput

log = logging.getLogger('midiin_callback')
logging.basicConfig(level=logging.DEBUG)

class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        midiout.send_message(message)
        print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))


# CAN NOT BE ALL IN ONE SINCE ZEROCONF IS KEEPING LOGGING EVENTS TO TERMINAL
# zeroconf = Zeroconf()
# zc_listener = IDeviceListener()
# search for _apple-midi._udp devices on bonjour network
# browser = ServiceBrowser(zeroconf, "_apple-midi._udp.local.", zc_listener)

# Prompts user for MIDI input port, unless a valid port number or name
# is given as the first argument on the command line.
# API backend defaults to ALSA on Linux.
in_port = sys.argv[1] if len(sys.argv) > 1 else None

# Prompts user for MIDI output port, unless a valid port number or name
# is given as the first argument on the command line.
# API backend defaults to ALSA on Linux.
out_port = sys.argv[1] if len(sys.argv) > 1 else None

try:
    midiin, port_name = open_midiinput(in_port)
    midiout, port_name = open_midioutput(out_port)
except (EOFError, KeyboardInterrupt):
    sys.exit()

print("Attaching MIDI input callback handler.")
midiin.set_callback(MidiInputHandler(port_name))

print("Entering main loop. Press Control-C to exit.")
try:
    # Just wait for keyboard interrupt,
    # everything else is handled via the input callback.
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    midiout.close_port()
    # zeroconf.close()
    del midiin
    del midiout
    # del zeroconf
