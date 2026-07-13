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

    # Let's explore the firewall CLI more carefully
    cmds = [
        # Try different name formats
        "set firewall_rule add r1",
        "set firewall_rule add rule01",
        "set firewall_rule add rule-1",
        "set firewall_rule add rule_1",
        "set firewall_rule add rule1",
        "set firewall_rule add 01",
        "set firewall_rule add 100",
        "set firewall_rule add 0x01",
        "set firewall_rule add my_rule",
        "set firewall_rule add default",
        "set firewall_rule add any",
        "set firewall_rule add all",
        "set firewall_rule add *",
    ]

    for cmd in cmds:
        channel.send(cmd + "\n")
        time.sleep(1.5)
        try:
            output = channel.recv(4096).decode('utf-8', errors='ignore')
            lines = [l for l in output.split('\r\n') if l.strip() and l.strip() != '>']
            if lines:
                last = lines[-1]
                if 'Wrong' in last:
                    pass  # Skip wrong params
                elif 'Missing' in last:
                    pass
                else:
                    print(f"$ {cmd}")
                    for line in lines:
                        print(f"  {line}")
        except:
            pass

    # Try to find the correct syntax by exploring
    print("\n--- Trying with curly braces or special syntax ---")
    more = [
        "set firewall_rule add {name}",
        "set firewall_rule add 'name'",
        "set firewall_rule add 'rule1'",
        'set firewall_rule add "rule1"',
    ]
    for cmd in more:
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
