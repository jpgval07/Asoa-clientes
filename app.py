#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SERVIDOR ASOA - VERSIÓN RENDER
Sistema de Gestión de Clientes ASOA
Adaptado para despliegue en Render.com
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from datetime import datetime

class ClientesHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parsear la URL
        path = self.path.split('?')[0]
        
        if path == '/':
            self.mostrar_lista_clientes()
        elif path == '/nuevo':
            self.mostrar_formulario_nuevo()
        elif path.startswith('/ver/'):
            cliente_id = int(path.split('/')[-1])
            self.mostrar_detalle_cliente(cliente_id)
        elif path.startswith('/editar/'):
            cliente_id = int(path.split('/')[-1])
            self.mostrar_formulario_editar(cliente_id)
        else:
            self.send_error(404)
    
    def do_POST(self):
        # Parsear la URL
        path = self.path.split('?')[0]
        
        # Leer datos del formulario
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        form_data = urllib.parse.parse_qs(post_data)
        
        if path == '/guardar_nuevo':
            self.guardar_nuevo_cliente(form_data)
        elif path.startswith('/guardar_editar/'):
            cliente_id = int(path.split('/')[-1])
            self.guardar_cliente_editado(cliente_id, form_data)
        elif path.startswith('/eliminar/'):
            cliente_id = int(path.split('/')[-1])
            self.eliminar_cliente(cliente_id)
        else:
            self.send_error(404)

    def cargar_clientes(self):
        """Cargar clientes desde el archivo JSON"""
        try:
            with open('clientes_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Si no existe el archivo, crear estructura inicial
            clientes_inicial = {
                "clientes": [],
                "ultimo_id": 0
            }
            self.guardar_clientes(clientes_inicial)
            return clientes_inicial
        except json.JSONDecodeError:
            print("⚠️ Error al leer clientes_data.json, creando nuevo archivo")
            clientes_inicial = {
                "clientes": [],
                "ultimo_id": 0
            }
            self.guardar_clientes(clientes_inicial)
            return clientes_inicial

    def guardar_clientes(self, data):
        """Guardar clientes en el archivo JSON"""
        try:
            with open('clientes_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error al guardar clientes: {e}")

    def mostrar_lista_clientes(self):
        """Mostrar lista de todos los clientes"""
        data = self.cargar_clientes()
        clientes = data.get('clientes', [])
        
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASOA - Sistema de Gestión de Clientes</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
        }}
        .main-container {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            margin: 2rem auto;
            max-width: 1200px;
        }}
        .header-section {{
            background: linear-gradient(45deg, #2c3e50, #3498db);
            color: white;
            padding: 2rem;
            border-radius: 20px 20px 0 0;
            text-align: center;
        }}
        .stats-card {{
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 15px;
            padding: 1rem;
            margin: 0.5rem;
            text-align: center;
        }}
        .cliente-card {{
            background: white;
            border: none;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            margin-bottom: 1rem;
        }}
        .cliente-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }}
        .btn-action {{
            border-radius: 25px;
            padding: 0.5rem 1rem;
            margin: 0.2rem;
            transition: all 0.3s ease;
        }}
        .btn-action:hover {{
            transform: scale(1.05);
        }}
        .status-badge {{
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
        }}
        .status-activo {{ background: #d4edda; color: #155724; }}
        .status-inactivo {{ background: #f8d7da; color: #721c24; }}
        .status-pendiente {{ background: #fff3cd; color: #856404; }}
    </style>
</head>
<body>
    <div class="container-fluid p-4">
        <div class="main-container">
            <!-- Header -->
            <div class="header-section">
                <h1><i class="fas fa-users me-3"></i>ASOA - Sistema de Gestión</h1>
                <p class="mb-0">Control total de tu cartera de clientes</p>
                
                <!-- Stats -->
                <div class="row mt-3">
                    <div class="col-md-4">
                        <div class="stats-card">
                            <i class="fas fa-users fa-2x mb-2"></i>
                            <h3>{len(clientes)}</h3>
                            <p class="mb-0">Total Clientes</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="stats-card">
                            <i class="fas fa-chart-line fa-2x mb-2"></i>
                            <h3>{len([c for c in clientes if c.get('estado', 'activo') == 'activo'])}</h3>
                            <p class="mb-0">Activos</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="stats-card">
                            <i class="fas fa-clock fa-2x mb-2"></i>
                            <h3>{len([c for c in clientes if c.get('estado', 'activo') == 'pendiente'])}</h3>
                            <p class="mb-0">Pendientes</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Content -->
            <div class="p-4">
                <!-- Actions -->
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h2><i class="fas fa-list me-2"></i>Lista de Clientes</h2>
                    <a href="/nuevo" class="btn btn-success btn-action">
                        <i class="fas fa-plus me-2"></i>Nuevo Cliente
                    </a>
                </div>

                <!-- Clientes List -->
                <div class="row">
        """
        
        if not clientes:
            html += """
                    <div class="col-12">
                        <div class="alert alert-info text-center">
                            <i class="fas fa-info-circle fa-3x mb-3"></i>
                            <h4>No hay clientes registrados</h4>
                            <p>Comienza agregando tu primer cliente</p>
                            <a href="/nuevo" class="btn btn-primary btn-action">
                                <i class="fas fa-plus me-2"></i>Agregar Primer Cliente
                            </a>
                        </div>
                    </div>
            """
        else:
            for cliente in clientes:
                estado = cliente.get('estado', 'activo')
                estado_class = f'status-{estado}'
                telefono = cliente.get('telefono', 'No especificado')
                email = cliente.get('email', 'No especificado')
                
                html += f"""
                    <div class="col-md-6 col-lg-4">
                        <div class="card cliente-card">
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-start mb-2">
                                    <h5 class="card-title text-primary">
                                        <i class="fas fa-user me-2"></i>{cliente['nombre']}
                                    </h5>
                                    <span class="status-badge {estado_class}">{estado.title()}</span>
                                </div>
                                
                                <div class="mb-3">
                                    <small class="text-muted">
                                        <i class="fas fa-phone me-1"></i>{telefono}<br>
                                        <i class="fas fa-envelope me-1"></i>{email}
                                    </small>
                                </div>
                                
                                <div class="d-grid gap-2">
                                    <a href="/ver/{cliente['id']}" class="btn btn-outline-primary btn-sm btn-action">
                                        <i class="fas fa-eye me-1"></i>Ver Detalles
                                    </a>
                                    <div class="btn-group">
                                        <a href="/editar/{cliente['id']}" class="btn btn-outline-warning btn-sm">
                                            <i class="fas fa-edit me-1"></i>Editar
                                        </a>
                                        <button onclick="confirmarEliminar({cliente['id']}, '{cliente['nombre']}')" 
                                                class="btn btn-outline-danger btn-sm">
                                            <i class="fas fa-trash me-1"></i>Eliminar
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                """
        
        html += """
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function confirmarEliminar(id, nombre) {
            if (confirm(`¿Estás seguro de eliminar al cliente "${nombre}"?\\n\\nEsta acción no se puede deshacer.`)) {
                // Crear formulario para eliminar
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = `/eliminar/${id}`;
                document.body.appendChild(form);
                form.submit();
            }
        }
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def mostrar_formulario_nuevo(self):
        """Mostrar formulario para nuevo cliente"""
        html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nuevo Cliente - ASOA</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
        }
        .form-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            margin: 2rem auto;
            max-width: 800px;
        }
        .form-header {
            background: linear-gradient(45deg, #2c3e50, #3498db);
            color: white;
            padding: 2rem;
            border-radius: 20px 20px 0 0;
            text-align: center;
        }
        .form-section {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        .form-section h5 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }
        .btn-action {
            border-radius: 25px;
            padding: 0.75rem 2rem;
            transition: all 0.3s ease;
        }
        .btn-action:hover {
            transform: scale(1.05);
        }
    </style>
</head>
<body>
    <div class="container p-4">
        <div class="form-container">
            <div class="form-header">
                <h1><i class="fas fa-user-plus me-3"></i>Nuevo Cliente</h1>
                <p class="mb-0">Completa la información del cliente</p>
            </div>
            
            <div class="p-4">
                <form method="POST" action="/guardar_nuevo">
                    <!-- Información Básica -->
                    <div class="form-section">
                        <h5><i class="fas fa-user me-2"></i>Información Personal</h5>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Nombre Completo *</label>
                                <input type="text" class="form-control" name="nombre" required>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Teléfono</label>
                                <input type="tel" class="form-control" name="telefono">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Email</label>
                                <input type="email" class="form-control" name="email">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Estado</label>
                                <select class="form-control" name="estado">
                                    <option value="activo">Activo</option>
                                    <option value="inactivo">Inactivo</option>
                                    <option value="pendiente">Pendiente</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- Información Comercial -->
                    <div class="form-section">
                        <h5><i class="fas fa-briefcase me-2"></i>Información Comercial</h5>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Empresa</label>
                                <input type="text" class="form-control" name="empresa">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Cargo</label>
                                <input type="text" class="form-control" name="cargo">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Sector</label>
                                <input type="text" class="form-control" name="sector">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Fuente de Contacto</label>
                                <select class="form-control" name="fuente">
                                    <option value="">Seleccionar...</option>
                                    <option value="referido">Referido</option>
                                    <option value="web">Página Web</option>
                                    <option value="redes">Redes Sociales</option>
                                    <option value="evento">Evento</option>
                                    <option value="llamada">Llamada Fría</option>
                                    <option value="otro">Otro</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- Fechas Importantes -->
                    <div class="form-section">
                        <h5><i class="fas fa-calendar me-2"></i>Fechas Importantes</h5>
                        <div class="row">
                            <div class="col-md-4 mb-3">
                                <label class="form-label">Primer Contacto</label>
                                <input type="date" class="form-control" name="fecha_contacto">
                            </div>
                            <div class="col-md-4 mb-3">
                                <label class="form-label">Última Interacción</label>
                                <input type="date" class="form-control" name="fecha_interaccion">
                            </div>
                            <div class="col-md-4 mb-3">
                                <label class="form-label">Próximo Seguimiento</label>
                                <input type="date" class="form-control" name="fecha_seguimiento">
                            </div>
                        </div>
                    </div>

                    <!-- Información Adicional -->
                    <div class="form-section">
                        <h5><i class="fas fa-sticky-note me-2"></i>Información Adicional</h5>
                        <div class="mb-3">
                            <label class="form-label">Dirección</label>
                            <textarea class="form-control" name="direccion" rows="2"></textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Notas</label>
                            <textarea class="form-control" name="notas" rows="3" placeholder="Información adicional, preferencias, historial, etc."></textarea>
                        </div>
                    </div>

                    <!-- Botones -->
                    <div class="text-center mt-4">
                        <a href="/" class="btn btn-secondary btn-action me-3">
                            <i class="fas fa-arrow-left me-2"></i>Cancelar
                        </a>
                        <button type="submit" class="btn btn-success btn-action">
                            <i class="fas fa-save me-2"></i>Guardar Cliente
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def guardar_nuevo_cliente(self, form_data):
        """Guardar nuevo cliente"""
        data = self.cargar_clientes()
        
        # Incrementar ID
        data['ultimo_id'] += 1
        nuevo_id = data['ultimo_id']
        
        # Crear nuevo cliente
        nuevo_cliente = {
            'id': nuevo_id,
            'nombre': form_data.get('nombre', [''])[0],
            'telefono': form_data.get('telefono', [''])[0],
            'email': form_data.get('email', [''])[0],
            'estado': form_data.get('estado', ['activo'])[0],
            'empresa': form_data.get('empresa', [''])[0],
            'cargo': form_data.get('cargo', [''])[0],
            'sector': form_data.get('sector', [''])[0],
            'fuente': form_data.get('fuente', [''])[0],
            'direccion': form_data.get('direccion', [''])[0],
            'notas': form_data.get('notas', [''])[0],
            'fecha_contacto': form_data.get('fecha_contacto', [''])[0],
            'fecha_interaccion': form_data.get('fecha_interaccion', [''])[0],
            'fecha_seguimiento': form_data.get('fecha_seguimiento', [''])[0],
            'fecha_creacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Agregar a la lista
        data['clientes'].append(nuevo_cliente)
        
        # Guardar
        self.guardar_clientes(data)
        
        # Redirigir
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def mostrar_detalle_cliente(self, cliente_id):
        """Mostrar detalles completos de un cliente"""
        data = self.cargar_clientes()
        cliente = None
        
        for c in data['clientes']:
            if c['id'] == cliente_id:
                cliente = c
                break
        
        if not cliente:
            self.send_error(404)
            return
        
        # Función para formatear fechas
        def formatear_fecha(fecha_str):
            if not fecha_str:
                return "No especificada"
            try:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
                return fecha.strftime('%d/%m/%Y')
            except:
                return fecha_str
        
        estado_class = f'status-{cliente.get("estado", "activo")}'
        
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cliente: {cliente['nombre']} - ASOA</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
        }}
        .detail-container {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            margin: 2rem auto;
            max-width: 1000px;
        }}
        .detail-header {{
            background: linear-gradient(45deg, #2c3e50, #3498db);
            color: white;
            padding: 2rem;
            border-radius: 20px 20px 0 0;
        }}
        .info-section {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
        }}
        .info-section h5 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }}
        .info-item {{
            background: white;
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
            border-left: 4px solid #3498db;
        }}
        .btn-action {{
            border-radius: 25px;
            padding: 0.75rem 2rem;
            transition: all 0.3s ease;
        }}
        .btn-action:hover {{
            transform: scale(1.05);
        }}
        .status-badge {{
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: bold;
        }}
        .status-activo {{ background: #d4edda; color: #155724; }}
        .status-inactivo {{ background: #f8d7da; color: #721c24; }}
        .status-pendiente {{ background: #fff3cd; color: #856404; }}
    </style>
</head>
<body>
    <div class="container p-4">
        <div class="detail-container">
            <div class="detail-header">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h1><i class="fas fa-user me-3"></i>{cliente['nombre']}</h1>
                        <p class="mb-0">Información completa del cliente</p>
                    </div>
                    <span class="status-badge {estado_class}">
                        {cliente.get('estado', 'activo').title()}
                    </span>
                </div>
            </div>
            
            <div class="p-4">
                <!-- Información Personal -->
                <div class="info-section">
                    <h5><i class="fas fa-user me-2"></i>Información Personal</h5>
                    <div class="row">
                        <div class="col-md-6">
                            <div class="info-item">
                                <strong><i class="fas fa-phone me-2"></i>Teléfono:</strong><br>
                                {cliente.get('telefono', 'No especificado')}
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="info-item">
                                <strong><i class="fas fa-envelope me-2"></i>Email:</strong><br>
                                {cliente.get('email', 'No especificado')}
                            </div>
                        </div>
                        <div class="col-12">
                            <div class="info-item">
                                <strong><i class="fas fa-map-marker-alt me-2"></i>Dirección:</strong><br>
                                {cliente.get('direccion', 'No especificada') or 'No especificada'}
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Información Comercial -->
                <div class="info-section">
                    <h5><i class="fas fa-briefcase me-2"></i>Información Comercial</h5>
                    <div class="row">
                        <div class="col-md-6">
                            <div class="info-item">
                                <strong><i class="fas fa-building me-2"></i>Empresa:</strong><br>
                                {cliente.get('empresa', 'No especificada') or 'No especificada'}
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="info-item">
                                <strong><i class="fas fa-user-tie me-2"></i>Cargo:</strong><br>
                                {cliente.get('cargo', 'No especificado') or 'No especificado'}
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="info-item">
                                <strong><i class="fas fa-industry me-2"></i>Sector:</strong><br>
                                {cliente.get('sector', 'No especificado') or 'No especificado'}
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="info-item">
                                <strong><i class="fas fa-handshake me-2"></i>Fuente de Contacto:</strong><br>
                                {cliente.get('fuente', 'No especificada') or 'No especificada'}
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Fechas Importantes -->
                <div class="info-section">
                    <h5><i class="fas fa-calendar me-2"></i>Fechas Importantes</h5>
                    <div class="row">
                        <div class="col-md-4">
                            <div class="info-item">
                                <strong><i class="fas fa-calendar-plus me-2"></i>Primer Contacto:</strong><br>
                                {formatear_fecha(cliente.get('fecha_contacto', ''))}
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="info-item">
                                <strong><i class="fas fa-calendar-check me-2"></i>Última Interacción:</strong><br>
                                {formatear_fecha(cliente.get('fecha_interaccion', ''))}
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="info-item">
                                <strong><i class="fas fa-calendar-day me-2"></i>Próximo Seguimiento:</strong><br>
                                {formatear_fecha(cliente.get('fecha_seguimiento', ''))}
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Notas -->
                <div class="info-section">
                    <h5><i class="fas fa-sticky-note me-2"></i>Notas</h5>
                    <div class="info-item">
                        {cliente.get('notas', 'Sin notas registradas') or 'Sin notas registradas'}
                    </div>
                </div>

                <!-- Información del Sistema -->
                <div class="info-section">
                    <h5><i class="fas fa-info-circle me-2"></i>Información del Sistema</h5>
                    <div class="row">
                        <div class="col-md-6">
                            <div class="info-item">
                                <strong><i class="fas fa-calendar-alt me-2"></i>Fecha de Creación:</strong><br>
                                {cliente.get('fecha_creacion', 'No disponible')}
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="info-item">
                                <strong><i class="fas fa-hashtag me-2"></i>ID Cliente:</strong><br>
                                #{cliente['id']:04d}
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Botones de Acción -->
                <div class="text-center mt-4">
                    <a href="/" class="btn btn-secondary btn-action me-2">
                        <i class="fas fa-arrow-left me-2"></i>Volver a Lista
                    </a>
                    <a href="/editar/{cliente['id']}" class="btn btn-warning btn-action me-2">
                        <i class="fas fa-edit me-2"></i>Editar Cliente
                    </a>
                    <button onclick="confirmarEliminar({cliente['id']}, '{cliente['nombre']}')" 
                            class="btn btn-danger btn-action">
                        <i class="fas fa-trash me-2"></i>Eliminar Cliente
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function confirmarEliminar(id, nombre) {{
            if (confirm(`¿Estás seguro de eliminar al cliente "${{nombre}}"?\\n\\nEsta acción no se puede deshacer.`)) {{
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = `/eliminar/${{id}}`;
                document.body.appendChild(form);
                form.submit();
            }}
        }}
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def mostrar_formulario_editar(self, cliente_id):
        """Mostrar formulario para editar cliente"""
        data = self.cargar_clientes()
        cliente = None
        
        for c in data['clientes']:
            if c['id'] == cliente_id:
                cliente = c
                break
        
        if not cliente:
            self.send_error(404)
            return
        
        # Función para crear select con opción seleccionada
        def crear_select_estado(valor_actual):
            opciones = ['activo', 'inactivo', 'pendiente']
            html = ""
            for opcion in opciones:
                selected = 'selected' if opcion == valor_actual else ''
                html += f'<option value="{opcion}" {selected}>{opcion.title()}</option>'
            return html
        
        def crear_select_fuente(valor_actual):
            opciones = [
                ('', 'Seleccionar...'),
                ('referido', 'Referido'),
                ('web', 'Página Web'),
                ('redes', 'Redes Sociales'),
                ('evento', 'Evento'),
                ('llamada', 'Llamada Fría'),
                ('otro', 'Otro')
            ]
            html = ""
            for valor, texto in opciones:
                selected = 'selected' if valor == valor_actual else ''
                html += f'<option value="{valor}" {selected}>{texto}</option>'
            return html
        
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editar Cliente: {cliente['nombre']} - ASOA</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
        }}
        .form-container {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            margin: 2rem auto;
            max-width: 800px;
        }}
        .form-header {{
            background: linear-gradient(45deg, #2c3e50, #3498db);
            color: white;
            padding: 2rem;
            border-radius: 20px 20px 0 0;
            text-align: center;
        }}
        .form-section {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
        }}
        .form-section h5 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }}
        .btn-action {{
            border-radius: 25px;
            padding: 0.75rem 2rem;
            transition: all 0.3s ease;
        }}
        .btn-action:hover {{
            transform: scale(1.05);
        }}
    </style>
</head>
<body>
    <div class="container p-4">
        <div class="form-container">
            <div class="form-header">
                <h1><i class="fas fa-user-edit me-3"></i>Editar Cliente</h1>
                <p class="mb-0">Modificar información de: <strong>{cliente['nombre']}</strong></p>
            </div>
            
            <div class="p-4">
                <form method="POST" action="/guardar_editar/{cliente['id']}">
                    <!-- Información Básica -->
                    <div class="form-section">
                        <h5><i class="fas fa-user me-2"></i>Información Personal</h5>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Nombre Completo *</label>
                                <input type="text" class="form-control" name="nombre" value="{cliente['nombre']}" required>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Teléfono</label>
                                <input type="tel" class="form-control" name="telefono" value="{cliente.get('telefono', '')}">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Email</label>
                                <input type="email" class="form-control" name="email" value="{cliente.get('email', '')}">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Estado</label>
                                <select class="form-control" name="estado">
                                    {crear_select_estado(cliente.get('estado', 'activo'))}
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- Información Comercial -->
                    <div class="form-section">
                        <h5><i class="fas fa-briefcase me-2"></i>Información Comercial</h5>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Empresa</label>
                                <input type="text" class="form-control" name="empresa" value="{cliente.get('empresa', '')}">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Cargo</label>
                                <input type="text" class="form-control" name="cargo" value="{cliente.get('cargo', '')}">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Sector</label>
                                <input type="text" class="form-control" name="sector" value="{cliente.get('sector', '')}">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Fuente de Contacto</label>
                                <select class="form-control" name="fuente">
                                    {crear_select_fuente(cliente.get('fuente', ''))}
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- Fechas Importantes -->
                    <div class="form-section">
                        <h5><i class="fas fa-calendar me-2"></i>Fechas Importantes</h5>
                        <div class="row">
                            <div class="col-md-4 mb-3">
                                <label class="form-label">Primer Contacto</label>
                                <input type="date" class="form-control" name="fecha_contacto" value="{cliente.get('fecha_contacto', '')}">
                            </div>
                            <div class="col-md-4 mb-3">
                                <label class="form-label">Última Interacción</label>
                                <input type="date" class="form-control" name="fecha_interaccion" value="{cliente.get('fecha_interaccion', '')}">
                            </div>
                            <div class="col-md-4 mb-3">
                                <label class="form-label">Próximo Seguimiento</label>
                                <input type="date" class="form-control" name="fecha_seguimiento" value="{cliente.get('fecha_seguimiento', '')}">
                            </div>
                        </div>
                    </div>

                    <!-- Información Adicional -->
                    <div class="form-section">
                        <h5><i class="fas fa-sticky-note me-2"></i>Información Adicional</h5>
                        <div class="mb-3">
                            <label class="form-label">Dirección</label>
                            <textarea class="form-control" name="direccion" rows="2">{cliente.get('direccion', '')}</textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Notas</label>
                            <textarea class="form-control" name="notas" rows="3" placeholder="Información adicional, preferencias, historial, etc.">{cliente.get('notas', '')}</textarea>
                        </div>
                    </div>

                    <!-- Botones -->
                    <div class="text-center mt-4">
                        <a href="/ver/{cliente['id']}" class="btn btn-secondary btn-action me-2">
                            <i class="fas fa-arrow-left me-2"></i>Cancelar
                        </a>
                        <a href="/" class="btn btn-outline-secondary btn-action me-2">
                            <i class="fas fa-list me-2"></i>Lista
                        </a>
                        <button type="submit" class="btn btn-success btn-action">
                            <i class="fas fa-save me-2"></i>Guardar Cambios
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def guardar_cliente_editado(self, cliente_id, form_data):
        """Guardar cambios en cliente existente"""
        data = self.cargar_clientes()
        
        # Encontrar el cliente
        for i, cliente in enumerate(data['clientes']):
            if cliente['id'] == cliente_id:
                # Actualizar datos
                data['clientes'][i].update({
                    'nombre': form_data.get('nombre', [''])[0],
                    'telefono': form_data.get('telefono', [''])[0],
                    'email': form_data.get('email', [''])[0],
                    'estado': form_data.get('estado', ['activo'])[0],
                    'empresa': form_data.get('empresa', [''])[0],
                    'cargo': form_data.get('cargo', [''])[0],
                    'sector': form_data.get('sector', [''])[0],
                    'fuente': form_data.get('fuente', [''])[0],
                    'direccion': form_data.get('direccion', [''])[0],
                    'notas': form_data.get('notas', [''])[0],
                    'fecha_contacto': form_data.get('fecha_contacto', [''])[0],
                    'fecha_interaccion': form_data.get('fecha_interaccion', [''])[0],
                    'fecha_seguimiento': form_data.get('fecha_seguimiento', [''])[0],
                })
                break
        
        # Guardar
        self.guardar_clientes(data)
        
        # Redirigir al detalle
        self.send_response(302)
        self.send_header('Location', f'/ver/{cliente_id}')
        self.end_headers()

    def eliminar_cliente(self, cliente_id):
        """Eliminar cliente"""
        data = self.cargar_clientes()
        
        # Filtrar cliente
        data['clientes'] = [c for c in data['clientes'] if c['id'] != cliente_id]
        
        # Guardar
        self.guardar_clientes(data)
        
        # Redirigir
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

if __name__ == '__main__':
    # Puerto para Render (toma del entorno o usa 8000 por defecto)
    port = int(os.environ.get('PORT', 8000))
    
    print("=" * 60)
    print("🌐 SERVIDOR ASOA - VERSIÓN RENDER")
    print("=" * 60)
    print(f"🚀 Puerto: {port}")
    print("✅ Listo para despliegue en Render")
    print("=" * 60)
    
    try:
        server = HTTPServer(('0.0.0.0', port), ClientesHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
    except Exception as e:
        print(f"\n❌ Error: {e}")
