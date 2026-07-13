import urllib.request, urllib.parse, http.cookiejar, re, sys

base = "http://192.168.1.1"
password = "gcdXt5AB"

def xor_str(s, key=0x1f):
    return bytes(ord(c) ^ key for c in s)

def login(opener):
    resp = opener.open(base + "/te_wifi.asp", timeout=5)
    resp.read()
    user_xor = xor_str("1234")
    pass_xor = xor_str(password)
    data = urllib.parse.urlencode([
        ("loginUsername", user_xor.decode("latin-1")),
        ("loginPassword", pass_xor.decode("latin-1")),
        ("curWebPage", "/$page")
    ]).encode("latin-1")
    req = urllib.request.Request(base + "/cgi-bin/te_acceso_router.cgi", data=data, method="POST")
    req.add_header("Referer", base + "/te_wifi.asp")
    opener.open(req, timeout=10)

pages = [
    "te_otras_funcionalidades.asp",
    "te_puertos.asp",
    "me_configuracion_avanzada.asp",
    "te_mapa_red_local.asp",
    "te_red_local.asp",
]

for page in pages:
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    opener.addheaders = [("User-Agent", "Mozilla/5.0")]
    try:
        login(opener)
        resp = opener.open(base + "/" + page, timeout=5)
        content = resp.read().decode("latin-1", errors="replace")
        is_login = "acceso_content" in content
        print(f"{page}: {len(content)} bytes, login_page={is_login}")
        
        # Look for keywords
        for kw in ["wol", "Wake", "wake", "encender", "WOL", "remoto", "puerto", "forward"]:
            count = content.lower().count(kw.lower())
            if count > 0:
                print(f"  [{kw}] x{count}")
    except Exception as e:
        print(f"{page}: ERROR {e}")
