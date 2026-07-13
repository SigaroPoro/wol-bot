import miniupnpc

upnp = miniupnpc.UPnP()
upnp.discoverdelay = 200
upnp.discover()
upnp.selectigd()

# Delete the Moonlight mapping on port 9/UDP
print("--- Deleting Moonlight mapping on port 9 UDP ---")
try:
    m = upnp.getspecificportmapping(9, 'UDP')
    print(f"Existing: {m}")
    r = upnp.deleteportmapping(9, 'UDP')
    print(f"Delete result: {r}")
except Exception as e:
    print(f"Error: {e}")

# Add our WOL mapping on port 9/UDP
print("\n--- Adding WOL mapping on port 9 UDP -> 192.168.1.37:9 ---")
try:
    r = upnp.addportmapping(9, 'UDP', '192.168.1.37', 9, 'WOL', '')
    print(f"Add result: {r}")
except Exception as e:
    print(f"Error: {e}")

# Also clean up test mappings
print("\n--- Cleaning up test mappings ---")
for port in [7, 9999]:
    try:
        m = upnp.getspecificportmapping(port, 'UDP')
        if m:
            print(f"Deleting port {port}: {m}")
            upnp.deleteportmapping(port, 'UDP')
    except:
        pass

# List all mappings
print("\n--- Final mappings ---")
for i in range(20):
    try:
        m = upnp.getgenericportmapping(i)
        if m is None:
            break
        print(f"  [{i}] {m}")
    except:
        break

# Also try TCP for good measure
print("\n--- Adding WOL mapping on port 9 TCP -> 192.168.1.37:9 ---")
try:
    r = upnp.addportmapping(9, 'TCP', '192.168.1.37', 9, 'WOL-TCP', '')
    print(f"Add result: {r}")
except Exception as e:
    print(f"Error: {e}")
