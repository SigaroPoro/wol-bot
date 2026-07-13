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

# Check all pools
for pool_0i in ["0", "1", "2"]:
    get_data = urllib.parse.urlencode({
        "rtm_cfg_dhcpv4_svr_pool_0i": pool_0i,
        "sessionKey": sessionKey
    }).encode()
    req_get = urllib.request.Request(
        base + "/cgi-bin/cbGetDhcpv4ServerPool.xml",
        data=get_data, method="POST"
    )
    req_get.add_header("Referer", base + "/dhcp.asp")
    resp_get = opener.open(req_get, timeout=10)
    result = resp_get.read().decode("latin-1", errors="replace")
    
    # Extract key fields
    pool_id = re.search(r"rtm_cfg_dhcpv4_svr_pool_id[^>]*>([^<]+)", result)
    ip_min = re.search(r"ipv4_addr_min[^>]*>([^<]+)", result)
    ip_max = re.search(r"ipv4_addr_max[^>]*>([^<]+)", result)
    opt60 = re.search(r"dhcpv4_opt60_value[^>]*>([^<]*)", result)
    ip_intf = re.search(r"ip_intf_id[^>]*>([^<]+)", result)
    
    print(f"\nPool index {pool_0i}:")
    print(f"  Pool ID: {pool_id.group(1) if pool_id else '?'}")
    print(f"  IP range: {ip_min.group(1) if ip_min else '?'} - {ip_max.group(1) if ip_max else '?'}")
    print(f"  Opt60: {opt60.group(1) if opt60 else '?'}")
    print(f"  IP Intf: {ip_intf.group(1) if ip_intf else '?'}")
    
    # Show first 500 chars of result
    print(f"  Full: {result[:500]}")
