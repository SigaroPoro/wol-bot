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

data2 = urllib.parse.urlencode({
    "rqUsername": "1234",
    "rqPasswd": "gcdXt5AB",
    "rqTimeout": "600"
}).encode()
req2 = urllib.request.Request(base + "/cgi-bin/cbCheckLogin.xml", data=data2, method="POST")
req2.add_header("Content-Type", "application/x-www-form-urlencoded")
opener.open(req2, timeout=10)

resp = opener.open(base + "/save.asp", timeout=5)
content = resp.read().decode("latin-1", errors="replace")
print(f"save.asp: {len(content)} bytes")

# Save config via the save button click handler (check save.js)
resp = opener.open(base + "/js/save.js?r=EN", timeout=5)
save_js = resp.read().decode("latin-1", errors="replace")
print(f"\nsave.js: {len(save_js)} bytes")

# Find where save does its work
for line in save_js.split('\n'):
    if any(kw in line.lower() for kw in ['save', 'post', 'cgi', 'xml', 'submit', 'click', 'btn']):
        print(f"  {line.strip()[:300]}")

# Try to save
print("\n\nAttempting save...")
save_data = urllib.parse.urlencode({"sessionKey": ""}).encode()
req = urllib.request.Request(
    base + "/cgi-bin/cbSaveConfig.xml",
    data=save_data, method="POST"
)
req.add_header("Referer", base + "/save.asp")
try:
    resp = opener.open(req, timeout=10)
    result = resp.read().decode("latin-1", errors="replace")
    print(f"Save result: {result}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print(e.read().decode("latin-1", errors="replace"))
