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

# Get sessionKey
resp = opener.open(base + "/dhcp.asp", timeout=5)
content = resp.read().decode("latin-1", errors="replace")
sk_match = re.search(r"sessionKey\s*=\s*'(\d+)'", content)
sessionKey = sk_match.group(1) if sk_match else "0"

# 1. Save config
print("=== Saving config ===")
save_data = urllib.parse.urlencode({"sessionKey": sessionKey, "backup": "1"}).encode()
req_save = urllib.request.Request(
    base + "/cgi-bin/cbSaveConfig.xml",
    data=save_data, method="POST"
)
req_save.add_header("Referer", base + "/save.asp")
resp_save = opener.open(req_save, timeout=10)
save_result = resp_save.read().decode("latin-1", errors="replace")
print(f"Save: {save_result[:500]}")

# 2. Get ARP table
print("\n=== ARP Table ===")
resp_arp = opener.open(base + "/arpstats.asp", timeout=5)
arp_content = resp_arp.read().decode("latin-1", errors="replace")
sk_arp = re.search(r"sessionKey\s*=\s*'(\d+)'", arp_content)
sessionKey_arp = sk_arp.group(1) if sk_arp else "0"

# Post to cbGetArpTables.xml
arp_data = urllib.parse.urlencode({"sessionKey": sessionKey_arp}).encode()
req_arp = urllib.request.Request(
    base + "/cgi-bin/cbGetArpTables.xml",
    data=arp_data, method="POST"
)
req_arp.add_header("Referer", base + "/arpstats.asp")
resp_arp = opener.open(req_arp, timeout=10)
arp_result = resp_arp.read().decode("latin-1", errors="replace")
print(f"ARP table: {arp_result[:2000]}")

# Check if 192.168.1.37 is there
if "192.168.1.37" in arp_result:
    idx = arp_result.find("192.168.1.37")
    # Get context
    print(f"\nContext around 192.168.1.37:")
    print(arp_result[max(0,idx-200):idx+400])
