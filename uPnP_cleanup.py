import miniupnpc

upnp = miniupnpc.UPnP()
upnp.discoverdelay = 200
upnp.discover()
upnp.selectigd()

# Remove unwanted mappings
print("=== Removing TCP 9 mapping ===")
try:
    m = upnp.getspecificportmapping(9, 'TCP')
    print(f"Port 9 TCP exists: {m}")
    upnp.deleteportmapping(9, 'TCP')
    print("Deleted TCP 9")
except Exception as e:
    print(f"No TCP 9 or error: {e}")

# Verify UDP 9 is still there
print("\n=== Verify UDP 9 mapping ===")
try:
    m = upnp.getspecificportmapping(9, 'UDP')
    print(f"Port 9 UDP: {m}")
except Exception as e:
    print(f"Error: {e}")

# Keep only the WOL mapping, delete everything else that's not from Moonlight
# Actually, don't touch Moonlight mappings - they're needed for streaming
print("\n=== Done ===")
