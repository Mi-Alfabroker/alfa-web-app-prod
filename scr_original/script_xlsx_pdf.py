from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from tempfile import mkdtemp
from typing import Dict, Optional, Tuple


def reemplazar_placeholders_en_xlsx(
    ruta_entrada: Path, 
    ruta_salida: Path, 
    variables: Dict[str, str],
    imagenes: Optional[Dict[str, str]] = None
) -> None:
    """
    Reemplaza placeholders en un XLSX preservando imágenes, dibujos y configuración de página.
    Trabaja directamente con los archivos XML internos del XLSX sin modificar configuraciones.
    Procesa: celdas, texto compartido, cuadros de texto, formas y gráficos.
    También reemplaza imágenes basándose en texto alternativo.
    
    Args:
        ruta_entrada: Archivo XLSX original
        ruta_salida: Archivo XLSX de salida
        variables: Variables de texto a reemplazar
        imagenes: Diccionario {texto_alternativo: ruta_imagen} (opcional)
    """
    print(f"\n🔄 Procesando XLSX: {ruta_entrada.name}")
    print(f"   Variables de texto: {len(variables)}")
    if imagenes:
        print(f"   Imágenes a reemplazar: {len(imagenes)}")
    
    # Crear directorio temporal
    temp_dir = Path(mkdtemp())

    try:
        # Extraer el XLSX (es un archivo ZIP) preservando metadatos
        with zipfile.ZipFile(ruta_entrada, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Procesar cada hoja de cálculo (sheet*.xml) - celdas
        xl_worksheets = temp_dir / "xl" / "worksheets"
        sheets_procesadas = 0
        if xl_worksheets.exists():
            for sheet_file in xl_worksheets.glob("sheet*.xml"):
                reemplazar_en_xml(sheet_file, variables)
                sheets_procesadas += 1
        print(f"  ✓ Procesadas {sheets_procesadas} hojas (celdas)")

        # Procesar sharedStrings.xml (texto compartido entre celdas)
        shared_strings = temp_dir / "xl" / "sharedStrings.xml"
        if shared_strings.exists():
            reemplazar_en_xml(shared_strings, variables)
            print(f"  ✓ Procesado texto compartido")
        
        # Procesar drawings (cuadros de texto, formas, objetos con texto)
        xl_drawings = temp_dir / "xl" / "drawings"
        drawings_procesados = 0
        if xl_drawings.exists():
            for drawing_file in xl_drawings.glob("*.xml"):
                reemplazar_en_xml(drawing_file, variables)
                drawings_procesados += 1
        if drawings_procesados > 0:
            print(f"  ✓ Procesados {drawings_procesados} dibujos/cuadros de texto")
        
        # Procesar charts (gráficos con etiquetas de texto)
        xl_charts = temp_dir / "xl" / "charts"
        charts_procesados = 0
        if xl_charts.exists():
            for chart_file in xl_charts.glob("*.xml"):
                reemplazar_en_xml(chart_file, variables)
                charts_procesados += 1
        if charts_procesados > 0:
            print(f"  ✓ Procesados {charts_procesados} gráficos")
        
        # Reemplazar imágenes si se especificaron
        if imagenes:
            reemplazar_imagenes_en_xlsx(temp_dir, imagenes, ruta_entrada.parent)

        # Re-empaquetar preservando exactamente la estructura y compresión originales
        print(f"  ↻ Re-empaquetando XLSX...")
        with zipfile.ZipFile(ruta_entrada, 'r') as zip_entrada:
            with zipfile.ZipFile(ruta_salida, 'w', zipfile.ZIP_DEFLATED) as zip_salida:
                for item in zip_entrada.infolist():
                    # Leer el archivo del directorio temporal (posiblemente modificado)
                    file_path = temp_dir / item.filename
                    
                    if file_path.is_file():
                        # Leer contenido (modificado o no)
                        contenido = file_path.read_bytes()
                        
                        # Preservar la información del archivo original (compresión, fechas, etc.)
                        zip_salida.writestr(item, contenido, compress_type=item.compress_type)
                    elif not file_path.exists() and not item.is_dir():
                        # Si el archivo no existe en temp (caso raro), copiar del original
                        contenido = zip_entrada.read(item.filename)
                        zip_salida.writestr(item, contenido, compress_type=item.compress_type)
        
        print(f"✅ XLSX generado: {ruta_salida.name}")
        print(f"   Configuración preservada: márgenes, orientación, tamaño\n")

    finally:
        # Limpiar directorio temporal
        shutil.rmtree(temp_dir, ignore_errors=True)


def reemplazar_en_xml(xml_file: Path, variables: Dict[str, str]) -> None:
    """
    Reemplaza placeholders en un archivo XML preservando la estructura exacta,
    incluyendo espacios, saltos de línea y configuraciones de formato.
    """
    # Leer el contenido XML como bytes para preservar codificación exacta
    with open(xml_file, 'rb') as f:
        contenido_bytes = f.read()
    
    # Decodificar a string para hacer los reemplazos
    contenido = contenido_bytes.decode('utf-8')
    
    # Reemplazar cada placeholder de forma segura
    # Solo reemplaza el contenido, no los atributos o etiquetas XML
    for marcador, valor in variables.items():
        if marcador in contenido:
            contenido = contenido.replace(marcador, valor)
    
    # Escribir preservando exactamente el formato y codificación
    with open(xml_file, 'wb') as f:
        f.write(contenido.encode('utf-8'))


def reemplazar_imagenes_en_xlsx(
    temp_dir: Path,
    imagenes: Dict[str, str],
    ruta_base: Path
) -> None:
    """
    Reemplaza imágenes en el XLSX basándose en su texto alternativo.
    
    Args:
        temp_dir: Directorio temporal con el XLSX extraído
        imagenes: Dict con {texto_alternativo: ruta_imagen}
        ruta_base: Ruta base para resolver rutas relativas de imágenes
    """
    if not imagenes:
        return
    
    print(f"  🖼️  Buscando imágenes para reemplazar...")
    imagenes_reemplazadas = 0
    
    # Procesar drawings para encontrar imágenes por texto alternativo
    xl_drawings = temp_dir / "xl" / "drawings"
    if not xl_drawings.exists():
        print(f"  ⚠️  No se encontraron dibujos en el XLSX")
        return
    
    for drawing_file in xl_drawings.glob("drawing*.xml"):
        # Leer el XML del dibujo
        with open(drawing_file, 'rb') as f:
            contenido = f.read().decode('utf-8')
        
        # Buscar cada imagen configurada
        for texto_alt, ruta_imagen in imagenes.items():
            # Buscar el texto alternativo en el XML
            # Formato: <wp:docPr id="..." name="..." descr="texto_alternativo"/>
            # O también: name="texto_alternativo"
            pattern_name = rf'name="([^"]*{re.escape(texto_alt)}[^"]*)"'
            pattern_descr = rf'descr="([^"]*{re.escape(texto_alt)}[^"]*)"'
            
            if re.search(pattern_name, contenido) or re.search(pattern_descr, contenido):
                # Encontramos la imagen, reemplazar el archivo físico
                if reemplazar_archivo_imagen(temp_dir, drawing_file, texto_alt, ruta_imagen, ruta_base):
                    imagenes_reemplazadas += 1
                    print(f"    ✓ Imagen reemplazada: {texto_alt}")
    
    if imagenes_reemplazadas > 0:
        print(f"  ✅ Total de imágenes reemplazadas: {imagenes_reemplazadas}")
    else:
        print(f"  ⚠️  No se encontraron imágenes con los textos alternativos especificados")


def reemplazar_archivo_imagen(
    temp_dir: Path,
    drawing_file: Path,
    texto_alt: str,
    ruta_nueva_imagen: str,
    ruta_base: Path
) -> bool:
    """
    Reemplaza el archivo físico de la imagen en xl/media/
    
    Returns:
        True si se reemplazó exitosamente, False si hubo error
    """
    try:
        # Resolver ruta de la nueva imagen
        if Path(ruta_nueva_imagen).is_absolute():
            nueva_imagen_path = Path(ruta_nueva_imagen)
        else:
            nueva_imagen_path = ruta_base / ruta_nueva_imagen
        
        if not nueva_imagen_path.exists():
            print(f"    ⚠️  Imagen no encontrada: {nueva_imagen_path}")
            return False
        
        # Buscar el rId de la imagen en el drawing
        rId = extraer_rId_de_drawing(drawing_file, texto_alt)
        if not rId:
            print(f"    ⚠️  No se pudo encontrar rId para: {texto_alt}")
            return False
        
        # Obtener el nombre del archivo de imagen desde _rels
        rels_file = drawing_file.parent / "_rels" / f"{drawing_file.name}.rels"
        if not rels_file.exists():
            print(f"    ⚠️  Archivo _rels no encontrado: {rels_file}")
            return False
        
        archivo_imagen = obtener_archivo_imagen_desde_rels(rels_file, rId)
        if not archivo_imagen:
            print(f"    ⚠️  No se pudo encontrar archivo de imagen para rId: {rId}")
            return False
        
        # Reemplazar el archivo en xl/media/
        archivo_destino = temp_dir / "xl" / "media" / archivo_imagen
        if not archivo_destino.exists():
            print(f"    ⚠️  Archivo de destino no encontrado: {archivo_destino}")
            return False
        
        # Copiar la nueva imagen sobre la antigua
        shutil.copy2(nueva_imagen_path, archivo_destino)
        return True
        
    except Exception as e:
        print(f"    ⚠️  Error reemplazando imagen: {e}")
        return False


def extraer_rId_de_drawing(drawing_file: Path, texto_alt: str) -> Optional[str]:
    """
    Extrae el rId (relationship ID) de una imagen basándose en su texto alternativo.
    """
    with open(drawing_file, 'rb') as f:
        contenido = f.read().decode('utf-8')
    
    # Buscar la sección que contiene el texto alternativo
    # Formato típico:
    # <xdr:pic>
    #   <xdr:nvPicPr>
    #     <xdr:cNvPr id="X" name="X" descr="texto_alt"/>
    #   </xdr:nvPicPr>
    #   <xdr:blipFill>
    #     <a:blip r:embed="rId1"/>
    
    # Buscar el bloque que contiene el texto alternativo
    pattern = rf'<xdr:cNvPr[^>]*(?:name="[^"]*{re.escape(texto_alt)}[^"]*"|descr="[^"]*{re.escape(texto_alt)}[^"]*")[^>]*>.*?<a:blip[^>]+r:embed="([^"]+)"'
    match = re.search(pattern, contenido, re.DOTALL)
    
    if match:
        return match.group(1)
    
    # Intento alternativo: buscar más amplio
    # Primero encontrar el cNvPr, luego buscar el siguiente a:blip
    pattern_cnvpr = rf'<xdr:cNvPr[^>]*(?:name="[^"]*{re.escape(texto_alt)}[^"]*"|descr="[^"]*{re.escape(texto_alt)}[^"]*")[^>]*>'
    match_cnvpr = re.search(pattern_cnvpr, contenido)
    
    if match_cnvpr:
        # Buscar el siguiente a:blip después de esta posición
        start_pos = match_cnvpr.end()
        remaining = contenido[start_pos:start_pos + 2000]  # Buscar en los próximos 2000 caracteres
        pattern_blip = r'<a:blip[^>]+r:embed="([^"]+)"'
        match_blip = re.search(pattern_blip, remaining)
        if match_blip:
            return match_blip.group(1)
    
    return None


def obtener_archivo_imagen_desde_rels(rels_file: Path, rId: str) -> Optional[str]:
    """
    Obtiene el nombre del archivo de imagen desde el archivo _rels usando el rId.
    """
    with open(rels_file, 'rb') as f:
        contenido = f.read().decode('utf-8')
    
    # Buscar la relación con el rId
    # Formato: <Relationship Id="rId1" Type="..." Target="../media/image1.png"/>
    pattern = rf'<Relationship[^>]+Id="{re.escape(rId)}"[^>]+Target="([^"]+)"'
    match = re.search(pattern, contenido)
    
    if match:
        target = match.group(1)
        # El target puede ser "../media/image1.png", extraer solo el nombre
        return Path(target).name
    
    return None


def encontrar_soffice() -> Optional[str]:
    """Busca el ejecutable de LibreOffice."""
    for candidato in ("soffice", "libreoffice"):
        encontrado = shutil.which(candidato)
        if encontrado:
            return encontrado
    return None


def convertir_a_pdf(
    ruta_xlsx: Path,
    ruta_pdf: Path,
    page_size: Optional[str] = None,
    orientation: Optional[str] = None
) -> None:
    """
    Convierte XLSX a PDF usando LibreOffice en modo headless.
    
    Args:
        ruta_xlsx: Ruta al archivo XLSX de entrada
        ruta_pdf: Ruta de salida del PDF
        page_size: Tamaño de página (a4, letter, legal). None preserva configuración del Excel.
        orientation: Orientación (portrait, landscape). None preserva configuración del Excel.
    
    IMPORTANTE: Si no se especifica page_size ni orientation, se preservan TODAS las 
    configuraciones del Excel original incluyendo márgenes, tamaño y orientación.
    """
    soffice = encontrar_soffice()
    if not soffice:
        raise RuntimeError(
            "No se encontró LibreOffice (soffice/libreoffice) en el PATH. "
            "Instálalo o convierte manualmente el XLSX a PDF."
        )

    # Solo aplicar filtros si se especifican opciones explícitamente
    # De lo contrario, LibreOffice usará la configuración del Excel tal cual
    if page_size or orientation:
        print(f"⚠️  Aplicando configuración personalizada (esto puede modificar márgenes)")
        
        # Mapear tamaños a códigos de papel de LibreOffice
        # Nota: Esto puede afectar las márgenes originales
        tamaños_codigo = {
            'a4': '9',      # Código de papel A4
            'letter': '1',  # Código de papel Letter
            'legal': '5',   # Código de papel Legal
        }
        
        # Construir opciones de filtro PDF
        opciones = []
        
        if page_size and page_size.lower() in tamaños_codigo:
            codigo = tamaños_codigo[page_size.lower()]
            opciones.append(f"PaperFormat={codigo}")
        
        if orientation:
            # 0 = portrait, 1 = landscape
            orient_value = '1' if orientation.lower() == 'landscape' else '0'
            opciones.append(f"PaperOrientation={orient_value}")
        
        # Construir el filtro completo
        if opciones:
            filtro = ";".join(opciones)
            formato_pdf = f"pdf:calc_pdf_Export:{{{filtro}}}"
        else:
            formato_pdf = "pdf"
    else:
        # Sin opciones = preserva TODO del Excel (márgenes, tamaño, orientación)
        print(f"✓ Preservando configuración original del Excel (incluyendo márgenes)")
        formato_pdf = "pdf"

    comando = [
        soffice,
        "--headless",
        "--convert-to",
        formato_pdf,
        "--outdir",
        str(ruta_pdf.parent),
        str(ruta_xlsx),
    ]
    subprocess.run(comando, check=True)

    generado = ruta_pdf.parent / f"{ruta_xlsx.stem}.pdf"
    if generado != ruta_pdf:
        generado.replace(ruta_pdf)


def cargar_variables(desde_json: Path) -> Tuple[Dict[str, str], Optional[Dict[str, str]]]:
    """
    Lee el JSON con variables y devuelve variables de texto e imágenes.
    
    Soporta dos formatos:
    1. Formato simple (compatibilidad): {"[var]": "valor"}
    2. Formato extendido: {"texto": {...}, "imagenes": {...}}
    
    Returns:
        Tupla (variables_texto, variables_imagenes)
    """
    with desde_json.open("r", encoding="utf-8") as f:
        data = json.load(f)
    
    if not isinstance(data, dict):
        raise ValueError("El JSON debe ser un objeto")
    
    # Detectar formato
    if "texto" in data or "imagenes" in data:
        # Formato extendido
        variables_texto = data.get("texto", {})
        variables_imagenes = data.get("imagenes", {})
        
        if not isinstance(variables_texto, dict):
            raise ValueError("'texto' debe ser un objeto")
        if variables_imagenes and not isinstance(variables_imagenes, dict):
            raise ValueError("'imagenes' debe ser un objeto")
        
        return (
            {str(k): "" if v is None else str(v) for k, v in variables_texto.items()},
            {str(k): str(v) for k, v in variables_imagenes.items()} if variables_imagenes else None
        )
    else:
        # Formato simple (retrocompatibilidad)
        return (
            {str(k): "" if v is None else str(v) for k, v in data.items()},
            None
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Reemplaza placeholders en un XLSX y lo convierte a PDF.\n"
            "Ejemplo de variables.json: {\"[nombre_administrador]\": \"Ana\"}"
        )
    )
    parser.add_argument("xlsx", type=Path, help="Ruta al XLSX de entrada")
    parser.add_argument("pdf", type=Path, help="Ruta de salida del PDF")
    parser.add_argument(
        "variables",
        type=Path,
        help="Ruta al JSON con variables {placeholder: valor}",
    )
    parser.add_argument(
        "--xlsx-salida",
        type=Path,
        default=None,
        help=(
            "Ruta opcional para guardar el XLSX ya reemplazado "
            "(por defecto junto al PDF)"
        ),
    )
    parser.add_argument(
        "--page-size",
        type=str,
        choices=['a4', 'letter', 'legal'],
        default=None,
        help=(
            "Tamaño de página del PDF (a4, letter, legal). "
            "Por defecto usa el tamaño configurado en el Excel."
        ),
    )
    parser.add_argument(
        "--orientation",
        type=str,
        choices=['portrait', 'landscape'],
        default=None,
        help=(
            "Orientación del PDF (portrait=vertical, landscape=horizontal). "
            "Por defecto usa la orientación del Excel."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    ruta_xlsx = args.xlsx.resolve()
    ruta_pdf = args.pdf.resolve()
    ruta_variables = args.variables.resolve()
    ruta_xlsx_salida = (
        args.xlsx_salida.resolve()
        if args.xlsx_salida
        else ruta_pdf.parent / f"{ruta_pdf.stem}.xlsx"
    )

    if not ruta_xlsx.exists():
        print(f"XLSX no encontrado: {ruta_xlsx}", file=sys.stderr)
        return 1
    if not ruta_variables.exists():
        print(
            f"JSON de variables no encontrado: {ruta_variables}",
            file=sys.stderr,
        )
        return 1
    ruta_pdf.parent.mkdir(parents=True, exist_ok=True)
    ruta_xlsx_salida.parent.mkdir(parents=True, exist_ok=True)

    variables_texto, variables_imagenes = cargar_variables(ruta_variables)
    reemplazar_placeholders_en_xlsx(
        ruta_xlsx, 
        ruta_xlsx_salida, 
        variables_texto,
        variables_imagenes
    )
    convertir_a_pdf(
        ruta_xlsx_salida,
        ruta_pdf,
        page_size=args.page_size,
        orientation=args.orientation
    )

    # Mostrar información de configuración usada
    config_info = []
    if args.page_size:
        config_info.append(f"tamaño: {args.page_size.upper()}")
    if args.orientation:
        config_info.append(f"orientación: {args.orientation}")
    
    if config_info:
        print(f"Listo. PDF generado en: {ruta_pdf} ({', '.join(config_info)})")
    else:
        print(f"Listo. PDF generado en: {ruta_pdf}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
