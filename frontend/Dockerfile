# Usamos una imagen ligera de Nginx para producción
FROM nginx:alpine

# Copiamos los archivos estáticos al directorio público de Nginx
COPY index.html /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/

# Exponemos el puerto 80 estándar
EXPOSE 80