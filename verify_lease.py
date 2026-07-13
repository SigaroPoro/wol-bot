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

# Get details of static lease ID 1 in pool 0 (main LAN)
# First, list all static leases for pool 0
list_data = urllib.parse.urlencode({
    "rtm_cfg_dhcpv4_svr_pool_id": "0",
    "sessionKey": sessionKey
}).encode()
req_list = urllib.request.Request(
    base + "/cgi-bin/cbDhcpV4SvrPoolGetStatic.xml",
    data=list_data, method="POST"
)
req_list.add_header("Referer", base + "/dhcp.asp")
resp_list = opener.open(req_list, timeout=10)
list_result = resp_list.read().decode("latin-1", errors="replace")
print(f"Pool 0 static lease list: {list_result}")

# Get details for static ID 1 (from the create response, it said static_id=1)
detail_data = urllib.parse.urlencode({
    "rtm_dhcpv4_svr_pool_static_id": "1",
    "sessionKey": sessionKey
}).encode()
req_detail = urllib.request.Request(
    base + "/cgi-bin/cbDhcpV4SvrPoolGetStatic.xml",
    data=detail_data, method="POST"
)
req_detail.add_header("Referer", base + "/dhcp.asp")
resp_detail = opener.open(req_detail, timeout=10)
detail_result = resp_detail.read().decode("latin-1", errors="replace")
print(f"\nStatic lease ID 1 detail: {detail_result}")

# Also get the 0i-based detail (0i=0 means first entry)
detail_data0 = urllib.parse.urlencode({
    "rtm_cfg_dhcpv4_svr_pool_id": "0",
    "sessionKey": sessionKey
}).encode()
req_detail0 = urllib.request.Request(
    base + "/cgi-bin/cbDhcpV4SvrPoolGetStatic.xml",
    data=detail_data0, method="POST"
)
req_detail0.add_header("Referer", base + "/dhcp.asp")
resp_detail0 = opener.open(req_detail0, timeout=10)
detail_result0 = resp_detail0.read().decode("latin-1", errors="replace")
print(f"\nPool 0 entries: {detail_result0}")
