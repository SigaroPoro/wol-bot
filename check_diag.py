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

# Check diag/sw page
for page in ["diagsw.asp", "diag.asp"]:
    try:
        resp = opener.open(base + "/" + page, timeout=5)
        content = resp.read().decode("latin-1", errors="replace")
        print(f"\n=== {page} ({len(content)} bytes) ===")
        
        # Find forms and CGIs
        cgis = re.findall(r'[\'"]([^\'"]*\.(?:cgi|xml)[^\'"]*)[\'"]', content, re.I)
        print(f"CGIs: {cgis}")
        
        # Find buttons/forms
        for m in re.findall(r'<input[^>]*type="(?:button|submit)"[^>]*value="([^"]*)"', content, re.I):
            print(f"  button: {m}")
        
        # Print first 2000 chars
        print(f"  Preview: {content[:1500]}")
    except urllib.error.HTTPError as e:
        print(f"\n{page}: HTTP {e.code}")
