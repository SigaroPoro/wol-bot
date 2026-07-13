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

# Get te_mapa_red_local.asp and extract scripts
resp = opener.open(base + "/te_mapa_red_local.asp", timeout=5)
content = resp.read().decode("latin-1", errors="replace")
scripts = re.findall(r"<script[^>]*>(.*?)</script>", content, re.DOTALL | re.I)

for s in scripts:
    # showdevice function
    if "showdevice" in s:
        print("=== showdevice function ===")
        print(s[:5000])
    # Logout function
    if "Logout" in s:
        print("\n=== Logout function ===")
        print(s[:1000])

# Check te_otras_funcionalidades.asp for WOL
resp = opener.open(base + "/te_otras_funcionalidades.asp", timeout=5)
other = resp.read().decode("latin-1", errors="replace")
scripts2 = re.findall(r"<script[^>]*>(.*?)</script>", other, re.DOTALL | re.I)

for s in scripts2:
    if "wol" in s.lower() or "wake" in s.lower() or "WOL" in s:
        print("\n=== WOL found in te_otras_funcionalidades ===")
        print(s[:2000])

# Try common CGI/WOL endpoints
wol_endpoints = [
    "/cgi-bin/te_wol.cgi",
    "/cgi-bin/te_wake.cgi",
    "/cgi-bin/te_wakeonlan.cgi",
    "/cgi-bin/wol.cgi",
    "/cgi-bin/wake.cgi",
    "/goform/wol",
    "/goform/wake",
    "/cgi-bin/te_wifirefresh.wl",
]

for ep in wol_endpoints:
    try:
        req = urllib.request.Request(base + ep)
        resp = opener.open(req, timeout=3)
        result = resp.read().decode("latin-1", errors="replace")[:200]
        print(f"\n{ep}: {resp.status} - {result}")
    except urllib.error.HTTPError as e:
        print(f"\n{ep}: HTTP {e.code}")
    except Exception as e:
        print(f"\n{ep}: {type(e).__name__}")
