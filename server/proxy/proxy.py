import datetime
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


server = SimpleXMLRPCServer(("localhost", 8018),
                            requestHandler=RequestHandler,
                            allow_none=False)

stats_server = xmlrpc.client.ServerProxy("http://localhost:8019")


def add_log(sname, func_duration):
    stats_server.add_to_db(sname, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           "{:.12f}".format(func_duration))
    return True


server.register_function(add_log, 'add_log')

print("Listening on port 8018...")
server.serve_forever()
