import urllib.request, urllib.parse, http.cookiejar

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

# Fetch the full page
resp = opener.open(base + "/te_otras_funcionalidades.asp", timeout=5)
content = resp.read().decode("latin-1", errors="replace")
with open(r"C:\Users\rmonz\Desktop\wol-bot\te_funciones_full.html", "w", encoding="latin-1") as f:
    f.write(content)
print(f"Saved: {len(content)} bytes")
