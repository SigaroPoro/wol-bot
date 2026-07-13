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
        # Help/query commands
        "help",
        "?",
        "syntax",
        "man",
        
        # Try netfilter/iptables directly
        "iptables -L",
        "iptables -t nat -L",
        "iptables -A INPUT -p udp --dport 9 -j ACCEPT",
        "iptables -t nat -A PREROUTING -p udp --dport 9 -j DNAT --to-destination 192.168.1.37:9",
        
        # Check system commands
        "system",
        "sh",
        "bash",
        "!/bin/sh",
        
        # Explore further
        "set firewall_rule add id 1",
        "set firewall_rule add 1 name wol",
        "set firewall_rule help",
        "set firewall_rule add --help",
        
        # Maybe it needs a different structured approach
        "set firewall_rule add rule table=filter chain=INPUT",
        
        # Check the FW version for search
        "show firmware_version",
        "show hardware_version",
        "show product_class",
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
