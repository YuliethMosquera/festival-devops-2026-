# Imagen base oficial de Python actualizada
FROM python:3.11-slim

# Directorio de trabajo interno
WORKDIR /app

# Copiar archivos de dependencias e instalar
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar todo el código fuente
COPY . .

# Exponer el puerto de Flask
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]