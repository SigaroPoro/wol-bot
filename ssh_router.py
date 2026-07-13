import paramiko
import sys

host = "192.168.1.1"
port = 22
username = "1234"
password = "gcdXt5AB"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"Connecting to {host}:{port} as {username}...")
    client.connect(host, port=port, username=username, password=password, timeout=10)
    print("Connected!")

    # Try various commands to see what's available
    commands = [
        "whoami",
        "id",
        "cat /etc/version",
        "uname -a",
        "iptables -t nat -L PREROUTING -n 2>/dev/null | head -20",
        "iptables -t nat -L 2>/dev/null | head -20",
        "ls /etc/",
        "ls /etc/config/ 2>/dev/null || ls /cfg/ 2>/dev/null || ls /conf/ 2>/dev/null",
        "ps 2>/dev/null | head -20",
        "ifconfig",
        "ip addr show",
        "cat /proc/net/nf_conntrack 2>/dev/null | head -5",
        "iptables -t nat -A PREROUTING -p udp --dport 9 -j DNAT --to-destination 192.168.1.37:9 2>&1; iptables -I FORWARD -p udp -d 192.168.1.37 --dport 9 -j ACCEPT 2>&1",
    ]

    for cmd in commands:
        print(f"\n$ {cmd}")
        try:
            stdin, stdout, stderr = client.exec_command(cmd, timeout=5)
            out = stdout.read().decode('utf-8', errors='ignore').strip()
            err = stderr.read().decode('utf-8', errors='ignore').strip()
            if out:
                print(out)
            if err:
                print(f"STDERR: {err}")
        except Exception as e:
            print(f"Error: {e}")

except paramiko.AuthenticationException:
    print("AUTHENTICATION FAILED: Wrong password")
except paramiko.SSHException as e:
    print(f"SSH ERROR: {e}")
except Exception as e:
    print(f"ERROR: {e}")
finally:
    client.close()
