#!/usr/bin/env python

from __future__ import print_function

import logging
import sys
import time


from zeroconf import ServiceBrowser, Zeroconf

from rtmidi.midiutil import open_midiinput
from rtmidi.midiutil import open_midioutput

logging.basicConfig(filename="debug.log", level=logging.DEBUG)

debug = input("Enable debug file? (y/N) ")


class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        # forward midi message to the selected output
        midiout.send_message(message)
        logging.debug("[%s] @%0.6f %r" %
                      (self.port, self._wallclock, message))


class ZeroConfListener:
    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if debug == 'y':
            logging.debug("Service %s added, service info: %s" % (name, info))

    def update_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if debug == 'y':
            logging.debug("Service %s updated, service info: %s" %
                          (name, info))


# instanciate zeronconf
zeroconf = Zeroconf()
zero_listener = ZeroConfListener()

# browse for _apple-midi._udp service
browser = ServiceBrowser(zeroconf, "_apple-midi._udp.local.", zero_listener)

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

if debug == 'y':
    logging.debug("Attaching MIDI input callback handler.")

midiin.set_callback(MidiInputHandler(port_name))

if debug == 'y':
    logging.debug("Entering main loop. Press Control-C to exit.")

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
    zeroconf.close()
    del midiin
    del midiout
    del zeroconf
