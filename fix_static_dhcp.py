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
print(f"sessionKey: {sessionKey}")

# Step 1: Delete wrong static lease from pool_id=1 (the IAL pool)
# Send rtm_dhcpv4_svr_pool_static_id=0 with adm_state=0 to delete
del_data = {
    "rtm_dhcpv4_svr_pool_static_id": "0",
    "rtm_cfg_dhcpv4_svr_pool_id": "1",
    "adm_state": "0",  # Disable it
    "sessionKey": sessionKey
}
data_bytes = urllib.parse.urlencode(del_data).encode()
req_del = urllib.request.Request(
    base + "/cgi-bin/cbDhcpV4SvrPoolSetStatic.xml",
    data=data_bytes, method="POST"
)
req_del.add_header("Referer", base + "/dhcp.asp")
resp_del = opener.open(req_del, timeout=10)
del_result = resp_del.read().decode("latin-1", errors="replace")
print(f"Delete from pool 1: {del_result}")

# Step 2: Add static lease to pool_id=0 (main LAN)
mac_parts = MAC.replace(":", "-").split("-")
ip_parts = IP.split(".")

form_data = {
    "adm_state": "1",
    "mac_addr-0": mac_parts[0], "mac_addr-1": mac_parts[1], "mac_addr-2": mac_parts[2],
    "mac_addr-3": mac_parts[3], "mac_addr-4": mac_parts[4], "mac_addr-5": mac_parts[5],
    "mac_addr": MAC,
    "ipv4_addr-0": ip_parts[0], "ipv4_addr-1": ip_parts[1], "ipv4_addr-2": ip_parts[2], "ipv4_addr-3": ip_parts[3],
    "ipv4_addr": IP,
    "rtm_dhcpv4_svr_pool_static_id": "-1",  # -1 for new
    "rtm_cfg_dhcpv4_svr_pool_id": "0",  # Pool ID 0 = main LAN
    "sessionKey": sessionKey,
}

print(f"\nAdding static lease to pool 0 (main LAN)...")
data_bytes = urllib.parse.urlencode(form_data).encode()
req_add = urllib.request.Request(
    base + "/cgi-bin/cbDhcpV4SvrPoolSetStatic.xml",
    data=data_bytes, method="POST"
)
req_add.add_header("Referer", base + "/dhcp.asp")
resp_add = opener.open(req_add, timeout=10)
add_result = resp_add.read().decode("latin-1", errors="replace")
print(f"Add to pool 0: {add_result}")

# Step 3: Verify
print(f"\n--- Static leases for pool 0 (main LAN) ---")
verify_data = urllib.parse.urlencode({
    "rtm_cfg_dhcpv4_svr_pool_id": "0",
    "sessionKey": sessionKey
}).encode()
req_verify = urllib.request.Request(
    base + "/cgi-bin/cbDhcpV4SvrPoolGetStatic.xml",
    data=verify_data, method="POST"
)
req_verify.add_header("Referer", base + "/dhcp.asp")
resp_verify = opener.open(req_verify, timeout=10)
verify_result = resp_verify.read().decode("latin-1", errors="replace")
print(f"Pool 0: {verify_result}")

print(f"\n--- Static leases for pool 1 (IAL TV) ---")
verify_data2 = urllib.parse.urlencode({
    "rtm_cfg_dhcpv4_svr_pool_id": "1",
    "sessionKey": sessionKey
}).encode()
req_verify2 = urllib.request.Request(
    base + "/cgi-bin/cbDhcpV4SvrPoolGetStatic.xml",
    data=verify_data2, method="POST"
)
req_verify2.add_header("Referer", base + "/dhcp.asp")
resp_verify2 = opener.open(req_verify2, timeout=10)
verify_result2 = resp_verify2.read().decode("latin-1", errors="replace")
print(f"Pool 1: {verify_result2}")
