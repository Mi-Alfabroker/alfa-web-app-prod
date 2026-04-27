"""Test backend service end-to-end against user's JSON."""
import json
import sys
sys.path.insert(0, 'backend')

from app.services.propuestas.propuesta_service import PropuestaService

with open('test_input_full.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

variables = data['variables']
print(f"Iter order [115], [118], [78]: positions in dict")
keys = list(variables.keys())
for k in ['[78]', '[115]', '[118]', '[119]']:
    if k in variables:
        print(f"  {k}: index={keys.index(k)}, value={variables[k]!r}")

# Call the service
buffer, filename, saved_path, error = PropuestaService.generate_proposal(
    template_name='copropiedades',
    variables=variables,
    imagenes=None
)

if error:
    print(f"ERROR: {error}")
else:
    print(f"Generated: {filename}")
    print(f"Saved at: {saved_path}")

    # Read back the generated XLSX and check [118] location
    import zipfile
    import re
    with zipfile.ZipFile(saved_path, 'r') as z:
        with z.open('xl/drawings/drawing10.xml') as f:
            content = f.read().decode('utf-8')

    # Check [118] location
    idx = content.find('<xdr:from><xdr:col>1</xdr:col><xdr:colOff>193700</xdr:colOff><xdr:row>46</xdr:row>')
    if idx > 0:
        end = content.find('</xdr:twoCellAnchor>', idx)
        block = content[idx:end]
        texts = re.findall(r'<a:t[^>]*>([^<]*)</a:t>', block)
        print(f"[118] text: {texts}")

    idx = content.find('<xdr:from><xdr:col>1</xdr:col><xdr:colOff>251152</xdr:colOff><xdr:row>46</xdr:row>')
    if idx > 0:
        end = content.find('</xdr:twoCellAnchor>', idx)
        block = content[idx:end]
        texts = re.findall(r'<a:t[^>]*>([^<]*)</a:t>', block)
        print(f"[119] text: {texts}")

    idx = content.find('<xdr:from><xdr:col>5</xdr:col><xdr:colOff>216941</xdr:colOff><xdr:row>46</xdr:row>')
    if idx > 0:
        end = content.find('</xdr:twoCellAnchor>', idx)
        block = content[idx:end]
        texts = re.findall(r'<a:t[^>]*>([^<]*)</a:t>', block)
        print(f"[209] text: {texts}")
