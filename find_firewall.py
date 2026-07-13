import urllib.request, urllib.parse, http.cookiejar, re

base = "http://192.168.1.1"
password = "gcdXt5AB"

def xor_str(s, key=0x1f):
    return bytes(ord(c) ^ key for c in s)

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
opener.addheaders = [("User-Agent", "Mozilla/5.0")]

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

# Get te_puertos.asp for port forwarding rules
resp = opener.open(base + "/te_puertos.asp", timeout=5)
content = resp.read().decode("latin-1", errors="replace")
with open(r"C:\Users\rmonz\Desktop\wol-bot\te_puertos.html", "w", encoding="latin-1") as f:
    f.write(content)

print(f"te_puertos.asp: {len(content)} bytes")

# Search for packet filter, firewall, ACL keywords
for kw in ["packet", "Packet", "filter", "Filter", "firewall", "Firewall", 
           "ACL", "acl", "regla", "Regla", "permitir", "Allow", "allow",
           "forward", "Forward", "puerto", "puertos", "WAN"]:
    matches = [m for m in re.finditer(r'.{0,50}' + kw + r'.{0,50}', content, re.I)]
    if matches:
        print(f"\n--- {kw} ({len(matches)}) ---")
        for m in matches[:5]:
            print(f"  {m.group().strip()[:200]}")

# Find all CGI endpoints
cgis = re.findall(r'action="([^"]+\.cgi[^"]*)"', content)
print(f"\n\nCGIs:")
for c in cgis:
    print(f"  {c}")

# Find all forms
forms = re.findall(r'<form[^>]*>', content)
for f in forms[:10]:
    print(f"  form: {f[:200]}")
