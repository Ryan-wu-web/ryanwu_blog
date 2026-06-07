import re

html = open('public/categories/tech/index.html', 'r', encoding='utf-8').read()

# Find h1 elements
for m in re.finditer(r'<(h1|h2|div|span|p)[^>]*class=["\']([^"\']*)["\'][^>]*>(.*?)</\1>', html, re.DOTALL | re.IGNORECASE):
    tag, cls, content = m.groups()
    text = re.sub(r'<[^>]+>', '', content).strip()
    if text and len(text) < 200 and ('title' in cls.lower() or 'header' in cls.lower() or 'site' in cls.lower()):
        print(f'<{tag} class="{cls}"> = "{text}"')

# Also search for id-based headers
for m in re.finditer(r'<(h1|h2|div|span|p)[^>]*id=["\']([^"\']*)["\'][^>]*>(.*?)</\1>', html, re.DOTALL | re.IGNORECASE):
    tag, id_val, content = m.groups()
    text = re.sub(r'<[^>]+>', '', content).strip()
    if text and len(text) < 200 and ('title' in id_val.lower() or 'header' in id_val.lower() or 'site' in id_val.lower()):
        print(f'<{tag} id="{id_val}"> = "{text}"')
