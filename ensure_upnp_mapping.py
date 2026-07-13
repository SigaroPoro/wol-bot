import miniupnpc

EXT_PORT = 43001
PROTO = 'UDP'
INT_IP = '192.168.1.255'
INT_PORT = 9
DESC = 'WOL_cloud'

upnp = miniupnpc.UPnP()
upnp.discoverdelay = 200
upnp.discover()
upnp.selectigd()

try:
    existing = upnp.getspecificportmapping(EXT_PORT, PROTO)
    if existing and existing[0] == INT_IP:
        print(f"WOL mapping OK ({EXT_PORT}/UDP -> {INT_IP})")
    else:
        if existing:
            upnp.deleteportmapping(EXT_PORT, PROTO)
        upnp.addportmapping(EXT_PORT, PROTO, INT_IP, INT_PORT, DESC, '', 0)
        print(f"WOL mapping re-added ({EXT_PORT}/UDP -> {INT_IP}:{INT_PORT})")
except:
    upnp.addportmapping(EXT_PORT, PROTO, INT_IP, INT_PORT, DESC, '', 0)
    print(f"WOL mapping added ({EXT_PORT}/UDP -> {INT_IP}:{INT_PORT})")
