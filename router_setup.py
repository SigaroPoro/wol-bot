import urllib.request, urllib.parse, http.cookiejar, re, sys

base = 'http://192.168.1.1'
password = 'gcdXt5AB'

def xor_str(s, key=0x1f):
    return bytes(ord(c) ^ key for c in s)

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(cookie_jar),
)
opener.addheaders = [
    ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'),
]

# Login
print("Logging in...")
resp = opener.open(base + '/te_wifi.asp', timeout=5)
resp.read()
user_xor = xor_str('1234')
pass_xor = xor_str(password)
data = urllib.parse.urlencode([
    ('loginUsername', user_xor.decode('latin-1')),
    ('loginPassword', pass_xor.decode('latin-1')),
    ('curWebPage', '/te_wifi.asp')
]).encode('latin-1')
req = urllib.request.Request(base + '/cgi-bin/te_acceso_router.cgi', data=data, method='POST')
req.add_header('Referer', base + '/te_wifi.asp')
opener.open(req, timeout=10)
print(f"Cookies: {len(list(cookie_jar))}")

# Load admin page
resp = opener.open(base + '/te_wifi.asp', timeout=5)
body = resp.read().decode('utf-8', errors='ignore')
print(f"Admin page: {len(body)} bytes, login_page={'acceso_content' not in body}")

# Find all .asp references
asp_pages = set()
for m in re.finditer(r'["\']([^"\']+\.asp)["\']', body):
    p = m.group(1)
    if '/logout' not in p.lower() and not p.startswith('http'):
        asp_pages.add(p)

print("\nAvailable admin pages:")
for p in sorted(asp_pages):
    print(f"  {p}")

# Try to access all found ASP pages
print("\nTrying ASP pages...")
for page in sorted(asp_pages):
    try:
        resp = opener.open(base + page, timeout=5)
        resp_body = resp.read().decode('utf-8', errors='ignore')
        title = 'no title'
        if '<title>' in resp_body:
            title = resp_body.split('<title>')[1].split('</title>')[0]
        size = len(resp_body)
        has_nat = any(kw in resp_body for kw in ['NAT', 'nat', 'forward', 'Forward', 'Port', 'port', 'mapping', 'Mapping', 'Virtual Server', 'virtual server'])
        print(f"  {page} -> {resp.status} ({size}b) title='{title}' nat={has_nat}")
    except Exception as e:
        pass
