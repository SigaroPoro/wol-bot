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
        "set static_arp",
        "set staticarp",
        "set arp_table",
        "set static_ip",
        "set dhcp_reservation",
        "set dhcp_static",
        "show lan_statistics",
        "show ethernet",
        "show statistics",
        "show nat_table",
        "show connections",
        "show firewall_session",
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
