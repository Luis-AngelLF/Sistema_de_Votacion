# Imagen base con Python 3.11 (ligera)
FROM python:3.11-slim

# Definir directorio de trabajo
WORKDIR /app

# Copiar los archivos al contenedor
COPY Suma_Cifrada.py .
COPY requirements.txt .

# Instalar dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto para ejecutar el script
CMD ["python", "Suma_Cifrada.py"]
