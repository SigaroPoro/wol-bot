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

    # Check firewall rules again (maybe UPnP added one we can see)
    cmds = [
        "show firewall_rule",
        "show firewall_exception",
        "show upnp",
    ]

    for cmd in cmds:
        print(f"\n--- {cmd} ---")
        channel.send(cmd + "\n")
        time.sleep(2)
        try:
            output = channel.recv(4096).decode('utf-8', errors='ignore')
            lines = [l for l in output.split('\r\n') if l.strip() and l.strip() != '>']
            for line in lines:
                print(f"  {line}")
        except:
            print("  (no output)")

except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
