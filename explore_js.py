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

resp = opener.open(base + "/te_mapa_red_local.asp", timeout=5)
content = resp.read().decode("latin-1", errors="replace")

# Extract all JavaScript
scripts = re.findall(r"<script[^>]*>(.*?)</script>", content, re.DOTALL | re.I)

# Save JavaScript
with open(r"C:\Users\rmonz\Desktop\wol-bot\lan_map_js.txt", "w", encoding="latin-1") as f:
    for i, s in enumerate(scripts):
        f.write(f"\n\n=== SCRIPT {i} (len={len(s)}) ===\n")
        f.write(s)

print(f"Extracted {len(scripts)} scripts ({sum(len(s) for s in scripts)} chars)")

# Look for WOL, wake, magic keywords in scripts
for s in scripts:
    for kw in ["wol", "wake", "WOL", "magic", "Magic", "remoto", "encender", "despertar", "wakeonlan"]:
        if kw.lower() in s.lower():
            print(f"\n[{kw}] found in script {i}:")
            for m in re.finditer(r'.{0,50}' + kw + r'.{0,50}', s, re.I):
                print(f"  {m.group().strip()[:200]}")

# Look for device data array 
for s in scripts:
    if "deviceData" in s:
        print("\n=== deviceData found ===")
        print(s[:3000])
