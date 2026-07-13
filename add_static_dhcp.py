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

# Fetch DHCP page to get sessionKey and pool_id
resp = opener.open(base + "/dhcp.asp", timeout=5)
content = resp.read().decode("latin-1", errors="replace")

# Extract session key
sk_match = re.search(r"sessionKey\s*=\s*'(\d+)'", content)
sessionKey = sk_match.group(1) if sk_match else ""
print(f"sessionKey: {sessionKey}")

# Extract pool_id from DHCPServerSettingForm
pool_match = re.search(r'name="rtm_cfg_dhcpv4_svr_pool_id"[^>]*value="([^"]*)"', content)
pool_id = pool_match.group(1) if pool_match else ""
print(f"pool_id: {pool_id}")

# Build form data
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

print(f"Sending: {form_data}")

# Send POST
data_bytes = urllib.parse.urlencode(form_data).encode()
req3 = urllib.request.Request(
    base + "/cgi-bin/cbDhcpV4SvrPoolSetStatic.xml",
    data=data_bytes,
    method="POST"
)
req3.add_header("Content-Type", "application/x-www-form-urlencoded")
req3.add_header("Referer", base + "/dhcp.asp")

try:
    resp3 = opener.open(req3, timeout=10)
    result = resp3.read().decode("latin-1", errors="replace")
    print(f"\nResponse ({len(result)} bytes): {result[:2000]}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} - {e.reason}")
    print(e.read().decode("latin-1", errors="replace"))
except Exception as e:
    print(f"Error: {e}")

# Now verify: fetch the DHCP page again and look for the static lease
print("\n\n=== Verifying ===")
resp4 = opener.open(base + "/dhcp.asp", timeout=5)
content2 = resp4.read().decode("latin-1", errors="replace")

# Check for our MAC or IP in the page
if MAC in content2 or IP in content2:
    print(f"SUCCESS: Found {MAC} or {IP} in DHCP page!")
else:
    print(f"MAC/IP not found in page")

# Also try to get the static lease list
data4 = urllib.parse.urlencode({
    "rtm_cfg_dhcpv4_svr_pool_id": pool_id,
    "sessionKey": sessionKey
}).encode()
req4 = urllib.request.Request(
    base + "/cgi-bin/cbDhcpV4SvrPoolGetStatic.xml",
    data=data4,
    method="POST"
)
req4.add_header("Content-Type", "application/x-www-form-urlencoded")
try:
    resp4 = opener.open(req4, timeout=10)
    result4 = resp4.read().decode("latin-1", errors="replace")
    print(f"\nStatic lease list: {result4[:2000]}")
except Exception as e:
    print(f"Error fetching lease list: {e}")
