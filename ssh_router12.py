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
        # Check privilege levels
        "set privilege",
        "set privilege 0",
        "set privilege 1",
        "set privilege 2",
        "set privilege 3",
        "set level 0",
        "set level 1",
        
        # Show UPnP details
        "show upnp",
        
        # Try set upnp - maybe add port mapping via UPnP CLI
        "set upnp",
        "set upnp status enable",
        "set upnp add",
        "set upnp add 1",
        
        # Check other set options
        "set nat",
        "set port_forward",
        "set portforward",
        "set port_trigger",
        "set virtual_server",
        
        # Maybe we can set firewall_exception for WOL
        "set firewall_exception add rule_name WOL wan_port 9 lan_port 9 lan_ip 192.168.1.37 proto UDP",
        
        # Try config/commit type commands
        "apply",
        "commit",
        "save",
        "write",
        
        # Check for other hidden commands
        "list",
        "ls",
        "dir",
        
        # Try different shell access
        "!",
        "run",
        "exec",
        "execute",
    ]

    for cmd in cmds:
        channel.send(cmd + "\n")
        time.sleep(2)
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
