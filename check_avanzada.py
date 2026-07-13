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

# Try to access avanzada.asp
resp = opener.open(base + "/avanzada.asp", timeout=5)
content = resp.read().decode("latin-1", errors="replace")
with open(r"C:\Users\rmonz\Desktop\wol-bot\avanzada.html", "w", encoding="latin-1") as f:
    f.write(content)
print(f"avanzada.asp: {len(content)} bytes")

# Find all pages and cgi
pages = re.findall(r'[\'"]([^\'"]*\.asp)[\'"]', content, re.I)
print(f"\nASP links: {sorted(set(pages))}")

cgis = re.findall(r'[\'"]([^\'"]*\.cgi[^\'"]*)[\'"]', content, re.I)
print(f"\nCGI links: {sorted(set(cgis))}")

# Find all form actions
forms = re.findall(r'action=[\'"]([^\'"]*)[\'"]', content, re.I)
print(f"\nForms: {sorted(set(forms))}")

# Find all functions
funcs = re.findall(r'function\s+(\w+)\s*\(', content)
print(f"\nFunctions: {sorted(set(funcs))}")

# Search for WOL
for kw in ['wol', 'wake', 'WOL', 'Wake', 'magic', 'encender', 'showdevice', 'devicelist', 'arp', 'ARP']:
    if kw in content:
        indices = [m.start() for m in re.finditer(kw, content)]
        for idx in indices[:3]:
            print(f"\n--- {kw} at [{idx}] ---")
            print(content[idx:idx+300])
