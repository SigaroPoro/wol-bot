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

# Get session key from natloopback.asp
resp = opener.open(base + "/natloopback.asp", timeout=5)
content = resp.read().decode("latin-1", errors="replace")
sk_match = re.search(r"sessionKey\s*=\s*'(\d+)'", content)
sessionKey = sk_match.group(1) if sk_match else "0"
print(f"sessionKey: {sessionKey}")

# Enable NAT Loopback
# From the HTML: <form id="NatLoopbackForm" action="/cgi-bin/cbSetNatConfig.xml">
# <input type="checkbox" name="adm_state">Enable
# <input type="hidden" name="rtm_cfg_nat_lb_intf_id" value="...">
# Need to find the correct interface ID

# First, get the current config
get_data = urllib.parse.urlencode({"sessionKey": sessionKey}).encode()
req_get = urllib.request.Request(
    base + "/cgi-bin/cbGetNatConfig.xml",
    data=get_data, method="POST"
)
req_get.add_header("Referer", base + "/natloopback.asp")
resp_get = opener.open(req_get, timeout=10)
nat_config = resp_get.read().decode("latin-1", errors="replace")
print(f"NAT config: {nat_config}")

# Find the loopback interface IDs
lb_ids = re.findall(r"rtm_cfg_nat_lb_intf_id[^>]*>([^<]+)", nat_config)
print(f"Loopback interface IDs: {lb_ids}")

# Enable loopback for each interface
for intf_id in lb_ids:
    set_data = urllib.parse.urlencode({
        "adm_state": "on",  # Checkbox value when checked
        "rtm_cfg_nat_lb_intf_id": intf_id,
        "sessionKey": sessionKey
    }).encode()
    req_set = urllib.request.Request(
        base + "/cgi-bin/cbSetNatConfig.xml",
        data=set_data, method="POST"
    )
    req_set.add_header("Referer", base + "/natloopback.asp")
    resp_set = opener.open(req_set, timeout=10)
    result = resp_set.read().decode("latin-1", errors="replace")
    print(f"Loopback {intf_id}: {result}")

# Verify
resp_get2 = opener.open(base + "/natloopback.asp", timeout=5)
content2 = resp_get2.read().decode("latin-1", errors="replace")
print(f"\nPage now has: {'checked' if 'checked' in content2.lower() else 'not checked'}")
for line in content2.split('\n'):
    if 'loopback' in line.lower() or 'adm_state' in line.lower() or 'checked' in line.lower():
        print(f"  {line.strip()[:200]}")

# Save config
resp = opener.open(base + "/dhcp.asp", timeout=5)
dhcp_content = resp.read().decode("latin-1", errors="replace")
sk2 = re.search(r"sessionKey\s*=\s*'(\d+)'", dhcp_content)
sessionKey2 = sk2.group(1) if sk2 else sessionKey

save_data = urllib.parse.urlencode({"sessionKey": sessionKey2, "backup": "1"}).encode()
req_save = urllib.request.Request(
    base + "/cgi-bin/cbSaveConfig.xml",
    data=save_data, method="POST"
)
req_save.add_header("Referer", base + "/save.asp")
resp_save = opener.open(req_save, timeout=10)
save_result = resp_save.read().decode("latin-1", errors="replace")
print(f"\nSave: {save_result[:200]}")
