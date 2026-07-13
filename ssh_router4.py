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
    channel.recv(4096)

    # Explore configuration commands
    commands = [
        "set",
        "add",
        "del",
        "config",
        "configure",
        "create",
        "remove",
        "save",
        "commit",
        "apply",
        "default",
        "reset",
        "restart",
        "reload",
        "reboot",
        "ping",
    ]

    for cmd in commands:
        channel.send(cmd + "\n")
        time.sleep(1.5)
        try:
            output = channel.recv(4096).decode('utf-8', errors='ignore')
            out_clean = output.strip()
            if out_clean and out_clean != '>':
                print(f"Cmd '{cmd}': {out_clean[:500]}")
        except:
            pass

    # Check if there's a way to see port forwarding
    print("\n--- Trying show firewall_rule ---")
    channel.send("show firewall_rule\n")
    time.sleep(2)
    try:
        output = channel.recv(4096).decode('utf-8', errors='ignore')
        print(output[:1000])
    except:
        pass

    print("\n--- Trying show upnp ---")
    channel.send("show upnp\n")
    time.sleep(2)
    try:
        output = channel.recv(4096).decode('utf-8', errors='ignore')
        print(output[:1000])
    except:
        pass

    print("\n--- Trying show wan_interface ---")
    channel.send("show wan_interface\n")
    time.sleep(2)
    try:
        output = channel.recv(4096).decode('utf-8', errors='ignore')
        print(output[:1000])
    except:
        pass

except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
