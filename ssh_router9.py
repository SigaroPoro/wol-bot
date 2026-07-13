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

    # Try completely different approaches
    all_cmds = []

    # Maybe the CLI uses pipe or specific delimiters
    all_cmds += [
        "set firewall_rule add|name=wol|proto=udp|port=9|dest=192.168.1.37",
        "set firewall_rule add:name=wol:proto=udp",
        'set firewall_rule add "wol"',
    ]

    # Maybe the CLI needs exact parameters in the help message format
    # Looking at the "set" output: <firewall_rule> - these might be the actual CLI keywords
    all_cmds += [
        "config firewall_rule",
        "edit firewall_rule",
        "enable",
        "configure terminal",
    ]

    # Check if there's a separate nat command
    all_cmds += [
        "ip nat",
        "ip firewall",
        "port forwarding",
        "virtual-server",
        "virtual_server",
    ]

    # Let's check what "set reboot" does (since reboot is in the set list)
    all_cmds += [
        "set reboot",
        "set wifi",
        "set wifi0",
    ]

    for cmd in all_cmds:
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
