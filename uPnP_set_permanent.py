import miniupnpc

upnp = miniupnpc.UPnP()
upnp.discoverdelay = 200
upnp.discover()
upnp.selectigd()

# Delete existing mapping
try:
    upnp.deleteportmapping(9, 'UDP')
    print("Deleted existing mapping")
except Exception as e:
    print(f"Delete error: {e}")

# Re-add with permanent lease (0)
print("=== Adding with permanent lease (0) ===")
try:
    r = upnp.addportmapping(9, 'UDP', '192.168.1.37', 9, 'WOL', '', 0)
    print(f"Result: {r}")
    m = upnp.getspecificportmapping(9, 'UDP')
    print(f"Mapping: {m}")
except Exception as e:
    print(f"Error: {e}")

# If permanent fails, re-add with 86400
if not r:
    print("=== Adding with 86400 lease ===")
    try:
        r = upnp.addportmapping(9, 'UDP', '192.168.1.37', 9, 'WOL', '', 86400)
        print(f"Result: {r}")
        m = upnp.getspecificportmapping(9, 'UDP')
        print(f"Mapping: {m}")
    except Exception as e:
        print(f"Error: {e}")
