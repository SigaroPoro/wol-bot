import paramiko

host = "192.168.1.1"
port = 22
username = "1234"
password = "gcdXt5AB"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("Connecting...")
    client.connect(host, port=port, username=username, password=password, timeout=10)
    print("Connected!")

    # Try basic router CLI commands
    commands = [
        "help",
        "?",
        "ls",
        "echo test",
        "show",
        "show version",
        "show running-config",
        "config",
        "enable",
        "system",
        "status",
        "info",
        "version",
        "help",
        "exit",
        "quit",
        "nat",
        "firewall",
        "portforward",
        "iptables",
    ]

    for cmd in commands:
        print(f"\n$ {cmd}")
        try:
            stdin, stdout, stderr = client.exec_command(cmd, timeout=5)
            out = stdout.read().decode('utf-8', errors='ignore').strip()
            err = stderr.read().decode('utf-8', errors='ignore').strip()
            if out:
                print(out[:500])
            if err:
                print(f"ERR: {err[:200]}")
        except Exception as e:
            print(f"Exception: {e}")

    # Also try an interactive shell
    print("\n\nTrying interactive shell...")
    channel = client.invoke_shell()
    channel.settimeout(3)
    
    # Send help
    channel.send("help\n")
    import time
    time.sleep(2)
    output = channel.recv(4096).decode('utf-8', errors='ignore')
    print(f"Shell response: {output[:1000]}")

except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
