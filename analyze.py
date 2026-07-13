import re

with open(r"C:\Users\rmonz\Desktop\wol-bot\admin_page.html", "r", encoding="latin-1") as f:
    content = f.read()

# Extract all JavaScript
scripts = re.findall(r"<script[^>]*>(.*?)</script>", content, re.DOTALL | re.I)

# Find all URLs/paths referenced
all_urls = []
for s in scripts:
    urls = re.findall(r'["]([^"]+\.[a-z]+)["]', s)
    all_urls.extend(urls)

print("URLs found:")
for u in sorted(set(all_urls)):
    print(f"  {u}")

# Find onclick, onload, etc references to pages
events = re.findall(r'(?:location|window\.open|loadPage|goPage|openPage)\s*[=.(]+\s*["\']([^"\']+)["\']', content, re.I)
print("\nNavigation events:")
for e in sorted(set(events)):
    print(f"  {e}")

# Search for .asp in all scripts
print("\nAll .asp references:")
for s in scripts:
    for m in re.finditer(r'"[^"]*\.asp[^"]*"', s):
        print(f"  {m.group()}")
