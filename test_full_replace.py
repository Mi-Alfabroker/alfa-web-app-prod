"""Mimic backend service _reemplazar_placeholders_en_xlsx end-to-end."""
import json
import re
import shutil
import zipfile
from pathlib import Path
from tempfile import mkdtemp

# Read JSON
with open('test_input_full.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
variables = data['variables']

print(f"Total variables: {len(variables)}")

template = Path('backend/app/resources/plantillas_xlsx/propuesta_cop.xlsx')
output = Path('test_output.xlsx')

temp_dir = Path(mkdtemp())
print(f"Temp: {temp_dir}")

with zipfile.ZipFile(template, 'r') as z:
    z.extractall(temp_dir)

def replace_in_xml(xml_file, variables):
    with open(xml_file, 'rb') as f:
        contenido = f.read().decode('utf-8')
    original = contenido
    for marcador, valor in variables.items():
        if marcador in contenido:
            valor_str = str(valor) if valor is not None else ''
            contenido = contenido.replace(marcador, valor_str)
    if contenido != original:
        with open(xml_file, 'wb') as f:
            f.write(contenido.encode('utf-8'))
        return True
    return False

# Process worksheets
for sheet_file in (temp_dir / 'xl' / 'worksheets').glob('sheet*.xml'):
    replace_in_xml(sheet_file, variables)

# sharedStrings
ss = temp_dir / 'xl' / 'sharedStrings.xml'
if ss.exists():
    replace_in_xml(ss, variables)

# Drawings
for d in (temp_dir / 'xl' / 'drawings').glob('*.xml'):
    replace_in_xml(d, variables)

# Now check drawing10
with open(temp_dir / 'xl' / 'drawings' / 'drawing10.xml', 'r', encoding='utf-8') as f:
    contenido = f.read()

# Find [118] location text
anchors = re.findall(
    r'<xdr:from><xdr:col>(\d+)</xdr:col><xdr:colOff>(\d+)</xdr:colOff><xdr:row>(\d+)</xdr:row>.*?</xdr:twoCellAnchor>',
    contenido, re.DOTALL
)
# Search col=1,row=46,colOff=193700 (was [118])
for col, coff, row in anchors:
    if col=='1' and row=='46' and coff=='193700':
        # Re-find the block
        idx = contenido.find(f'<xdr:from><xdr:col>1</xdr:col><xdr:colOff>193700</xdr:colOff><xdr:row>46</xdr:row>')
        end = contenido.find('</xdr:twoCellAnchor>', idx)
        block = contenido[idx:end]
        texts = re.findall(r'<a:t[^>]*>([^<]*)</a:t>', block)
        print(f"[118] location text: {texts}")
        break

# col=5,row=46,colOff=216941 (was [209])
idx = contenido.find('<xdr:from><xdr:col>5</xdr:col><xdr:colOff>216941</xdr:colOff><xdr:row>46</xdr:row>')
if idx > 0:
    end = contenido.find('</xdr:twoCellAnchor>', idx)
    block = contenido[idx:end]
    texts = re.findall(r'<a:t[^>]*>([^<]*)</a:t>', block)
    print(f"[209] location text: {texts}")

# col=1,row=46,colOff=251152 (was [119])
idx = contenido.find('<xdr:from><xdr:col>1</xdr:col><xdr:colOff>251152</xdr:colOff><xdr:row>46</xdr:row>')
if idx > 0:
    end = contenido.find('</xdr:twoCellAnchor>', idx)
    block = contenido[idx:end]
    texts = re.findall(r'<a:t[^>]*>([^<]*)</a:t>', block)
    print(f"[119] location text: {texts}")

shutil.rmtree(temp_dir, ignore_errors=True)
