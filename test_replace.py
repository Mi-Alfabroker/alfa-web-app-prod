import json
import re
import sys

# Read JSON
with open('test_input.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
variables = data['variables']

# Read template
with open('drawing10_dump.xml', 'r', encoding='utf-8') as f:
    contenido = f.read()

# Mimic backend replace logic
print(f"Total variables: {len(variables)}")
print(f"Iter order first 5: {list(variables.keys())[:5]}")
print(f"[78] value: {variables.get('[78]')}")
print(f"[118] value: {variables.get('[118]')}")

# Track [118] state through iterations
checkpoints = ['[1]', '[78]', '[118]', '[200]', '[300]']

for marcador, valor in variables.items():
    if marcador in contenido:
        valor_str = str(valor) if valor is not None else ''
        contenido = contenido.replace(marcador, valor_str)
    if marcador in checkpoints:
        # Check what's at location of [118] (col=1,row=46,cOff=193700)
        # Simply search for unique anchor pattern
        anchor_pat = r'<xdr:from><xdr:col>1</xdr:col><xdr:colOff>193700</xdr:colOff><xdr:row>46</xdr:row>'
        m = re.search(anchor_pat, contenido)
        if m:
            block_end = contenido.find('</xdr:twoCellAnchor>', m.start())
            block = contenido[m.start():block_end]
            text_match = re.search(r'<a:t[^>]*>([^<]*)</a:t>', block)
            text = text_match.group(1) if text_match else 'NONE'
            print(f"  After {marcador}: text at [118] location = '{text}'")

# Final search
print("\nFinal: search [118] location text:")
anchor_pat = r'<xdr:from><xdr:col>1</xdr:col><xdr:colOff>193700</xdr:colOff><xdr:row>46</xdr:row>'
m = re.search(anchor_pat, contenido)
if m:
    block_end = contenido.find('</xdr:twoCellAnchor>', m.start())
    block = contenido[m.start():block_end]
    texts = re.findall(r'<a:t[^>]*>([^<]*)</a:t>', block)
    print(f"  Texts: {texts}")

# Also check col=1,row=46,cOff=251152 ([119])
print("\nFinal: search [119] location text:")
anchor_pat = r'<xdr:from><xdr:col>1</xdr:col><xdr:colOff>251152</xdr:colOff><xdr:row>46</xdr:row>'
m = re.search(anchor_pat, contenido)
if m:
    block_end = contenido.find('</xdr:twoCellAnchor>', m.start())
    block = contenido[m.start():block_end]
    texts = re.findall(r'<a:t[^>]*>([^<]*)</a:t>', block)
    print(f"  Texts: {texts}")
