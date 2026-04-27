"""Business logic service for proposal (propuesta) generation.

Uses the same technique as the original script: works directly with
the internal XML files of the XLSX (which is a ZIP archive) to preserve
all images, drawings, and page configurations.
"""
import os
import io
import re
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from tempfile import mkdtemp
from typing import Optional, Dict


class PropuestaService:
    """
    Service for generating insurance proposals from Excel templates.
    
    Handles variable replacement in Excel templates by working directly
    with the internal XML files, preserving images, drawings, and formatting.
    """

    # Available templates mapping
    TEMPLATES = {
        'copropiedades': 'propuesta_cop.xlsx',
        'hogar': 'propuesta_hogar.xlsx',
        'vehiculos': 'propuesta_vehiculos.xlsx',
        'otros': 'propuesta_otros.xlsx',
        'entrega_copropiedades': 'entrega_copropiedades.xlsx',
        'entrega_hogar': 'entrega_hogar.xlsx',
        'entrega_vehiculos': 'entrega_vehiculos.xlsx',
        'entrega_otros': 'entrega_otro.xlsx',
    }
    
    # Base path for templates
    TEMPLATES_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'resources',
        'plantillas_xlsx'
    )
    
    # Base path for images
    IMAGES_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'resources',
        'images'
    )
    
    # Image categories and their folder names
    IMAGE_CATEGORIES = {
        'logo_aseg': 'logos_aseguradoras',
        'bandera_aseg': 'banderas_aseguradoras',
    }
    
    # Output path for generated documents (shared volume)
    OUTPUT_PATH = os.environ.get(
        'GESTION_DOCUMENTAL_PATH',
        '/opt/gestion_documental_ab'
    )
    
    # Subdirectory for proposals
    PROPOSALS_SUBDIR = 'propuestas'

    @classmethod
    def get_available_templates(cls) -> list[str]:
        """
        Get list of available template names.
        
        Returns:
            List of template identifiers
        """
        return list(cls.TEMPLATES.keys())

    @classmethod
    def _get_template_path(cls, template_name: str) -> Optional[str]:
        """
        Get the full path for a template.
        
        Args:
            template_name: The template identifier
            
        Returns:
            Full path to template file or None if not found
        """
        filename = cls.TEMPLATES.get(template_name)
        if not filename:
            return None
        
        path = os.path.join(cls.TEMPLATES_PATH, filename)
        return path if os.path.exists(path) else None

    @classmethod
    def _ensure_output_directory(cls) -> str:
        """
        Ensure the output directory exists.
        
        Returns:
            Full path to the proposals output directory
        """
        output_dir = os.path.join(cls.OUTPUT_PATH, cls.PROPOSALS_SUBDIR)
        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    @classmethod
    def _generate_unique_filename(cls, template_name: str) -> str:
        """
        Generate a unique filename with timestamp.
        
        Args:
            template_name: The template identifier
            
        Returns:
            Unique filename with timestamp
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"propuesta_{template_name}_{timestamp}.xlsx"

    @classmethod
    def _reemplazar_en_xml(cls, xml_file: Path, variables: Dict[str, str]) -> int:
        """
        Replace placeholders in an XML file preserving exact structure.
        
        Only replaces content text, not XML attributes or tags.
        
        Args:
            xml_file: Path to the XML file
            variables: Dictionary of {placeholder: value}
            
        Returns:
            Number of replacements made
        """
        # Read XML content as bytes to preserve exact encoding
        with open(xml_file, 'rb') as f:
            contenido_bytes = f.read()
        
        # Decode to string for replacements
        contenido = contenido_bytes.decode('utf-8')
        contenido_original = contenido  # Keep original for comparison
        
        replacements = 0
        
        # DEBUG: Check specifically for [1] in this file
        if '[1]' in contenido:
            print(f"    DEBUG _reemplazar: [1] EXISTE en contenido de {xml_file.name}", flush=True)
        
        # Replace each placeholder safely
        for marcador, valor in variables.items():
            if marcador in contenido:
                # Convert value to string, handle None
                valor_str = str(valor) if valor is not None else ''
                contenido = contenido.replace(marcador, valor_str)
                replacements += 1
                msg = f"    OK Reemplazado: {marcador} -> {valor_str[:50]}..." if len(str(valor_str)) > 50 else f"    OK Reemplazado: {marcador} -> {valor_str}"
                print(msg, flush=True)
        
        # Only write if changes were made
        if contenido != contenido_original:
            with open(xml_file, 'wb') as f:
                f.write(contenido.encode('utf-8'))
            print(f"  Archivo modificado: {xml_file.name}", flush=True)
        
        return replacements

    @classmethod
    def _normalize_filename(cls, value: str) -> str:
        """
        Normalize a string to be used as a filename.
        Removes accents, special characters, and replaces spaces with underscores.
        
        Args:
            value: Original string
            
        Returns:
            Normalized string safe for filenames
        """
        import unicodedata
        
        # Convert to lowercase
        result = value.lower().strip()
        
        # Remove accents (normalize to NFD and remove combining characters)
        result = unicodedata.normalize('NFD', result)
        result = ''.join(c for c in result if unicodedata.category(c) != 'Mn')
        
        # Replace spaces with nothing or underscore
        result = result.replace(' ', '_')
        
        # Remove special characters, keep only alphanumeric and underscore
        result = re.sub(r'[^a-z0-9_]', '', result)
        
        # Remove consecutive underscores
        result = re.sub(r'_+', '_', result)
        
        # Remove leading/trailing underscores
        result = result.strip('_')
        
        return result

    @classmethod
    def _resolve_image_path(cls, key: str, value: str) -> Optional[Path]:
        """
        Resolve the full path to an image file based on the key pattern.
        
        Args:
            key: Image key (e.g., 'logo_aseg_1', 'bandera_aseg_2')
            value: Image name (e.g., 'mapfre', 'sura')
            
        Returns:
            Full path to the image file or None if not found
        """
        # Normalize value to a safe filename
        value_normalized = cls._normalize_filename(value)
        
        print(f"    Buscando imagen: key={key}, valor_original={value}, normalizado={value_normalized}", flush=True)
        
        # Determine category from key (e.g., 'logo_aseg_1' -> 'logo_aseg')
        for category_prefix, folder_name in cls.IMAGE_CATEGORIES.items():
            if key.startswith(category_prefix):
                image_path = Path(cls.IMAGES_PATH) / folder_name / f"{value_normalized}.png"
                print(f"    Ruta completa: {image_path}", flush=True)
                if image_path.exists():
                    print(f"    Imagen ENCONTRADA!", flush=True)
                    return image_path
                print(f"    Imagen no encontrada: {image_path}", flush=True)
                return None
        
        print(f"    Categoria de imagen no reconocida para key: {key}", flush=True)
        return None

    @classmethod
    def _extraer_rId_de_drawing(cls, drawing_file: Path, texto_alt: str) -> Optional[str]:
        """
        Extract the rId (relationship ID) of an image based on its EXACT alternative text.
        
        Args:
            drawing_file: Path to the drawing XML file
            texto_alt: Alternative text to search for (exact match)
            
        Returns:
            The rId string or None if not found
        """
        with open(drawing_file, 'rb') as f:
            contenido = f.read().decode('utf-8')
        
        # Search for EXACT match of alternative text
        # Format: <xdr:cNvPr id="X" name="texto_alt" descr="..."/> or name="..." descr="texto_alt"
        # Using exact match with word boundaries
        
        # Pattern 1: Exact match in name attribute
        pattern_exact_name = rf'<xdr:cNvPr[^>]*\bname="{re.escape(texto_alt)}"[^>]*>.*?<a:blip[^>]+r:embed="([^"]+)"'
        match = re.search(pattern_exact_name, contenido, re.DOTALL)
        if match:
            print(f"      rId encontrado por name exacto: {match.group(1)}", flush=True)
            return match.group(1)
        
        # Pattern 2: Exact match in descr attribute
        pattern_exact_descr = rf'<xdr:cNvPr[^>]*\bdescr="{re.escape(texto_alt)}"[^>]*>.*?<a:blip[^>]+r:embed="([^"]+)"'
        match = re.search(pattern_exact_descr, contenido, re.DOTALL)
        if match:
            print(f"      rId encontrado por descr exacto: {match.group(1)}", flush=True)
            return match.group(1)
        
        # Alternative: First find exact cNvPr, then search for the next a:blip
        pattern_cnvpr_name = rf'<xdr:cNvPr[^>]*\bname="{re.escape(texto_alt)}"[^>]*>'
        pattern_cnvpr_descr = rf'<xdr:cNvPr[^>]*\bdescr="{re.escape(texto_alt)}"[^>]*>'
        
        match_cnvpr = re.search(pattern_cnvpr_name, contenido) or re.search(pattern_cnvpr_descr, contenido)
        
        if match_cnvpr:
            # Search for the next a:blip after this position (within same pic block)
            start_pos = match_cnvpr.end()
            # Look for closing </xdr:pic> to limit search scope
            remaining = contenido[start_pos:start_pos + 3000]
            pattern_blip = r'<a:blip[^>]+r:embed="([^"]+)"'
            match_blip = re.search(pattern_blip, remaining)
            if match_blip:
                print(f"      rId encontrado por búsqueda alternativa: {match_blip.group(1)}", flush=True)
                return match_blip.group(1)
        
        return None

    @classmethod
    def _obtener_archivo_imagen_desde_rels(cls, rels_file: Path, rId: str) -> Optional[str]:
        """
        Get the image filename from the _rels file using the rId.
        
        Args:
            rels_file: Path to the .rels file
            rId: Relationship ID to search for
            
        Returns:
            Image filename or None if not found
        """
        with open(rels_file, 'rb') as f:
            contenido = f.read().decode('utf-8')
        
        # Search for the relationship with the rId
        # Format: <Relationship Id="rId1" Type="..." Target="../media/image1.png"/>
        pattern = rf'<Relationship[^>]+Id="{re.escape(rId)}"[^>]+Target="([^"]+)"'
        match = re.search(pattern, contenido)
        
        if match:
            target = match.group(1)
            return Path(target).name
        
        return None

    @classmethod
    def _reemplazar_archivo_imagen(
        cls,
        temp_dir: Path,
        drawing_file: Path,
        texto_alt: str,
        ruta_nueva_imagen: Path
    ) -> bool:
        """
        Replace the physical image file in xl/media/.
        
        Args:
            temp_dir: Temporary directory with extracted XLSX
            drawing_file: Path to the drawing XML file
            texto_alt: Alternative text of the image to replace
            ruta_nueva_imagen: Path to the new image file
            
        Returns:
            True if replaced successfully, False otherwise
        """
        try:
            if not ruta_nueva_imagen.exists():
                print(f"    Imagen no encontrada: {ruta_nueva_imagen}", flush=True)
                return False
            
            # Get the rId of the image from the drawing
            rId = cls._extraer_rId_de_drawing(drawing_file, texto_alt)
            if not rId:
                print(f"    No se pudo encontrar rId para: {texto_alt}", flush=True)
                return False
            
            # Get the image filename from _rels
            rels_file = drawing_file.parent / "_rels" / f"{drawing_file.name}.rels"
            if not rels_file.exists():
                print(f"    Archivo _rels no encontrado: {rels_file}", flush=True)
                return False
            
            archivo_imagen = cls._obtener_archivo_imagen_desde_rels(rels_file, rId)
            if not archivo_imagen:
                print(f"    No se pudo encontrar archivo de imagen para rId: {rId}", flush=True)
                return False
            
            # Replace the file in xl/media/
            archivo_destino = temp_dir / "xl" / "media" / archivo_imagen
            if not archivo_destino.exists():
                print(f"    Archivo destino no encontrado: {archivo_destino}", flush=True)
                return False
            
            # Copy the new image over the old one
            shutil.copy2(ruta_nueva_imagen, archivo_destino)
            return True
            
        except Exception as e:
            print(f"    Error reemplazando imagen: {e}", flush=True)
            return False

    @classmethod
    def _reemplazar_imagenes_en_xlsx(
        cls,
        temp_dir: Path,
        imagenes: Dict[str, str]
    ) -> int:
        """
        Replace images in the XLSX based on their alternative text.
        
        Args:
            temp_dir: Temporary directory with extracted XLSX
            imagenes: Dict with {texto_alternativo: nombre_imagen}
                      e.g., {"logo_aseg_1": "mapfre", "bandera_aseg_2": "sura"}
                      
        Returns:
            Number of images replaced
        """
        if not imagenes:
            return 0
        
        print(f"  Buscando imagenes para reemplazar...", flush=True)
        print(f"  Imagenes configuradas: {imagenes}", flush=True)
        imagenes_reemplazadas = 0
        
        # Process drawings to find images by alternative text
        xl_drawings = temp_dir / "xl" / "drawings"
        if not xl_drawings.exists():
            print(f"  No se encontraron dibujos en el XLSX", flush=True)
            return 0
        
        for drawing_file in xl_drawings.glob("drawing*.xml"):
            # Read the drawing XML
            with open(drawing_file, 'rb') as f:
                contenido = f.read().decode('utf-8')
            
            # Debug: List all name and descr attributes in this drawing
            all_names = re.findall(r'name="([^"]+)"', contenido)
            all_descr = re.findall(r'descr="([^"]+)"', contenido)
            if all_names or all_descr:
                print(f"  {drawing_file.name} - names: {all_names[:10]}, descr: {all_descr[:10]}", flush=True)
            
            # Search for each configured image with EXACT match
            for texto_alt, nombre_imagen in imagenes.items():
                # Search for EXACT match of alternative text in name or descr attributes
                # Important: Use exact match to avoid replacing wrong images
                pattern_name_exact = rf'\bname="{re.escape(texto_alt)}"'
                pattern_descr_exact = rf'\bdescr="{re.escape(texto_alt)}"'
                
                match_name = re.search(pattern_name_exact, contenido)
                match_descr = re.search(pattern_descr_exact, contenido)
                
                if match_name:
                    print(f"    MATCH EXACTO en name='{texto_alt}'", flush=True)
                if match_descr:
                    print(f"    MATCH EXACTO en descr='{texto_alt}'", flush=True)
                
                if match_name or match_descr:
                    # Resolve the image path
                    ruta_imagen = cls._resolve_image_path(texto_alt, nombre_imagen)
                    if ruta_imagen:
                        # Replace the physical image file
                        if cls._reemplazar_archivo_imagen(temp_dir, drawing_file, texto_alt, ruta_imagen):
                            imagenes_reemplazadas += 1
                            print(f"    OK Imagen reemplazada: {texto_alt} -> {nombre_imagen}", flush=True)
        
        if imagenes_reemplazadas > 0:
            print(f"  Total imagenes reemplazadas: {imagenes_reemplazadas}", flush=True)
        else:
            print(f"  No se encontraron imagenes con los textos alternativos especificados", flush=True)
        
        return imagenes_reemplazadas

    @classmethod
    def _reemplazar_placeholders_en_xlsx(
        cls,
        ruta_entrada: Path,
        ruta_salida: Path,
        variables: Dict[str, str],
        imagenes: Optional[Dict[str, str]] = None
    ) -> int:
        """
        Replace placeholders in an XLSX preserving images, drawings, and page config.
        
        Works directly with internal XML files of the XLSX without modifying
        any configuration. Processes: cells, shared strings, text boxes, shapes, charts.
        Also replaces images based on alternative text.
        
        Args:
            ruta_entrada: Input XLSX file path
            ruta_salida: Output XLSX file path
            variables: Dictionary of {placeholder: value}
            imagenes: Optional dictionary of {texto_alternativo: nombre_imagen}
            
        Returns:
            Total number of replacements made
        """
        total_replacements = 0
        
        print(f"\n=== Procesando XLSX: {ruta_entrada.name} ===", flush=True)
        print(f"   Variables recibidas: {len(variables)}", flush=True)
        print(f"   Primeras 5 variables: {dict(list(variables.items())[:5])}", flush=True)
        if imagenes:
            print(f"   Imagenes a reemplazar: {len(imagenes)}", flush=True)
        
        # Check specifically for [1]
        if '[1]' in variables:
            print(f"   [1] ESTA en el JSON: {variables['[1]']}", flush=True)
        else:
            print(f"   [1] NO esta en el JSON!", flush=True)
            # Show all keys that start with [1
            keys_with_1 = [k for k in variables.keys() if '1' in k][:10]
            print(f"   Keys con '1': {keys_with_1}", flush=True)
        
        # Create temp directory
        temp_dir = Path(mkdtemp())

        try:
            # Extract XLSX (it's a ZIP file) preserving metadata
            with zipfile.ZipFile(ruta_entrada, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            print(f"   Extraido a: {temp_dir}", flush=True)

            # Process each worksheet (sheet*.xml) - cells
            xl_worksheets = temp_dir / "xl" / "worksheets"
            sheets_count = 0
            if xl_worksheets.exists():
                for sheet_file in xl_worksheets.glob("sheet*.xml"):
                    print(f"\n  Procesando hoja: {sheet_file.name}", flush=True)
                    repl = cls._reemplazar_en_xml(sheet_file, variables)
                    total_replacements += repl
                    sheets_count += 1
            print(f"  Procesadas {sheets_count} hojas", flush=True)

            # Process sharedStrings.xml (shared text between cells)
            shared_strings = temp_dir / "xl" / "sharedStrings.xml"
            if shared_strings.exists():
                print(f"\n  Procesando: sharedStrings.xml", flush=True)
                repl = cls._reemplazar_en_xml(shared_strings, variables)
                total_replacements += repl
                print(f"  Procesado texto compartido", flush=True)
            else:
                print(f"  No existe sharedStrings.xml", flush=True)
            
            # Process drawings (text boxes, shapes, objects with text)
            xl_drawings = temp_dir / "xl" / "drawings"
            drawings_count = 0
            if xl_drawings.exists():
                for drawing_file in xl_drawings.glob("*.xml"):
                    print(f"\n  Procesando drawing: {drawing_file.name}", flush=True)
                    
                    # DEBUG: Check if [1] is in this drawing file
                    if drawing_file.name == 'drawing1.xml':
                        with open(drawing_file, 'rb') as debug_f:
                            debug_content = debug_f.read().decode('utf-8')
                        if '[1]' in debug_content:
                            print(f"    DEBUG: [1] ENCONTRADO en {drawing_file.name}", flush=True)
                            idx = debug_content.find('[1]')
                            print(f"    DEBUG: Contexto: {repr(debug_content[idx-10:idx+10])}", flush=True)
                        else:
                            print(f"    DEBUG: [1] NO encontrado en {drawing_file.name}", flush=True)
                        
                        # Check if the key [1] exists in variables
                        test_key = '[1]'
                        print(f"    DEBUG: test_key '{test_key}' in variables: {test_key in variables}", flush=True)
                        print(f"    DEBUG: type(test_key): {type(test_key)}", flush=True)
                        print(f"    DEBUG: sample keys types: {[type(k) for k in list(variables.keys())[:3]]}", flush=True)
                    
                    repl = cls._reemplazar_en_xml(drawing_file, variables)
                    total_replacements += repl
                    drawings_count += 1
            if drawings_count > 0:
                print(f"  Procesados {drawings_count} dibujos", flush=True)
            
            # Process charts (charts with text labels)
            xl_charts = temp_dir / "xl" / "charts"
            charts_count = 0
            if xl_charts.exists():
                for chart_file in xl_charts.glob("*.xml"):
                    repl = cls._reemplazar_en_xml(chart_file, variables)
                    total_replacements += repl
                    charts_count += 1
            if charts_count > 0:
                print(f"  Procesados {charts_count} graficos", flush=True)
            
            # Replace images if specified
            if imagenes:
                cls._reemplazar_imagenes_en_xlsx(temp_dir, imagenes)

            print(f"\n  Re-empaquetando XLSX...", flush=True)
            
            # Re-package preserving exactly the original structure and compression
            with zipfile.ZipFile(ruta_entrada, 'r') as zip_entrada:
                with zipfile.ZipFile(ruta_salida, 'w', zipfile.ZIP_DEFLATED) as zip_salida:
                    for item in zip_entrada.infolist():
                        # Read file from temp directory (possibly modified)
                        file_path = temp_dir / item.filename
                        
                        if file_path.is_file():
                            # Read content (modified or not)
                            contenido = file_path.read_bytes()
                            
                            # Preserve original file info (compression, dates, etc.)
                            zip_salida.writestr(item, contenido, compress_type=item.compress_type)
                        elif not file_path.exists() and not item.is_dir():
                            # If file doesn't exist in temp (rare case), copy from original
                            contenido = zip_entrada.read(item.filename)
                            zip_salida.writestr(item, contenido, compress_type=item.compress_type)
            
            print(f"XLSX generado: {ruta_salida.name}", flush=True)
            print(f"   Total reemplazos: {total_replacements}", flush=True)

        finally:
            # Clean up temp directory
            shutil.rmtree(temp_dir, ignore_errors=True)
        
        return total_replacements

    @classmethod
    def generate_proposal(
        cls,
        template_name: str,
        variables: dict,
        imagenes: Optional[Dict[str, str]] = None
    ) -> tuple[Optional[io.BytesIO], Optional[str], Optional[str], Optional[str]]:
        """
        Generate a proposal document from a template with variable replacement.
        
        The generated file is saved to the shared volume (gestion_documental_ab)
        and also returned as a BytesIO buffer for immediate download.
        
        Uses the same technique as the original script: works directly with
        internal XML files to preserve all images, drawings, and formatting.
        
        Args:
            template_name: The name of the template to use (e.g., 'copropiedades')
            variables: Dictionary of variables to replace in the format {"[key]": "value"}
            imagenes: Optional dictionary of images to replace in the format
                      {"texto_alternativo": "nombre_imagen"}
                      e.g., {"logo_aseg_1": "mapfre", "bandera_aseg_2": "sura"}
            
        Returns:
            Tuple of (file_buffer, filename, saved_path, error_message)
            - On success: (BytesIO with Excel content, filename, path where saved, None)
            - On error: (None, None, None, error description)
        """
        # Validate template exists
        template_path = cls._get_template_path(template_name)
        if not template_path:
            available = ', '.join(cls.TEMPLATES.keys())
            return None, None, None, f"Template '{template_name}' not found. Available: {available}"
        
        # Validate variables
        if not variables or not isinstance(variables, dict):
            return None, None, None, "Variables dictionary is required"
        
        try:
            # Generate unique filename
            output_filename = cls._generate_unique_filename(template_name)
            
            # Ensure output directory exists and get path
            output_dir = cls._ensure_output_directory()
            saved_path = os.path.join(output_dir, output_filename)
            
            # Process the template using XML replacement (preserves everything)
            ruta_entrada = Path(template_path)
            ruta_salida = Path(saved_path)
            
            total_replacements = cls._reemplazar_placeholders_en_xlsx(
                ruta_entrada,
                ruta_salida,
                variables,
                imagenes
            )
            
            # Read the generated file into BytesIO for response
            output = io.BytesIO()
            with open(saved_path, 'rb') as f:
                output.write(f.read())
            output.seek(0)
            
            return output, output_filename, saved_path, None
            
        except Exception as e:
            return None, None, None, f"Error processing template: {str(e)}"

    @classmethod
    def validate_variables(cls, variables: dict) -> tuple[bool, Optional[str]]:
        """
        Validate the structure of variables dictionary.
        
        Args:
            variables: Dictionary to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not variables:
            return False, "Variables dictionary cannot be empty"
        
        if not isinstance(variables, dict):
            return False, "Variables must be a dictionary"
        
        # Check that all keys are in the expected format [n]
        invalid_keys = []
        for key in variables.keys():
            if not (key.startswith('[') and key.endswith(']')):
                invalid_keys.append(key)
        
        if invalid_keys:
            return False, f"Invalid variable keys (must be in format [n]): {invalid_keys[:5]}"
        
        return True, None
