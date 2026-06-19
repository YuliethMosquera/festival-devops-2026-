import os
import time
from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Permite que el frontend consulte la API sin problemas de políticas CORS

# Configuración de la base de datos tomada de las variables de entorno
DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secret")
DB_NAME = os.getenv("DB_NAME", "festival_db")

def get_db_connection():
    """Intenta conectar a la base de datos con reintentos."""
    retries = 5
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            return conn
        except mysql.connector.Error:
            retries -= 1
            time.sleep(2)
    return None

def init_db():
    """Crea las tablas e inserta los datos iniciales si no existen."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        # Crear tabla de información del festival
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS festival_info (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                event_date VARCHAR(50)
            )
        """)
        # Crear tabla de artistas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS artists (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100)
            )
        """)
        
        # Verificar si ya hay datos
        cursor.execute("SELECT COUNT(*) FROM festival_info")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO festival_info (name, event_date) VALUES (%s, %s)", 
                           ("Pacific DevOps Music Fest", "17 de Octubre, 2026"))
            
            artists = [("The Docker Containers"), ("Kubernetes Pods"), ("The Microservices"), ("Flask & The Pythonistas")]
            cursor.executemany("INSERT INTO artists (name) VALUES (%s)", artists)
            conn.commit()
            
        cursor.close()
        conn.close()

# Inicializar Base de Datos al arrancar la API
init_db()

@app.route('/api/festival', methods=['GET'])
def get_festival_data():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Obtener info del festival
    cursor.execute("SELECT name, event_date FROM festival_info LIMIT 1")
    info = cursor.fetchone()
    
    # Obtener lista de artistas
    cursor.execute("SELECT name FROM artists")
    artists_rows = cursor.fetchall()
    artists_list = [row['name'] for row in artists_rows]
    
    cursor.close()
    conn.close()
    
    return jsonify({
        "name": info["name"] if info else "Pacific DevOps Music Fest",
        "date": info["event_date"] if info else "Por confirmar",
        "artists": artists_list
    })

if __name__ == '__main__':
    # Escuchar en todas las interfaces de red del contenedor en el puerto 5000
    app.run(host='0.0.0.0', port=5000)