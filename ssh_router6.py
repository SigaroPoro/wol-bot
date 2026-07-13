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

    # Try firewall_rule with add parameter
    cmds = [
        "set firewall_rule add",
        "set firewall_rule add 1",
        "set firewall_rule add tcp",
        "set firewall_rule add 192.168.1.37 9 udp",
        "set firewall_rule add wan_port=9 lan_ip=192.168.1.37 lan_port=9 proto=udp",
        "set firewall_rule enabled=1 add=1",
        "set firewall_rule add rule1",
        
        # Try other syntaxes
        "set firewall_exception add",
        "set firewall_exception add 1",
        
        # Check if there's a different way
        "add firewall_rule",
        "configure firewall_rule",
        
        # Try set with more details
        "set priority add",
        "set priority ip_port",
    ]

    for cmd in cmds:
        print(f"\n--- {cmd} ---")
        channel.send(cmd + "\n")
        time.sleep(2)
        try:
            output = channel.recv(4096).decode('utf-8', errors='ignore')
            print(output[:500])
        except:
            pass

except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
