import miniupnpc
import time

upnp = miniupnpc.UPnP()
upnp.discoverdelay = 200
upnp.discover()
upnp.selectigd()

# Delete Moonlight's mapping on port 9 UDP
try:
    existing = upnp.getspecificportmapping(9, 'UDP')
    print(f"Current port 9 mapping: {existing}")
    if existing:
        upnp.deleteportmapping(9, 'UDP')
        print("Deleted old mapping")
        time.sleep(1)
except Exception as e:
    print(f"Error deleting: {e}")

# Add our mapping
try:
    r = upnp.addportmapping(9, 'UDP', '192.168.1.37', 9, 'WOL', '', 0)
    print(f"Add result: {r}")
    m = upnp.getspecificportmapping(9, 'UDP')
    print(f"New mapping: {m}")
except Exception as e:
    print(f"Error adding: {e}")
