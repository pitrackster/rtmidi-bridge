from __future__ import print_function

import sys
import os
import datetime
import time
import rtmidi
from PyQt5.QtWidgets import *
from zeroconf import ServiceBrowser, Zeroconf
from rtmidi.midiutil import open_midiinput
from rtmidi.midiutil import open_midioutput
from subprocess import Popen, PIPE


class ZeroConfListener:
    def remove_service(self, zeroconf, type, name):
        MainWindow.addLog("Service %s removed" % (name))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        MainWindow.addLo("Service %s added, service info: %s" % (name, info))

    def update_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        MainWindow.addLog("Service %s updated, service info: %s" % (name, info))

class MidiInputHandler(object):
    def __init__(self, port, midiout):
        self.port = port
        self._wallclock = time.time()
        self.midiout = midiout

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        # forward midi message to the selected output
        self.midiout.send_message(message)
        MainWindow.addLog("[%s] @%0.6f %r" % (self.port, self._wallclock, message))

class MainWindow(QMainWindow):   

    def __init__(self):
        super(MainWindow, self).__init__()
        self.showLogs = True
        self.midiout = rtmidi.MidiOut()
        available_out_ports = self.midiout.get_ports()
        self.midiin = rtmidi.MidiIn()
        available_in_ports = self.midiin.get_ports()

        # WIDGETS 

        # top groupbox (utils)
        utilsGroupbox = QGroupBox("Utils")
        utilsWidgetContainer = QHBoxLayout()
        utilsGroupbox.setLayout(utilsWidgetContainer)        

        # utils widgets
        # show logs checkbox 
        showLogsCheckBox = QCheckBox("Show logs")
        showLogsCheckBox.setChecked(self.showLogs)
        showLogsCheckBox.toggled.connect(self.setShowLogs)

        btnRefreshMidiSources = QPushButton("Refresh available midi devices")
        btnRefreshMidiSources.clicked.connect(self.refreshMidiDevices)

        # create virtual midi ports btn
        btnCreateVirtualMidi = QPushButton("Create virtual ALSA midi ports")
        btnCreateVirtualMidi.clicked.connect(self.createAlsaVirtualMidiPorts)
        # remove virtual midi ports btn
        btnRemoveVirtualMidi = QPushButton("Remove virtual ALSA midi ports")
        btnRemoveVirtualMidi.clicked.connect(self.removeAlsaVirtualMidiPorts)

        utilsWidgetContainer.addWidget(showLogsCheckBox)
        utilsWidgetContainer.addWidget(btnRefreshMidiSources)
        utilsWidgetContainer.addWidget(btnCreateVirtualMidi)
        utilsWidgetContainer.addWidget(btnRemoveVirtualMidi)        

        # MIDI SOURCES (BRIDGE-IN)
        midiInGroupbox = QGroupBox("Select midi bridge source")
        midiInGroupboxContainer = QHBoxLayout()
        midiInGroupbox.setLayout(midiInGroupboxContainer)
    
        self.comboIn = QComboBox()        
        for min in available_in_ports:
            self.comboIn.addItem(min)
        self.comboIn.adjustSize()
        self.comboIn.activated[int].connect(self.selectMidiIn)        

        midiInGroupboxContainer.addWidget(self.comboIn)
        midiInGroupbox.setLayout(midiInGroupboxContainer)    

        # MIDI DEST (BRIDGE-OUT)
        midiOutGroupbox = QGroupBox("Select midi bridge destination")
        midiOutGroupboxContainer = QHBoxLayout()
        midiOutGroupbox.setLayout(midiOutGroupboxContainer)
        self.comboOut = QComboBox()
        for out in available_out_ports:
            self.comboOut.addItem(out)
        
        self.comboOut.adjustSize()
        self.comboOut.activated[int].connect(self.selectMidiOut)

        midiOutGroupboxContainer.addWidget(self.comboOut)
        midiOutGroupbox.setLayout(midiOutGroupboxContainer)       

        logsGoupbox = QGroupBox("Logs")
        logsGoupboxContainer = QVBoxLayout()
        self.textArea = QTextEdit()
        self.textArea.setReadOnly(True)
        logsGoupboxContainer.addWidget(self.textArea)
        logsGoupbox.setLayout(logsGoupboxContainer)
  
        grid = QGridLayout()
        grid.addWidget(utilsGroupbox, 0, 0)
        grid.addWidget(midiInGroupbox, 1, 0)
        grid.addWidget(midiOutGroupbox, 2, 0)
        grid.addWidget(logsGoupbox, 3, 0)

        widget = QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)
        self.setWindowTitle("RT-MIDI-BRIDGE UI")
        self.show()

    def addLog(self, msg):
        if(self.showLogs):
            text = datetime.date.fromtimestamp(time.time()).strftime("%d/%m/%Y, %H:%M:%S") + " - " + msg
            self.textArea.append(text)

    def selectMidiOut(self, index):
        self.midiout, port_name = open_midioutput(index)
        self.addLog ("Selected MIDI source %s with %s" % (port_name, self.midiout))        

    def selectMidiIn(self, index):
        self.midiin, port_name = open_midiinput(index)
        self.addLog("Selected MIDI destination %s" % (port_name))
        self.midiin.set_callback(MidiInputHandler(port_name, self.midiout))

    def setShowLogs(self):
        sender = self.sender()
        self.showLogs = sender.isChecked()
        if(sender.isChecked() == False):
            self.textArea.setText("")

    def refreshMidiDevices(self):
        available_in_ports = self.midiin.get_ports()
        available_out_ports = self.midiout.get_ports()
        self.comboIn.clear()
        self.comboOut.clear()
        self.addLog("Refreshing midi devices")
        for midiIn in available_in_ports:            
            self.comboIn.addItem(midiIn)
        for out in available_out_ports:
            self.comboOut.addItem(out)

    def createAlsaVirtualMidiPorts(self):
        command = 'modprobe snd-virmidi'.split()
        password, ok = QInputDialog.getText(self, 'This action requires root privileges', 'Enter sudo password:', QLineEdit.Password)
        if ok:
            p = Popen(['sudo', '-S'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
            p.communicate(password + '\n')[1]
        
    
    def removeAlsaVirtualMidiPorts(self):
        command = 'modprobe -r snd-virmidi'.split()
        password, ok = QInputDialog.getText(self, 'This action requires root privileges', 'Enter sudo password:', QLineEdit.Password)
        if ok:
            p = Popen(['sudo', '-S'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
            p.communicate(password + '\n')[1]
        os.system("modprobe -r snd-virmidi")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    # instanciate zeronconf
    zeroconf = Zeroconf()
    zero_listener = ZeroConfListener()

    # browse for _apple-midi._udp service
    browser = ServiceBrowser(zeroconf, "_apple-midi._udp.local.", zero_listener)
    sys.exit(app.exec_())
