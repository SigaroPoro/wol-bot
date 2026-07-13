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

for page in ["te_red_local.asp", "me_configuracion_avanzada.asp", "te_mapa_red_local.asp"]:
    resp = opener.open(base + "/" + page, timeout=5)
    content = resp.read().decode("latin-1", errors="replace")
    print(f"\n{'='*60}")
    print(f"=== {page} ({len(content)} bytes) ===")
    print(f"{'='*60}")
    
    # Extract JavaScript variables
    vars = re.findall(r'var\s+(\w+)\s*=\s*([^;]+);', content)
    for name, val in vars:
        if any(k in name.lower() for k in ['device', 'dhcp', 'arp', 'reserv', 'static', 'mac', 'wol', 'wake']):
            print(f"  var {name} = {val[:200]}")
    
    # Find all form action and cgi-bin
    cgis = re.findall(r'cgi-bin/[^"\'<> ]+', content)
    print(f"  CGIs: {cgis}")
    
    # Search for WOL, DHCP reservation, static ARP keywords
    for kw in ['dhcp', 'arp', 'reserv', 'static lease', 'wol', 'wake', 'device', 'mac']:
        matches = [(m.start(), content[m.start():m.start()+200]) for m in re.finditer(kw, content, re.I)]
        if matches:
            print(f"\n  --- {kw} ({len(matches)} matches) ---")
            for idx, txt in matches[:3]:
                print(f"  [{idx}]: {txt}")
    
    # Save the full content
    safe_name = page.replace('.asp', '.html')
    with open(f"C:\\Users\\rmonz\\Desktop\\wol-bot\\{safe_name}", "w", encoding="latin-1") as f:
        f.write(content)
