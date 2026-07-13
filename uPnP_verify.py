import miniupnpc

upnp = miniupnpc.UPnP()
upnp.discoverdelay = 200
upnp.discover()
upnp.selectigd()

print("=== Verify UDP port 9 mapping ===")
try:
    m = upnp.getspecificportmapping(9, 'UDP')
    print(f"Port 9 UDP: {m}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Verify TCP port 9 mapping ===")
try:
    m = upnp.getspecificportmapping(9, 'TCP')
    print(f"Port 9 TCP: {m}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== All mappings (raw) ===")
i = 0
while True:
    try:
        m = upnp.getgenericportmapping(i)
        if m is None:
            break
        print(f"  [{i}] ext_port={m[0]} proto={m[1]} int_client={m[2]} int_port={m[3]} desc={m[4]} enabled={m[5]} lease={m[6]}")
        i += 1
    except:
        break

print(f"\nTotal count from function: {upnp.getportmappingnumberofentries()}")
