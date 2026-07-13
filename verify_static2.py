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

# List static leases for pool 1
for pool_id in ["1", "0", "2"]:
    list_data = urllib.parse.urlencode({
        "rtm_cfg_dhcpv4_svr_pool_id": pool_id,
        "sessionKey": sessionKey
    }).encode()
    req = urllib.request.Request(
        base + "/cgi-bin/cbDhcpV4SvrPoolGetStatic.xml",
        data=list_data, method="POST"
    )
    req.add_header("Referer", base + "/dhcp.asp")
    resp = opener.open(req, timeout=10)
    result = resp.read().decode("latin-1", errors="replace")
    print(f"\nPool {pool_id}: {result}")

# Also try without pool_id
list_data = urllib.parse.urlencode({"sessionKey": sessionKey}).encode()
req = urllib.request.Request(
    base + "/cgi-bin/cbDhcpV4SvrPoolGetStatic.xml",
    data=list_data, method="POST"
)
req.add_header("Referer", base + "/dhcp.asp")
resp = opener.open(req, timeout=10)
result = resp.read().decode("latin-1", errors="replace")
print(f"\nNo pool_id: {result}")
