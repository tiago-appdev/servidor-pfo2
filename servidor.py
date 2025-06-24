from flask import Flask, request, jsonify, render_template_string, session
import sqlite3
import bcrypt
import os
import bienvenida
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta'
app.config['DATABASE'] = 'database/tareas.db'

# Importar el HTML de bienvenida desde el archivo templates/bienvenida.py
BIENVENIDA_HTML = bienvenida.BIENVENIDA_HTML

def init_db():
    """Inicializa la base de datos y crea las tablas necesarias"""
    # Crear directorio si no existe
    os.makedirs('database', exist_ok=True)
    
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    # Crear tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contraseña_hash TEXT NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Crear tabla de tareas para futuras implementaciones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            completada BOOLEAN DEFAULT 0,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada correctamente")

def get_db_connection():
    """Obtiene una conexión a la base de datos"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    """Hashea una contraseña usando bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    """Verifica una contraseña contra su hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

@app.route('/')
def index():
    """Página de inicio que redirige a /tareas"""
    return """
    <h1>Sistema de Gestión de Tareas</h1>
    <p><a href="/tareas">Ir a la página principal</a></p>
    """

@app.route('/registro', methods=['POST'])
def registro():
    """Endpoint para registrar nuevos usuarios"""
    try:
        # Validar que se reciban los datos necesarios
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type debe ser application/json'
            }), 400
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No se recibieron datos JSON válidos'
            }), 400
        
        usuario = data.get('usuario')
        contraseña = data.get('contraseña')
        
        # Validar campos requeridos
        if not usuario or not contraseña:
            return jsonify({
                'error': 'Los campos usuario y contraseña son obligatorios'
            }), 400
        
        # Validar longitud mínima
        if len(usuario.strip()) < 3:
            return jsonify({
                'error': 'El nombre de usuario debe tener al menos 3 caracteres'
            }), 400
        
        if len(contraseña) < 4:
            return jsonify({
                'error': 'La contraseña debe tener al menos 4 caracteres'
            }), 400
        
        # Conectar a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si el usuario ya existe
        cursor.execute('SELECT id FROM usuarios WHERE usuario = ?', (usuario,))
        if cursor.fetchone():
            conn.close()
            return jsonify({
                'error': 'El usuario ya existe'
            }), 409
        
        # Hashear la contraseña
        contraseña_hash = hash_password(contraseña)
        
        # Insertar el nuevo usuario
        cursor.execute('''
            INSERT INTO usuarios (usuario, contraseña_hash) 
            VALUES (?, ?)
        ''', (usuario, contraseña_hash))
        
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'mensaje': 'Usuario registrado exitosamente',
            'usuario': usuario,
            'id': user_id
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': f'Error interno del servidor: {str(e)}'
        }), 500

@app.route('/login', methods=['POST'])
def login():
    """Endpoint para iniciar sesión"""
    try:
        # Validar que se reciban los datos necesarios
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type debe ser application/json'
            }), 400
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No se recibieron datos JSON válidos'
            }), 400
        
        usuario = data.get('usuario')
        contraseña = data.get('contraseña')
        
        # Validar campos requeridos
        if not usuario or not contraseña:
            return jsonify({
                'error': 'Los campos usuario y contraseña son obligatorios'
            }), 400
        
        # Conectar a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Buscar el usuario en la base de datos
        cursor.execute('SELECT id, usuario, contraseña_hash FROM usuarios WHERE usuario = ?', (usuario,))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({
                'error': 'Credenciales inválidas'
            }), 401
        
        # Verificar la contraseña
        if not verify_password(contraseña, user['contraseña_hash']):
            return jsonify({
                'error': 'Credenciales inválidas'
            }), 401
        
        # Guardar información de sesión
        session['user_id'] = user['id']
        session['usuario'] = user['usuario']
        
        return jsonify({
            'mensaje': 'Inicio de sesión exitoso',
            'usuario': user['usuario'],
            'id': user['id']
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Error interno del servidor: {str(e)}'
        }), 500

@app.route('/tareas', methods=['GET'])
def tareas():
    """Endpoint que muestra la página de bienvenida"""
    try:
        # Obtener estadísticas para mostrar en la página
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as total FROM usuarios')
        total_usuarios = cursor.fetchone()['total']
        
        conn.close()
        
        # Fecha actual
        fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        
        # Renderizar la página con datos dinámicos
        return render_template_string(
            BIENVENIDA_HTML,
            fecha_actual=fecha_actual,
            total_usuarios=total_usuarios
        )
        
    except Exception as e:
        return f"Error al cargar la página: {str(e)}", 500

@app.route('/logout', methods=['POST'])
def logout():
    """Endpoint para cerrar sesión"""
    session.clear()
    return jsonify({
        'mensaje': 'Sesión cerrada exitosamente'
    }), 200

@app.route('/status', methods=['GET'])
def status():
    """Endpoint para verificar el estado del servidor"""
    return jsonify({
        'status': 'ok',
        'mensaje': 'Servidor funcionando correctamente',
        'timestamp': datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    print("🚀 Inicializando Sistema de Gestión de Tareas...")
    init_db()
    print("🌐 Servidor iniciado en http://localhost:5000")
    print("📋 Endpoints disponibles:")
    print("   - POST /registro")
    print("   - POST /login")
    print("   - GET /tareas")
    print("   - POST /logout")
    print("   - GET /status")
    
    app.run(debug=True, host='0.0.0.0', port=5000)