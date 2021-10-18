# RTMIDI BRIDGE

> Allow my iDevice to send midi messages to bitwig using rtpmidi, avahi and ALSA virtual midi (snd-virmidi module)

Recently I discovered [rtpMIDI](http://www.tobias-erichsen.de/software/rtpmidi.html) from Tobias Erichsen and used it to control bitwig from my iPad... But:

- it only works on windows
- I am really fed up with Windows and want to make the switch to Linux... at least I want to try ;-)

So I made something similar (same purpose but way more simple) to Tobias Erichsen rtpMIDI but for Linux !

## THINGS TO KNOW

- I don't speak python and I am also a total noob in network / midi
- this developpement is for my personal use and is intended to work with an iDevice, bitwig and Ubuntu Studio (20.04)
- in the current state it works and it fulfill my needs...
- on iOS you can use the free [MIDI Wrench](https://apps.apple.com/us/app/midi-wrench/id589243566) tool to test midi messages

## DEPENDENCIES

- python 3.8 & pip3
- [pipenv](https://packaging.python.org/tutorials/managing-dependencies/#installing-pipenv)

###  UBUNTU

- if not provided by your distribution install avahi `sudo apt install avahi-daemon avahi-discover`
- install rtpmidi daemon
  - download last rtpmidid release from [here](https://github.com/davidmoreno/rtpmidid/releases)
  - run `sudo dpkg -i rtpmidid_xxxx_amd64.deb`

## INSTALL

- `python3 -m pip install -r requirements.txt`
- or use the release

## USE IT

- enable ALSA virtual midi module `sudo modprobe snd-virmidi` (Bitwig is ALSA MIDI only)
  - you can also add this module permanently by editing the modules.conf file (on Ubuntu Studio `/etc/modules-load.d/modules.conf`)
- be sure to have an iDevice connected on the same network as your computer
- launch `python3 rt-midi-cli.py` (with my python install it is `python3 python3 rt-midi-cli.py`)
  - you can also do `chmod +x rt-midi-cli.py` and then launch with `./rt-midi-cli.py`
- answer the questions (below is a full example on my computer)

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
[6] rtpmidi pitrack-computer:iPad 128:1 # this is the one for me

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

- you should be able to send midi data from your iDevice to Bitwig

## KNOWN ISSUES / LIMITATIONS

- it takes a little time for midi input to be effective i.e. receive midi messages from the iDevice
- quickly reapeating notes will result in timing issues (this issue also exist with rtpMIDI)
- relies on "WIP" projects (RTP MIDI is an Alpha software)
- iDevice and computer need to be on the same network
- if there is to much latency you can create a wifi hotspot on the computer and connect the iDevice to this wifi hotspot

## POSSIBLE IMPROVMENTS

- should be able to mesure latency
- should be able to send midi data from computer to iDevice
- use a UI
- make a standalone [release](http://www.pyinstaller.org/) basicaly `pyinstaller rt-midi-cli.py`

## RESOURCES

- PyQT tutorials https://pythonbasics.org/pyqt-input-dialog/
- update a dependecy `pip3 install python-rtmidi --upgrade`
- packaging application https://packaging.python.org/
- pipenv install libs here `~/.local/lib/pythonX.Y`
- `pipenv lock -r > requirements.txt`
