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

resp = opener.open(base + "/dhcp.asp", timeout=5)
content = resp.read().decode("latin-1", errors="replace")
with open(r"C:\Users\rmonz\Desktop\wol-bot\dhcp_full.html", "w", encoding="latin-1") as f:
    f.write(content)
print(f"Saved: {len(content)} bytes")

# Print lines 230-320
for i, line in enumerate(content.split('\n')[229:320]):
    print(f"{i+230}: {line}")
