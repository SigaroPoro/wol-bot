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
sk_match = re.search(r"sessionKey\s*=\s*'(\d+)'", content)
sessionKey = sk_match.group(1) if sk_match else "0"

# Try different parameter combinations to get static lease details
for params, desc in [
    ({"rtm_cfg_dhcpv4_svr_pool_static_0i": "0", "sessionKey": sessionKey}, "0i=0"),
    ({"rtm_cfg_dhcpv4_svr_pool_id": "0", "rtm_cfg_dhcpv4_svr_pool_static_0i": "0", "sessionKey": sessionKey}, "pool=0 & 0i=0"),
    ({"rtm_cfg_dhcpv4_svr_pool_id": "0", "rtm_dhcpv4_svr_pool_static_id": "0", "sessionKey": sessionKey}, "pool=0 & static=0"),
    ({"rtm_dhcpv4_svr_pool_static_id": "0", "sessionKey": sessionKey}, "static=0"),
    ({"rtm_dhcpv4_svr_pool_static_id": "1", "sessionKey": sessionKey}, "static=1"),
    ({"rtm_dhcpv4_svr_pool_static_id": "-1", "sessionKey": sessionKey}, "static=-1"),
]:
    data_bytes = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(
        base + "/cgi-bin/cbDhcpV4SvrPoolGetStatic.xml",
        data=data_bytes, method="POST"
    )
    req.add_header("Referer", base + "/dhcp.asp")
    resp = opener.open(req, timeout=10)
    result = resp.read().decode("latin-1", errors="replace")
    # Pretty print
    import xml.dom.minidom
    try:
        parsed = xml.dom.minidom.parseString(result)
        pretty = parsed.toprettyxml(indent="  ")
        print(f"\n=== {desc} ===")
        print(pretty[:800])
    except:
        print(f"\n=== {desc} ===")
        print(result[:800])
