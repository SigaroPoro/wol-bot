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
    channel.settimeout(3)
    time.sleep(1)

    # Read initial prompt
    try:
        output = channel.recv(4096).decode('utf-8', errors='ignore')
        print(f"Initial: {repr(output)}")
    except:
        pass

    # Try different commands
    test_commands = [
        "",
        "?",
        "help",
        "system",
        "show",
        "list",
        "status",
        "version",
        "nat",
        "ip",
        "show version",
        "show nat",
        "show firewall",
        "show port",
        "show config",
        "running",
        "show running",
        "sys",
        "info",
        "show info",
    ]

    for cmd in test_commands:
        channel.send(cmd + "\n")
        time.sleep(1.5)
        try:
            output = channel.recv(4096).decode('utf-8', errors='ignore')
            if output.strip():
                print(f"Cmd '{cmd}': {repr(output)}")
        except:
            pass

    # Try to get help
    channel.send("?\n")
    time.sleep(2)
    try:
        output = channel.recv(8192).decode('utf-8', errors='ignore')
        print(f"Help output: {repr(output[:2000])}")
    except:
        pass

except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
