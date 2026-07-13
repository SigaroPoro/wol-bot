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
        "show arp",
        "show arp_table",
        "show arp_cache",
        "show mac_table",
        "show mac_address",
        "show bridge",
        "show lan_hosts",
        "show dhcp_leases",
        "show dhcp_reservation",
        "show wireless_clients",
        "show routing_table",
        "show route",
        "show wan_interface",
        "show lan_interface",
        "show network",
        "show device_info",
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
