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

    # Explore firewall_rule help
    cmds = [
        "set firewall_rule",
        "show firewall_rule",
        "show firewall_exception",
        "set firewall_exception",
        "set upnp",
        "set priority",
        "show device_info",
    ]

    for cmd in cmds:
        print(f"\n--- {cmd} ---")
        channel.send(cmd + "\n")
        time.sleep(2)
        try:
            output = channel.recv(8192).decode('utf-8', errors='ignore')
            print(output[:1000])
        except:
            pass

    # Check the full output of set firewall_rule
    print("\n--- Trying set firewall_rule with various params ---")
    variants = [
        "set firewall_rule help",
        "set firewall_rule ?",
        "set firewall_rule -h",
        "set firewall_rule --help",
    ]
    for v in variants:
        channel.send(v + "\n")
        time.sleep(1.5)
        try:
            output = channel.recv(4096).decode('utf-8', errors='ignore')
            if "Invalid" not in output:
                print(f"  {v}: {output[:500]}")
        except:
            pass

except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
