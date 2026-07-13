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

resp = opener.open(base + "/te_otras_funcionalidades.asp", timeout=5)
content = resp.read().decode("latin-1", errors="replace")

# Find the WOL form/submit
for pattern in ["te_", "wol", "WOL", "Wake", "wake", "cgi", "CGI", "submit", "action", "showdevice",
                "packet", "magic", "dispositivo", "encender", "wakeonlan", "func"]:
    indices = [m.start() for m in re.finditer(pattern, content, re.I)]
    for idx in indices[:5]:
        print(f"[{idx}:{idx+100}] {content[idx:idx+200]}")
        print()

# Find all forms
forms = re.findall(r'<form[^>]*action="([^"]*)"[^>]*>', content)
print(f"\nForms: {forms}")

# Find all cgi-bin references
cgis = re.findall(r'cgi-bin/[^"\'<> ]+', content)
print(f"\nCGIs: {cgis}")

# Find all functions
funcs = re.findall(r'function\s+(\w+)\s*\(', content)
print(f"\nFunctions: {funcs}")

# Find onclick handlers
onclicks = re.findall(r'onclick\s*=\s*"([^"]*)"', content)
for oc in onclicks:
    print(f"onclick: {oc}")

# Find hrefs
hrefs = re.findall(r'href=[\'"]([^\'"]+)[\'"]', content)
for h in hrefs:
    if 'wol' in h.lower() or 'cgi' in h.lower():
        print(f"href: {h}")

# Search specifically for showdevice and WOL-related JS
for line in content.split('\n'):
    if any(kw in line.lower() for kw in ['wol', 'showdevice', 'wake', 'magic', 'encender', 'packet']):
        print(f"\nWOL-RELATED LINE: {line[:500]}")
