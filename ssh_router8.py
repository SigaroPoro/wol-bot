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

    cmds = [
        # Try simple names
        "set firewall_rule add wol",
        "set firewall_rule add test",
        "set firewall_rule add 1",
        "set firewall_rule add a",
        "set firewall_rule add rule_1",
        "set firewall_rule add wol udp 9 192.168.1.37 9",
        "set firewall_rule add wol protocol udp port 9 dest 192.168.1.37",
        "set firewall_rule add 1 udp 9 192.168.1.37 9",
        "set firewall_rule add 1 UDP 9 192.168.1.37",
        
        # Try with different order
        "set firewall_rule add enabled=1",
        "set firewall_rule add enabled 1",
        "set firewall_rule add wol enabled 1",
        
        # Try the other format - maybe it takes JSON or specific format
        "set firewall_rule add ext_port=9 int_port=9 int_ip=192.168.1.37 proto=udp",
        "set firewall_rule add src_port=9 dst_ip=192.168.1.37",
        "set firewall_rule add wan=9 lan=9 ip=192.168.1.37",
        
        # Maybe the parameters need to be in a specific order
        "set firewall_rule add 1 udp 192.168.1.37 9 9",
        "set firewall_rule add 1 192.168.1.37 9 udp",
        
        # Or maybe it needs to be set differently
        "set firewall_rule rule wol",
        "set firewall_rule rule_name wol",
        "set firewall_rule param wol",
        
        # Let's check the delete option too
        "set firewall_rule delete",
        "set firewall_rule delete 1",
        "set firewall_rule delete test",
        
        # Check enabled
        "set firewall_rule enabled",
        "set firewall_rule enabled 1",
    ]

    for cmd in cmds:
        channel.send(cmd + "\n")
        time.sleep(1.5)
        try:
            output = channel.recv(4096).decode('utf-8', errors='ignore')
            lines = [l for l in output.split('\r\n') if l.strip() and l.strip() != '>']
            if lines:
                print(f"$ {cmd}")
                for line in lines:
                    print(f"  {line}")
        except:
            pass

except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
