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

# Find all buttons, inputs, forms
inputs = re.findall(r"<input[^>]*>", content)
for inp in inputs:
    if "button" in inp.lower() or "submit" in inp.lower() or "wol" in inp.lower() or "wake" in inp.lower():
        print(f"  {inp}")

# Find all onclick handlers
onclicks = re.findall(r'onclick="([^"]*)"', content)
for oc in onclicks:
    print(f"  onclick: {oc[:200]}")

# Find all forms
forms = re.findall(r"<form[^>]*action=\"([^\"]*)\"[^>]*>", content)
for f in forms:
    print(f"  form action: {f}")

# Find JavaScript functions that might send WOL
funcs = re.findall(r'function\s+(\w+)\s*\(', content)
for fn in funcs:
    print(f"  function: {fn}")

# Search for mac addresses and WOL keywords  
print("\nKeywords:")
for kw in ["wol", "wake", "WOL", "encender", "magic", "Magic", "MAC", "remoto"]:
    if kw.lower() in content.lower():
        for m in re.finditer(r'.{0,40}' + kw + r'.{0,40}', content, re.I):
            print(f"  [{kw}] {m.group().strip()[:150]}")
