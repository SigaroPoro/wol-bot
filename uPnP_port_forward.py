import miniupnpc

def add_upnp_port(ext_port, int_port, int_ip, protocol='UDP', desc='WOL'):
    upnp = miniupnpc.UPnP()
    upnp.discoverdelay = 200
    devices = upnp.discover()
    print(f"UPnP devices found: {devices}")

    upnp.selectigd()
    print(f"External IP: {upnp.externalipaddress()}")
    print(f"LAN addr: {upnp.lanaddr}")

    try:
        result = upnp.addportmapping(ext_port, protocol, int_ip, int_port, desc, '')
        if result:
            print(f"SUCCESS: Port {ext_port}/{protocol} -> {int_ip}:{int_port}")
        else:
            print("FAILED: Could not add port mapping")
    except Exception as e:
        print(f"Error: {e}")

    print("\nCurrent UPnP mappings:")
    i = 0
    while True:
        try:
            m = upnp.getgenericportmapping(i)
            if m is None:
                break
            print(f"  [{i}] {m[0]} -> {m[1]}:{m[2]} ({m[3]})")
            i += 1
        except:
            break
    print(f"Total: {i}")

if __name__ == '__main__':
    add_upnp_port(9, 9, '192.168.1.37', 'UDP', 'WOL')
