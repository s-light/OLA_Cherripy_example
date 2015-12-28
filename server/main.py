#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
OLA Cherrypy example.

a simple example to demonstrate how to combine ola and cherrypy.

URI structure:
'/' --> static content (index.html)
'/api' api root
    '/channels' GET --> returns list with all channel values
        '/id' GET UPDATE (id = channel to set)
"""

# import socket
# import struct

import sys
import os


import pprint


# import json
# import time

import cherrypy
# import cherrypy.lib.jsontools
# from cherrypy.process.plugins import Monitor
from ola_plugin import OLAPlugin

from API import APIHandler

##########################################
version = '''27.12.2015 16:16 s-light'''
##########################################

dir_current = os.path.dirname(os.path.abspath(__file__))


class StaticFiles(object):

    """only here to have a class..."""

    pass
    # _cp_config = {
    #     'tools.staticdir.on': True,
    #     # 'tools.staticdir.root': dir_static,
    #     # 'tools.staticdir.dir': '',
    #     'tools.staticdir.index' : 'index.html'
    # }
#

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

    # https://docs.python.org/3/library/pprint.html
    pp = pprint.PrettyPrinter(
        indent=4,
        width=20,
        # compact=False
    )

    # config global server
    configServer = {
        'global': {
            # 'server.socket_host': '::',
            'server.socket_host': '0.0.0.0',
            # 'server.socket_host': '192.168.178.41',
            # 'server.socket_port': 8080,
            'server.socket_port': 80,
            'server.environment': 'development',
            # 'server.environment': 'production',
            'server.thread_pool': 20,
        }
    }
    cherrypy.config.update(configServer)

    # config static tool
    dir_static = os.path.join(dir_current, 'static')
    dir_logo = dir_static + '/img/logo'
    configStatic = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.root': dir_static,
            'tools.staticdir.dir': '',
            'tools.staticdir.index': 'index.html'
        },
        '/favicon.ico': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': dir_logo + '/logo.ico',
        },
        '/favicon.svg': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': dir_logo + '/logo.svg',
        },
        '/favicon.png': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': dir_logo + '/logo_500x500.png',
        },
    }
    # pp.pprint(configStatic)
    cherrypy.tree.mount(StaticFiles(), '', configStatic)

    ##########################################
    # API

    configAPI = {
        '/': {
            # 'tools.sessions.on': True,
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        },
    }
    APIHandlerInstance = APIHandler()
    cherrypy.tree.mount(APIHandlerInstance, '/api', configAPI)

    # enable ola plugin
    OLAPlugin(cherrypy.engine, 'Hello').subscribe()

    # start cherrypy
    print('')
    print('******************************************')
    print('')
    print('cherrypy server - start engine:')
    cherrypy.engine.start()
    cherrypy.engine.block()
