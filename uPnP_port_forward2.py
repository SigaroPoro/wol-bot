import miniupnpc

upnp = miniupnpc.UPnP()
upnp.discoverdelay = 200
upnp.discover()
upnp.selectigd()
print(f"External IP: {upnp.externalipaddress()}")
print(f"LAN addr: {upnp.lanaddr}")
print(f"WAN addr: {upnp.wanaddr}")

# Try addanyportmapping (allows any remote host)
print("\n--- Try addanyportmapping port 9 UDP -> 192.168.1.37:9 ---")
try:
    r = upnp.addanyportmapping(9, 'UDP', '192.168.1.37', 9, 'WOL', '')
    print(f"Result: {r}")
except Exception as e:
    print(f"Error: {e}")

# Try with external port 7 (also standard WOL)
print("\n--- Try addportmapping port 7 UDP -> 192.168.1.37:9 ---")
try:
    r = upnp.addportmapping(7, 'UDP', '192.168.1.37', 9, 'WOL-alt', '')
    print(f"Result: {r}")
except Exception as e:
    print(f"Error: {e}")

# Try with a non-standard external port
print("\n--- Try addportmapping port 9999 UDP -> 192.168.1.37:9 ---")
try:
    r = upnp.addportmapping(9999, 'UDP', '192.168.1.37', 9, 'WOL-9999', '')
    print(f"Result: {r}")
except Exception as e:
    print(f"Error: {e}")

# Check if there's a specific mapping on port 9
print("\n--- Check specific mapping port 9 UDP ---")
try:
    m = upnp.getspecificportmapping(9, 'UDP')
    print(f"Mapping: {m}")
except Exception as e:
    print(f"Error: {e}")

# List all
print("\n--- All current mappings ---")
i = 0
while True:
    try:
        m = upnp.getgenericportmapping(i)
        if m is None:
            break
        print(f"  [{i}] {m}")
        i += 1
    except:
        break
print(f"Total: {i}")
