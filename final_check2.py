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

# Get ARP cache
req_arp = urllib.request.Request(
    base + "/cgi-bin/cbGetArpCache.xml",
    data=b"", method="POST"
)
req_arp.add_header("Referer", base + "/arpstats.asp")
resp_arp = opener.open(req_arp, timeout=10)
arp_result = resp_arp.read().decode("latin-1", errors="replace")
print(f"ARP Cache: {arp_result}")

# Check if 192.168.1.37 is there
if "192.168.1.37" in arp_result:
    # Extract context
    idx = arp_result.find("192.168.1.37")
    print(f"\n=== Entry for 192.168.1.37 ===")
    print(arp_result[max(0,idx-100):idx+200])
else:
    print("\n192.168.1.37 NOT found in ARP cache")
    # Check for any entries that might be related
    for ip in re.findall(r'<ipaddr>([^<]+)</ipaddr>', arp_result):
        print(f"  Entry: {ip}")
    for hw in re.findall(r'<hwaddr>([^<]+)</hwaddr>', arp_result):
        print(f"  HW: {hw}")
