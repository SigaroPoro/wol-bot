import urllib.request, urllib.parse, http.cookiejar, re, sys

base = "http://192.168.1.1"
password = "gcdXt5AB"

def xor_str(s, key=0x1f):
    return bytes(ord(c) ^ key for c in s)

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(cookie_jar),
)
opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")]

# Login
print("Logging in...")
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

# Now try accessing admin page
resp = opener.open(base + "/te_wifi.asp", timeout=5)
content = resp.read().decode("latin-1", errors="replace")
print(f"Page length: {len(content)}")
print(f"Shows login: {'acceso_content' in content}")

# Look for links and pages
links = re.findall(r'"([^"]+\.asp)"', content)
for l in sorted(set(links)):
    print(f"  {l}")
