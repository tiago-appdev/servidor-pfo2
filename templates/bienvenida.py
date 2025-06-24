# HTML para la página de bienvenida
BIENVENIDA_HTML = """
<!DOCTYPE html>
<html lang="es">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sistema de Gestión de Tareas</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
      background-color: #f5f5f5;
    }

    .container {
      background-color: white;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    h1 {
      color: #333;
      text-align: center;
      margin-bottom: 30px;
    }

    .welcome-message {
      background-color: #e8f5e8;
      padding: 20px;
      border-radius: 5px;
      margin-bottom: 30px;
      border-left: 4px solid #4CAF50;
    }

    .info-section {
      margin-bottom: 20px;
    }

    .info-section h3 {
      color: #555;
      border-bottom: 2px solid #4CAF50;
      padding-bottom: 5px;
    }

    .endpoints {
      background-color: #f8f9fa;
      padding: 15px;
      border-radius: 5px;
      margin: 10px 0;
    }

    .endpoint {
      margin: 10px 0;
      padding: 10px;
      background-color: white;
      border-radius: 3px;
      border-left: 3px solid #007bff;
    }

    .method {
      font-weight: bold;
      color: #007bff;
    }

    .footer {
      text-align: center;
      margin-top: 30px;
      padding-top: 20px;
      border-top: 1px solid #ddd;
      color: #666;
    }
  </style>
</head>

<body>
  <div class="container">
    <h1>🚀 Sistema de Gestión de Tareas</h1>

    <div class="welcome-message">
      <h2>¡Bienvenido al Sistema de Gestión de Tareas!</h2>
      <p>Esta API te permite registrar usuarios, iniciar sesión y gestionar tareas de manera segura.</p>
    </div>

    <div class="info-section">
      <h3>📋 Endpoints Disponibles</h3>
      <div class="endpoints">
        <div class="endpoint">
          <span class="method">POST</span> /registro
          <br><small>Registrar un nuevo usuario</small>
        </div>
        <div class="endpoint">
          <span class="method">POST</span> /login
          <br><small>Iniciar sesión con credenciales</small>
        </div>
        <div class="endpoint">
          <span class="method">GET</span> /tareas
          <br><small>Ver esta página de bienvenida</small>
        </div>
      </div>
    </div>

    <div class="info-section">
      <h3>🔐 Características de Seguridad</h3>
      <ul>
        <li>Contraseñas hasheadas con bcrypt</li>
        <li>Autenticación por sesión</li>
        <li>Base de datos SQLite persistente</li>
        <li>Validación de datos de entrada</li>
      </ul>
    </div>

    <div class="info-section">
      <h3>📊 Estado del Sistema</h3>
      <p><strong>Fecha y hora:</strong> {{ fecha_actual }}</p>
      <p><strong>Usuarios registrados:</strong> {{ total_usuarios }}</p>
      <p><strong>Estado:</strong> <span style="color: green;">✅ Operativo</span></p>
    </div>

    <div class="footer">
      <p>PFO2 - Sistema de Gestión de Tareas | Desarrollado con Flask y SQLite</p>
    </div>
  </div>
</body>

</html>
"""