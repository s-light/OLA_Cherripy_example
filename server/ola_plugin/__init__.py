#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
CherryPy Plugin for ola.

connect with ola
"""

import sys

import cherrypy
from cherrypy.process import wspbus, plugins

import time
import threading

import array
import socket
from ola.ClientWrapper import ClientWrapper
from ola.OlaClient import OLADNotRunningException

##########################################
version = '''27.12.2015 16:16 s-light'''
##########################################


class OLAPlugin(plugins.SimplePlugin):

    """creates a bridge between cherrypy and ola."""

    def __init__(self, bus, myname):
        """connect to ola and initialize channel values."""
        plugins.SimplePlugin.__init__(self, bus)
        self.myname = myname
        self.channel_names = {
            'channel_request': 'ola-channel-request',
            'channel_response': 'ola-channel-response',
            'channel_set': 'ola-channel-set',
        }

        # ola things
        self.ola_connection = OLAThread()
        self.channels = self.ola_connection.channels

    def start(self):
        """Starting up OLA Plugin."""
        self.bus.log('Starting up OLA Plugin.')
        self.bus.subscribe(
            self.channel_names['channel_request'],
            self.handle_channel
        )
        self.bus.subscribe(
            self.channel_names['channel_set'],
            self.handle_channel_set
        )
        self.ola_connection.start()

    def stop(self):
        """Stopping down OLA Plugin."""
        self.bus.log('Stopping down OLA Plugin.')
        self.bus.unsubscribe(
            self.channel_names['channel_request'],
            self.handle_channel
        )
        self.bus.unsubscribe(
            self.channel_names['channel_set'],
            self.handle_channel_set
        )
        self.ola_connection.disconnect()
        # wait for thread to finish.
        self.ola_connection.join()

    def handle_channel(self, channel_id=None, entity=None):
        """handle channel bus request."""
        # print("handle_channel:")
        # print("\tchannel_id:{}".format(channel_id))
        # print("\tentitiy:{}".format(entity))
        if channel_id:
            if channel_id.isdigit():
                # if int(channel_id) < 512:
                # if (0 < int(channel_id)) & (int(channel_id) < 512):
                if 0 <= int(channel_id) < 512:
                    # print("int(channel_id): {}".format(int(channel_id)))
                    channel_value = self.channels[int(channel_id)]
                    return channel_value
                else:
                    return -1

        else:
            return self.channels

    def handle_channel_set(self, channel_id=None, channel_value=None):
        """handle channel set bus request."""
        # print("handle_channel_set:")
        # print("\tchannel_id:{}".format(channel_id))
        # print("\tchannel_value:{}".format(channel_value))
        if channel_id is not None:
            # try:
            print("int(channel_id): {}".format(int(channel_id)))
            # now please set the value of the given channel to new value..
            if int(channel_id) > 512:
                channel_id = 512
            if int(channel_id) < 0:
                channel_id = 0
            if int(channel_value) > 255:
                channel_value = 255
            if int(channel_value) < 0:
                channel_value = 0
            self.channels[int(channel_id)] = int(channel_value)
            # send new values
            self.ola_connection.dmx_send_frame()
            return self.channels[int(channel_id)]
            # except:
            #     return -1
        else:
            # return error
            return -1

##########################################
# ola things
##########################################


class OLAThread(threading.Thread):

    """connect to olad in a threaded way."""

    def __init__(self, universe=0, channel_count=512):
        """create new OLAThread instance."""
        super(OLAThread, self).__init__()

        self.flag_connected = False
        self.flag_wait_for_ola = False
        self.wrapper = None
        self.client = None

        self.universe = universe
        self.channel_count = channel_count
        self.channels = array.array('B')
        # self.channels = []

        # init byte array
        # index 0 is not used.
        # self.channels.append(255)
        # for channel_index in range(1, self.channel_count+1):
        for channel_index in range(0, self.channel_count):
            # print(channel_index)
            # temp_value = (channel_index-1) % 256
            temp_value = (channel_index) % 256
            # print("{}:{}".format(channel_index, temp_value))
            self.channels.append(temp_value)

        print(self.channels)

    def dmx_send_frame(self):
        """send data as one dmx frame."""
        if self.flag_connected:
            try:
                temp_array = array.array('B')
                for channel_index in range(0, self.channel_count):
                    temp_array.append(self.channels[channel_index])

                # print("temp_array:{}".format(temp_array))
                # print("send frame..")
                self.wrapper.Client().SendDmx(
                    self.universe,
                    # self.channels,
                    temp_array,
                    self.dmx_send_callback
                )
                # print("done.")
            except OLADNotRunningException:
                self.wrapper.Stop()
                print("olad not running anymore.")
        else:
            # throw error
            pass

    def dmx_send_callback(self, state):
        """react on ola state."""
        if not state.Succeeded():
            self.wrapper.Stop()
            print("warning: dmxSent does not Succeeded.")
        else:
            print("send frame succeeded.")

    def run(self):
        """run thread and connect to ola."""
        self.connect()

    def connect(self):
        """connect to ola."""
        print("waiting for olad....")
        self.flag_connected = False
        self.flag_wait_for_ola = True
        while (not self.flag_connected) & self.flag_wait_for_ola:
            try:
                # print("get wrapper")
                self.wrapper = ClientWrapper()
            except OLADNotRunningException:
                time.sleep(0.5)
            else:
                self.flag_connected = True

        if self.flag_connected:

            self.flag_wait_for_ola = False
            print("get client")
            self.client = self.wrapper.Client()

            print("run ola wrapper.")
            try:
                self.wrapper.Run()
            except KeyboardInterrupt:
                self.wrapper.Stop()
                print("\nstopped")
            except socket.error as error:
                print("connection to OLAD lost:")
                print("   error: " + error.__str__())
                self.flag_connected = False
            # except Exception as error:
            #     print(error)
        else:
            print("\nstopped waiting for olad.")

    def disconnect(self):
        """stop ola wrapper."""
        if self.flag_wait_for_ola:
            print("stop search for ola wrapper.")
            self.flag_wait_for_ola = False
        if self.flag_connected:
            print("stop ola wrapper.")
            self.wrapper.Stop()

################################################################
if __name__ == '__main__':
    print('')
    print(42*'*')
    print('Python Version: {}'.format(sys.version))
    print(42*'*')
    print('')
    print(__doc__)
    print('')
    print(42*'*')
    print('version: {}'.format(version))
    print(42*'*')
    print('')

    print("test not implemented.")
    print("")
#
