from wakeonlan import send_magic_packet
import socket

MAC = "10-FF-E0-65-C8-4C"

# Test 1: Send WOL to public IP on port 9 (tests port forwarding via UPnP)
print("=== Test 1: Send WOL to 88.20.72.39:9 ===")
try:
    send_magic_packet(MAC, ip_address="88.20.72.39", port=9)
    print("Sent to 88.20.72.39:9")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Send WOL to local broadcast (standard local WOL)
print("\n=== Test 2: Send WOL to 255.255.255.255:9 ===")
try:
    send_magic_packet(MAC, ip_address="255.255.255.255", port=9)
    print("Sent to 255.255.255.255:9")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Verify the UPnP mapping is alive
import miniupnpc
print("\n=== Test 3: Verify UPnP mapping ===")
upnp = miniupnpc.UPnP()
upnp.discoverdelay = 200
upnp.discover()
upnp.selectigd()
try:
    m = upnp.getspecificportmapping(9, 'UDP')
    print(f"Port 9 UDP mapping: {m}")
except Exception as e:
    print(f"Error: {e}")
