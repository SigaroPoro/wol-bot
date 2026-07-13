import paramiko
import time

host = "192.168.1.1"
port = 22
username = "1234"
password = "gcdXt5AB"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(host, port=port, username=username, password=password, timeout=10)
    channel = client.invoke_shell()
    channel.settimeout(5)
    time.sleep(1)
    channel.recv(4096)

    # Try various syntax patterns for firewall_rule add
    cmds = [
        "set firewall_rule add name WOL",
        "set firewall_rule add name WOL protocol udp wan_port 9 lan_port 9 lan_ip 192.168.1.37 enabled 1",
        "set firewall_rule add name WOL dest_port 9 dest_ip 192.168.1.37 proto udp",
        "set firewall_rule add WOL proto udp port 9 dest 192.168.1.37",
        "set firewall_rule add rule_name WOL proto udp port 9 dest 192.168.1.37",
        "set firewall_rule add name=WOL proto=udp wan_port=9 lan_ip=192.168.1.37",
        "set firewall_rule add WOL udp 9 192.168.1.37 9",
        "set firewall_rule add WOL UDP 9 192.168.1.37",
        "set firewall_rule add WOL 9 UDP 192.168.1.37 9",
        
        # Try with different quote styles
        'set firewall_rule add name "WOL"',
        
        # Check the syntax for firewall_exception
        "set firewall_exception add rule_name WOL",
        "set firewall_exception add WOL",
    ]

    for cmd in cmds:
        print(f"\n--- {cmd} ---")
        channel.send(cmd + "\n")
        time.sleep(2)
        try:
            output = channel.recv(4096).decode('utf-8', errors='ignore')
            lines = [l for l in output.split('\r\n') if l.strip()]
            for line in lines:
                print(line)
        except:
            pass

except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
