import urllib.request, urllib.parse, http.cookiejar, re

base = "http://192.168.1.1"
password = "gcdXt5AB"
MAC = "10:FF:E0:65:C8:4C"
IP = "192.168.1.37"

def xor_str(s, key=0x1f):
    return bytes(ord(c) ^ key for c in s)

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
opener.addheaders = [("User-Agent", "Mozilla/5.0")]

# Login (standard)
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

# Login (advanced)
data2 = urllib.parse.urlencode({
    "rqUsername": "1234",
    "rqPasswd": "gcdXt5AB",
    "rqTimeout": "600"
}).encode()
req2 = urllib.request.Request(base + "/cgi-bin/cbCheckLogin.xml", data=data2, method="POST")
req2.add_header("Content-Type", "application/x-www-form-urlencoded")
opener.open(req2, timeout=10)

# Get sessionKey from dhcp.asp
resp = opener.open(base + "/dhcp.asp", timeout=5)
content = resp.read().decode("latin-1", errors="replace")
sk_match = re.search(r"sessionKey\s*=\s*'(\d+)'", content)
sessionKey = sk_match.group(1) if sk_match else "0"
print(f"sessionKey: {sessionKey}")

# Step 1: Call cbGetDhcpv4ServerPool.xml WITHOUT params to list pools
# Use POST with no data (matching the $.post call)
req_list = urllib.request.Request(
    base + "/cgi-bin/cbGetDhcpv4ServerPool.xml",
    data=b"", method="POST"
)
req_list.add_header("Referer", base + "/dhcp.asp")
resp_list = opener.open(req_list, timeout=10)
list_result = resp_list.read().decode("latin-1", errors="replace")
print(f"\nPool list response ({len(list_result)} bytes): {list_result[:2000]}")

# Find all pool IDs
pool_0is = re.findall(r"rtm_cfg_dhcpv4_svr_pool_0i[^>]*>([^<]+)<", list_result)
print(f"\nFound pool IDs: {pool_0is}")

# Use the first pool
if pool_0is:
    pool_0i = pool_0is[0]
    print(f"Using pool_0i: {pool_0i}")
    
    # Step 2: Get pool details
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
    get_result = resp_get.read().decode("latin-1", errors="replace")
    print(f"\nPool details: {get_result[:2000]}")
    
    pool_id_match = re.search(r"rtm_cfg_dhcpv4_svr_pool_id[^>]*>([^<]+)<", get_result)
    pool_id = pool_id_match.group(1) if pool_id_match else "0"
    print(f"pool_id: {pool_id}")
else:
    pool_id = "0"
    print("No pools found")

# Step 3: Add static lease
mac_parts = MAC.replace(":", "-").split("-")
ip_parts = IP.split(".")

form_data = {
    "adm_state": "1",
    "mac_addr-0": mac_parts[0], "mac_addr-1": mac_parts[1], "mac_addr-2": mac_parts[2],
    "mac_addr-3": mac_parts[3], "mac_addr-4": mac_parts[4], "mac_addr-5": mac_parts[5],
    "mac_addr": MAC,
    "ipv4_addr-0": ip_parts[0], "ipv4_addr-1": ip_parts[1], "ipv4_addr-2": ip_parts[2], "ipv4_addr-3": ip_parts[3],
    "ipv4_addr": IP,
    "rtm_dhcpv4_svr_pool_static_id": "-1",
    "rtm_cfg_dhcpv4_svr_pool_id": pool_id,
    "sessionKey": sessionKey,
}

print(f"\nAdding static lease with pool_id={pool_id}...")
data_bytes = urllib.parse.urlencode(form_data).encode()
req_add = urllib.request.Request(
    base + "/cgi-bin/cbDhcpV4SvrPoolSetStatic.xml",
    data=data_bytes, method="POST"
)
req_add.add_header("Referer", base + "/dhcp.asp")
try:
    resp_add = opener.open(req_add, timeout=10)
    result = resp_add.read().decode("latin-1", errors="replace")
    print(f"Response: {result}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print(e.read().decode("latin-1", errors="replace"))

# Step 4: Verify by getting static lease list
if pool_id:
    verify_data = urllib.parse.urlencode({
        "rtm_cfg_dhcpv4_svr_pool_id": pool_id,
        "sessionKey": sessionKey
    }).encode()
    req_verify = urllib.request.Request(
        base + "/cgi-bin/cbDhcpV4SvrPoolGetStatic.xml",
        data=verify_data, method="POST"
    )
    req_verify.add_header("Referer", base + "/dhcp.asp")
    resp_verify = opener.open(req_verify, timeout=10)
    verify_result = resp_verify.read().decode("latin-1", errors="replace")
    print(f"\nStatic leases: {verify_result}")
