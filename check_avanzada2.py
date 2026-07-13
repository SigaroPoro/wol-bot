import urllib.request, urllib.parse, http.cookiejar, re, ssl

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

# Also login via the advanced login
sUsername = "1234"
sPasswd = "gcdXt5AB"
data2 = urllib.parse.urlencode({
    "rqUsername": sUsername,
    "rqPasswd": sPasswd,
    "rqTimeout": "600"
}).encode()
req2 = urllib.request.Request(base + "/cgi-bin/cbCheckLogin.xml", data=data2, method="POST")
req2.add_header("Content-Type", "application/x-www-form-urlencoded")
opener.open(req2, timeout=10)

# Now access summary.asp (the advanced config main frame)
for page in ["summary.asp", "monu.asp", "top.asp", "bottom.asp"]:
    resp = opener.open(base + "/" + page, timeout=5)
    content = resp.read().decode("latin-1", errors="replace")
    print(f"\n{'='*60}")
    print(f"=== {page} ({len(content)} bytes) ===")
    
    if page == "summary.asp":
        with open(r"C:\Users\rmonz\Desktop\wol-bot\summary.html", "w", encoding="latin-1") as f:
            f.write(content)
    
    # Find all asp and cgi references
    refs = re.findall(r'[\'"]([^\'"]*\.(?:asp|cgi)[^\'"]*)[\'"]', content, re.I)
    for r in refs:
        print(f"  ref: {r}")
    
    # Print first 2000 chars
    print(f"\n  Content preview:")
    print(content[:2000])
