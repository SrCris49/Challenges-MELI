# Usa una imagen oficial de Python
FROM python:3.9-slim

# Crea y selecciona el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que usa Flask
EXPOSE 5000

# Comando para ejecutar la app
CMD ["flask", "run", "--host=0.0.0.0"]