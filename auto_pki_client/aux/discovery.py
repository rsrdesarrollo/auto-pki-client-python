from zeroconf import ServiceBrowser, Zeroconf, ServiceStateChange
import time
import socket

def get_est_services(timeout=5):
    with ESTDiscovery() as est_discovery:
        time.sleep(timeout)

        return est_discovery.get_found_services()

class ESTServer (object):
    def __init__(self, address, port, weight, priority, server, properties=None):
        self.address = address
        self.port = port
        self.weight = weight
        self.priority = priority
        self.server = server
        self.properties = properties


class ESTDiscovery (object):

    _zeroconf = None
    _browser = None
    _found_services = []

    def __init__(self):
        self._zeroconf = Zeroconf()

    def __enter__(self):
        self._browser = ServiceBrowser(self._zeroconf, '_est._tcp.local.', handlers=[self._action_listener])
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._zeroconf.close()

    def _action_listener(self, zeroconf, service_type, name, state_change):
        if state_change == ServiceStateChange.Added:
            info = zeroconf.get_service_info(service_type, name, timeout=10000)
            if info:
                server = info.server.encode('ascii', 'ignore')
                srv = ESTServer(
                    address=socket.inet_ntoa(info.address),
                    port=info.port,
                    weight=info.weight,
                    priority=info.priority,
                    server=(server,server[:-1])[server[-1] == '.']
                )

                if info.properties:
                    srv.properties = info.properties

                self._found_services.append(srv)

    def get_found_services(self):
        return sorted(self._found_services, reverse=True, key=lambda srv: (srv.priority, srv.weight))
