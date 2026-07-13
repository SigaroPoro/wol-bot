import urllib.request, urllib.parse, http.cookiejar, re

base = "http://192.168.1.1"
password = "gcdXt5AB"

def xor_str(s, key=0x1f):
    return bytes(ord(c) ^ key for c in s)

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(cookie_jar),
)
opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")]

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

resp = opener.open(base + "/te_wifi.asp", timeout=5)
content = resp.read().decode("latin-1", errors="replace")

# Save to file for analysis
with open(r"C:\Users\rmonz\Desktop\wol-bot\admin_page.html", "w", encoding="latin-1") as f:
    f.write(content)

print(f"Saved admin page: {len(content)} bytes")

# Look for interesting keywords
keywords = ["wol", "WOL", "wake", "Wake", "LAN", "firewall", "Firewall", "packet", "Packet", 
            "forward", "Forward", "NAT", "management", "Management", "config", "Config"]
for kw in keywords:
    count = content.lower().count(kw.lower())
    if count > 0:
        print(f"  '{kw}' found {count} times")

# Find all ASP pages referenced
all_asp = re.findall(r'"([^"]+\.asp)"', content)
print(f"\nAll ASP pages ({len(all_asp)}):")
for a in sorted(set(all_asp)):
    print(f"  {a}")

# Also get the header
resp = opener.open(base + "/te_header.asp", timeout=5)
header = resp.read().decode("latin-1", errors="replace")
header_links = re.findall(r'"([^"]+\.asp)"', header)
print(f"\nHeader ASP links ({len(header_links)}):")
for a in sorted(set(header_links)):
    print(f"  {a}")
with open(r"C:\Users\rmonz\Desktop\wol-bot\admin_header.html", "w", encoding="latin-1") as f:
    f.write(header)

# Find JavaScript/cgi endpoints
all_cgi = re.findall(r'"([^"]+\.cgi[^"]*)"', content)
print(f"\nCGI endpoints:")
for c in sorted(set(all_cgi)):
    print(f"  {c}")

# Find onclick handlers with known keywords
onclicks = re.findall(r'onclick="([^"]*wol[^"]*)"', content, re.I)
print(f"\nWOL onclick handlers: {onclicks}")
