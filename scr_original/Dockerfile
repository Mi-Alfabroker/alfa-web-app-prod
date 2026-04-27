FROM python:3.11-slim

# Instalar LibreOffice y dependencias
RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-writer \
    libreoffice-calc \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el script
COPY script_xlsx_pdf.py .

# Crear directorios para entrada/salida
RUN mkdir -p /input /output /tmp-xlsx

# Verificar que soffice está disponible
RUN which soffice && soffice --version