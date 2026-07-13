import subprocess
import re

HOST = "192.168.1.1"
PORT = 22
PASS = "gcdXt5AB"

# We'll try various approaches to send a WOL packet from inside the router
# First, let's see what commands are available

commands = [
    # Check basic commands
    "help",
    "?" ,
    "show ?",
    "set ?",
    "show arp",
    "show wol",
    "show lan",
    "show device",
    # Try to find tools
    "toolbox",
    "diag",
    "ping",
    # Try shell escape
    "!",
    "sh",
    "bash",
    # Try sending WOL
    "wol send ?",
    "wol ?",
    "wake ?",
    # Try config
    "show running-config | include wol",
    "show running-config | include arp",
]

for cmd in commands:
    print(f"\n=== Trying: {cmd} ===")
    try:
        result = subprocess.run(
            ["sshpass", "-p", PASS, "ssh", "-o", "StrictHostKeyChecking=no", 
             "-o", "UserKnownHostsFile=NUL", "-o", "ConnectTimeout=5",
             f"admin@{HOST}", cmd],
            capture_output=True, text=True, timeout=10
        )
        out = (result.stdout + result.stderr)[:500]
        print(out if out else "(no output)")
    except FileNotFoundError:
        print("sshpass not found, trying plink...")
        break
    except subprocess.TimeoutExpired:
        print("(timed out)")
    except Exception as e:
        print(f"(error: {e})")
        break
