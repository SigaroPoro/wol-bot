import miniupnpc

EXT_PORT = 43001  # Puerto fuera del rango de Moonlight
PROTO = 'UDP'
INT_IP = '192.168.1.37'
INT_PORT = 9
DESC = 'WOL'

upnp = miniupnpc.UPnP()
upnp.discoverdelay = 200
upnp.discover()
upnp.selectigd()

# Delete Moonlight's port 9 UDP mapping if it's there
try:
    m9 = upnp.getspecificportmapping(9, 'UDP')
    if m9 and 'Moonlight' in str(m9):
        upnp.deleteportmapping(9, 'UDP')
        print("Deleted Moonlight port 9 UDP mapping")
except:
    pass

# Add our WOL mapping on port 47990 (safe from Moonlight)
try:
    existing = upnp.getspecificportmapping(EXT_PORT, PROTO)
    if existing and existing[0] == INT_IP:
        print(f"Port {EXT_PORT}/UDP already mapped to {INT_IP}")
    else:
        if existing:
            upnp.deleteportmapping(EXT_PORT, PROTO)
        r = upnp.addportmapping(EXT_PORT, PROTO, INT_IP, INT_PORT, DESC, '', 0)
        print(f"Port {EXT_PORT}/UDP -> {INT_IP}:{INT_PORT} added: {r}")
except Exception as e:
    print(f"Error: {e}")

# Verify
m = upnp.getspecificportmapping(EXT_PORT, 'UDP')
print(f"Verification: {m}")
