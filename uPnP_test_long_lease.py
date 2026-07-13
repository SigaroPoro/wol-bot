import miniupnpc

upnp = miniupnpc.UPnP()
upnp.discoverdelay = 200
upnp.discover()
upnp.selectigd()

# Test longer lease (0 = permanent)
print("=== Testing permanent lease (0) ===")
try:
    r = upnp.addportmapping(9, 'UDP', '192.168.1.37', 9, 'WOL', '', 0)
    print(f"Lease 0 result: {r}")
    m = upnp.getspecificportmapping(9, 'UDP')
    print(f"Mapping: {m}")
except Exception as e:
    print(f"Error: {e}")
