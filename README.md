# RTMIDI BRIDGE

> Allow my iDevice to send midi messages to bitwig using rtpmidi, avahi and ALSA virtual midi (snd-virmidi module)

For now I use Windows / iPad for all my music hobby. I discovered the fabulous tool [rtpMIDI](http://www.tobias-erichsen.de/software/rtpmidi.html) from Tobias Erichsen 
and use it to control bitwig from my iPad... But I am really fed up with Windows and want to make the switch to Linux... 
So I try to make something similar to Tobias Erichsen rtpMIDI in open source and for Linux...

## THINGS TO KNOW

- Bitwig uses ALSA MIDI, so it wont allow to select other MIDI ports than ALSA MIDI ports hence the use of snd-virmidi
- this is a WIP, I don't speak python and I am also a total noob in network / midi
- this developpement is for my personal use and is intended to work with bitwig and Ubuntu (20.04 LTS)
- the python code used is taken from various examples and I do not fully understand what is done ;-)

## DEPENDENCIES

###  UBUNTU

- if not provided by your distribution install avahi `sudo apt install avahi-daemon avahi-discover`
- install rtpmidi daemon
  - download last rtpmidid release from [here](https://github.com/davidmoreno/rtpmidid/releases)
  - run `sudo dpkg -i rtpmidid_xxxx_amd64.deb`

### PYTHON

- install [Zeroconf](https://pypi.org/project/zeroconf/) with `pip3 install zeroconf`
- install [rtmidi](https://github.com/SpotlightKid/python-rtmidi) with `pip3 install python-rtmidi`
  - python-rtmidi relies on libasound2-dev so pip3 will fail if this package is not installed

## USE IT

> personaly I uses [KB-1](https://apps.apple.com/us/app/kb-1-keyboard-suite/id1437919435) to send midi data to the computer but you can use [MIDI Wrench](https://apps.apple.com/us/app/midi-wrench/id589243566) which is free

- enable ALSA virtual midi module `sudo modprobe snd-virmidi`
- be sure to have an iDevice connected on the same network as your computer
- launch `rtmidi-bridge.py` (with my python install it is `python3 rtmidi-bridge.py`)
- you'll be asked for several questions... among them you'll have to choose the appropriate midi input / output (you should see your iDevice)

```bash
# answer yes if you want to log informations
Enable debug file? (y/N) y

Do you want to create a virtual MIDI input port? (y/N) N
Available MIDI ports:

[0] Midi Through:Midi Through Port-0 14:0
[1] Virtual Raw MIDI 1-0:VirMIDI 1-0 20:0
[2] Virtual Raw MIDI 1-1:VirMIDI 1-1 21:0
[3] Virtual Raw MIDI 1-2:VirMIDI 1-2 22:0
[4] Virtual Raw MIDI 1-3:VirMIDI 1-3 23:0
[5] rtpmidi pitrack-computer:Network 128:0
[6] rtpmidi pitrack-computer:iBidule 128:1 # this is the one for me

Select MIDI input port (Control-C to exit): 6
Do you want to create a virtual MIDI output port? (y/N) N
Available MIDI ports:

[0] Midi Through:Midi Through Port-0 14:0
[1] Virtual Raw MIDI 1-0:VirMIDI 1-0 20:0 # this is the one I use in bitwig
[2] Virtual Raw MIDI 1-1:VirMIDI 1-1 21:0
[3] Virtual Raw MIDI 1-2:VirMIDI 1-2 22:0
[4] Virtual Raw MIDI 1-3:VirMIDI 1-3 23:0
[5] rtpmidi pitrack-computer:Network 128:0
[6] RtMidiIn Client:rtpmidi pitrack-computer:Network 128:0 129:0

Select MIDI output port (Control-C to exit): 1

```

- you should be able to send midi data from your iDevice to bitwig

## KNOWN ISSUES / LIMITATIONS

- it takes a little time for midi input to be effective i.e. receive midi messages from iDevice
- relies on "WIP" projects (RTP MIDI is an Alpha software)
- uses two separate scripts...
- iDevice and comptuer need to be on the same network
- if there is to much latency you can use wifi hotspot on the computer and connect the iDevice to this wifi hotspot...

## TODO

- enable snd-virmidi with a persistent conf file in modules ?
- use a UI ?
- should be able to mesure latency
