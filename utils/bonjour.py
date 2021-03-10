from zeroconf import ServiceBrowser, Zeroconf

# https://pypi.org/project/zeroconf/

class ZeroConfListener:
    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print("Service %s added, service info: %s" % (name, info))

    def update_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print("Service %s updated, service info: %s" % (name, info))


zeroconf = Zeroconf()
zero_listener = ZeroConfListener()
# listen to _apple-midi._udp
browser = ServiceBrowser(zeroconf, "_apple-midi._udp.local.", zero_listener)
try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()


