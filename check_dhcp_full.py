import urllib.request, urllib.parse, http.cookiejar, re

base = "http://192.168.1.1"
password = "gcdXt5AB"

def xor_str(s, key=0x1f):
    return bytes(ord(c) ^ key for c in s)

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
opener.addheaders = [("User-Agent", "Mozilla/5.0")]

# Login
resp = opener.open(base + "/te_wifi.asp", timeout=5)
resp.read()
user_xor = xor_str("1234")
pass_xor = xor_str(password)
data = urllib.parse.urlencode([
    ("loginUsername", user_xor.decode("latin-1")),
    ("loginPassword", pass_xor.decode("latin-1")),
    ("curWebPage", "/te_wifi.asp")
]).encode("latin-1")
req = urllib.request.Request(base + "/cgi-bin/te_acceso_router.cgi", data=data, method="POST")
req.add_header("Referer", base + "/te_wifi.asp")
opener.open(req, timeout=10)

# Advanced login
data2 = urllib.parse.urlencode({
    "rqUsername": "1234",
    "rqPasswd": "gcdXt5AB",
    "rqTimeout": "600"
}).encode()
req2 = urllib.request.Request(base + "/cgi-bin/cbCheckLogin.xml", data=data2, method="POST")
req2.add_header("Content-Type", "application/x-www-form-urlencoded")
opener.open(req2, timeout=10)

# Get DHCP page full content
resp = opener.open(base + "/dhcp.asp", timeout=5)
content = resp.read().decode("latin-1", errors="replace")

# Find all JavaScript variables and their values
lines = content.split('\n')
for i, line in enumerate(lines):
    if any(kw in line for kw in ['var ', 'static', 'Static', 'lease', 'Lease', 'reserv', 'Reserv', 'manual', 'Manual', 'fix', 'Fix']):
        print(f"{i}: {line[:500]}")

print("\n\n=== Looking for data structures ===")
# Find arrays and objects
for pattern in [r'var\s+(\w+)\s*=\s*\[.*?\];', r'var\s+(\w+)\s*=\s*\{.*?\};']:
    matches = re.findall(pattern, content, re.DOTALL)
    for m in matches[:20]:
        if len(m) < 500:
            print(f"  {m}")

# Find session key
sk = re.search(r"sessionKey\s*=\s*'(\d+)'", content)
if sk:
    print(f"\nSessionKey: {sk.group(1)}")

# Find all forms and their fields
forms = re.findall(r'<form[^>]*id="([^"]*)"[^>]*action="([^"]*)"[^>]*>(.*?)</form>', content, re.DOTALL)
for fid, action, form_html in forms:
    inputs = re.findall(r'<input[^>]*name="([^"]*)"[^>]*>', form_html)
    print(f"\nForm: {fid} -> {action}")
    print(f"  Inputs: {inputs}")
