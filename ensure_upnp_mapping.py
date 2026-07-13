import miniupnpc
import socket

EXT_PORT_UDP = 43001
EXT_PORT_TCP = 43002
INT_IP = "192.168.1.37"
INT_PORT_WOL = 9
INT_PORT_SMB = 445
DESC_WOL = "WOL_cloud"
DESC_STATUS = "WOL_status"

upnp = miniupnpc.UPnP()
upnp.discoverdelay = 200
upnp.discover()
upnp.selectigd()

def ensure_mapping(ext_port, proto, int_ip, int_port, desc):
    try:
        existing = upnp.getspecificportmapping(ext_port, proto)
        if existing and existing[0] == int_ip:
            return False
        if existing:
            upnp.deleteportmapping(ext_port, proto)
        upnp.addportmapping(ext_port, proto, int_ip, int_port, desc, "", 86400)
        return True
    except:
        upnp.addportmapping(ext_port, proto, int_ip, int_port, desc, "", 86400)
        return True

if ensure_mapping(EXT_PORT_UDP, "UDP", INT_IP, INT_PORT_WOL, DESC_WOL):
    print(f"WOL mapping added ({EXT_PORT_UDP}/UDP -> {INT_IP}:{INT_PORT_WOL})")
else:
    print(f"WOL mapping OK ({EXT_PORT_UDP}/UDP -> {INT_IP})")

if ensure_mapping(EXT_PORT_TCP, "TCP", "192.168.1.37", INT_PORT_SMB, DESC_STATUS):
    print(f"Status mapping added ({EXT_PORT_TCP}/TCP -> 192.168.1.37:{INT_PORT_SMB})")
else:
    print(f"Status mapping OK ({EXT_PORT_TCP}/TCP -> 192.168.1.37)")
