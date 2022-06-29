import SimpleHTTPServer
import BaseHTTPServer
import json
import logging
import os

from SocketServer import ThreadingMixIn
import threading

import scaner
import launch

class HTMLGuiHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """Handler, GET command use the default behavior(file server), POST should be used for XmlhttpRequest and return the launcher and processes state"""
    def __init__(self, request, client_address, server, launcher):
        self.launcher = launcher
        SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_POST(self):
        """Handle a post request by returning the current state and the launcher time, and the frequency of all the modules"""
        #length = int(self.headers.getheader('content-length'))        
        #data_string = self.rfile.read(length)
        logging.debug("POST - %s:%s"%self.client_address)
        if "help.json" in self.path:
            self.wfile.write(json.dumps(vars(self.launcher.options)))
        elif 'supervision' in self.path:
            dic = {}
            scaner.Simulation_UpdateProcessInfo()
            process_infos = (scaner.APIProcessInfo*scaner.Simulation_getProcessNumber())()
            scaner.Simulation_getAllProcessInfo(process_infos)
            process_info = []
            for info in process_infos:
                id = scaner.Simulation_GetIdFromName(info.name)
                auto_launched = scaner.Simulation_IsProcessAutoLaunched(id)
                if auto_launched:
                    process_info.append({"name":info.name, "frequency":info.frequency, "state":scaner.state_string(info.state)})
            dic["process"] = process_info
            dic["launcher"] = {"state": self.launcher.state()}
            json_response = json.dumps(dic)
            logging.debug("WRITE - %(json_response)s"%locals())
            self.wfile.write(json_response)
        elif 'command.json' in self.path:
            length = self.headers['content-length']
            data = self.rfile.read(int(length))

            client_response = json.loads(data.decode())
            logging.debug("READ - %(client_response)s"%locals())
            command = client_response["command"]
            argument = client_response["arguments"]
            self.launcher.add_command(launch.LauncherCommand(command, argument))
            self.send_response(200)
        elif 'log.json' in self.path:
            self.wfile.write(json.dumps(self.launcher.get_log()))

    def log_message(self, format, *args):
        logging.info("%s - %s" %
                         (self.client_address[0],
                          format%args))

class HTMLGuiHandlerFactory:
    """A HTMLGuiHandler factory to set allow access to the launcher to the web response object"""
    def __init__(self, launcher):
        self.launcher = launcher
        pass

    def __call__(self, request, client_address, server):
        handler = HTMLGuiHandler(request, client_address, server, self.launcher)
        return handler

    
class ThreadedHTTPServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    """ This class allows to handle requests in separated threads.
        No further content needed, don't touch this. """

class HTMLGui(threading.Thread):
    """HTML5 GUi of the launch module.
    the displayed page is relative to the current working directory
    """
    def __init__(self, launcher):
        threading.Thread.__init__(self)
        self.handler = HTMLGuiHandlerFactory(launcher)
        self.stop_server = False
    def run(self):
        PORT = 9000
        httpd = ThreadedHTTPServer(("", PORT), self.handler)
        httpd.timeout = 1
        sa = httpd.socket.getsockname()
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        print "serving HTTP on", sa[0], "port", sa[1], "..."
        logging.info("serving HTTP on %s port %s", sa[0], sa[1])
        while not self.stop_server:
            httpd.handle_request()