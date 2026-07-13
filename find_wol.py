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

pages = ["te_mapa_red_local.asp", "te_puertos.asp", "te_otras_funcionalidades.asp"]

for page in pages:
    try:
        resp = opener.open(base + "/" + page, timeout=5)
        content = resp.read().decode("latin-1", errors="replace")
        cgis = re.findall(r'action="([^"]+\.cgi[^"]*)"', content)
        if cgis:
            print(f"{page} CGIs: {cgis}")
        btns = re.findall(r'(?:value|onclick|name)="([^"]*)"', content)
        wol_btns = [b for b in btns if any(kw in b.lower() for kw in ["wol", "wake", "encender", "despertar", "remoto"])]
        if wol_btns:
            print(f"{page} WOL buttons: {wol_btns}")
        # Look for forms
        forms = re.findall(r'<form[^>]*>', content)
        if forms:
            for f in forms:
                print(f"{page} form: {f[:200]}")
    except Exception as e:
        print(f"{page}: ERROR {e}")
