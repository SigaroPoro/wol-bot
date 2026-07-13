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

# Advanced login
data2 = urllib.parse.urlencode({
    "rqUsername": "1234",
    "rqPasswd": "gcdXt5AB",
    "rqTimeout": "600"
}).encode()
req2 = urllib.request.Request(base + "/cgi-bin/cbCheckLogin.xml", data=data2, method="POST")
req2.add_header("Content-Type", "application/x-www-form-urlencoded")
opener.open(req2, timeout=10)

pages = ["dhcp.asp", "arpstats.asp", "filtering.asp", "natportmap.asp", "natloopback.asp", "save.asp"]

for page in pages:
    resp = opener.open(f"{base}/{page}", timeout=5)
    content = resp.read().decode("latin-1", errors="replace")
    print(f"\n{'='*60}")
    print(f"=== {page} ({len(content)} bytes) ===")
    print(f"{'='*60}")
    
    # Find session key
    sk = re.search(r"sessionKey\s*=\s*'(\d+)'", content)
    if sk:
        print(f"  sessionKey = {sk.group(1)}")
    
    # Find JavaScript variables
    vars = re.findall(r'var\s+(\w+)\s*=\s*([^;]+);', content)
    for name, val in vars:
        val_short = val.strip()[:300]
        if any(k in name.lower() for k in ['arp', 'static', 'dhcp', 'reserv', 'lease', 'mac', 'wol', 'wake', 'host', 'filter', 'firewall', 'rule', 'forward', 'dmz', 'loopback']):
            print(f"  var {name} = {val_short}")
    
    # Find all form actions and CGIs
    cgis = re.findall(r'[\'"]([^\'"]*\.cgi[^\'"]*)[\'"]', content, re.I)
    if cgis:
        print(f"  CGIs: {sorted(set(cgis))}")
    
    # Print content preview
    print(f"\n  Content preview:")
    print(content[:1500])
