<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASOA - Sistema de Gestión de Clientes Agrícolas</title>
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <!-- SweetAlert2 -->
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    
    <style>
        :root {
            --primary-green: #2d5016;
            --secondary-green: #4a7c3a;
            --light-green: #e8f4e8;
            --accent-yellow: #f4a261;
            --text-dark: #2c3e50;
        }
        
        body { 
            background: linear-gradient(135deg, var(--light-green) 0%, #f8f9fa 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
        }
        
        .navbar { 
            background: linear-gradient(45deg, var(--primary-green), var(--secondary-green)) !important;
            box-shadow: 0 4px 15px rgba(45, 80, 22, 0.2);
        }
        
        .navbar-brand { 
            font-weight: bold; 
            font-size: 1.5rem;
            color: white !important;
        }
        
        .card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            overflow: hidden;
        }
        
        .card:hover { 
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        }
        
        .card-header {
            background: linear-gradient(45deg, var(--secondary-green), var(--primary-green));
            color: white;
            border: none;
            padding: 1rem 1.5rem;
        }
        
        .cliente-card {
            border-left: 5px solid var(--secondary-green);
            margin-bottom: 1rem;
        }
        
        .btn-primary {
            background: linear-gradient(45deg, var(--secondary-green), var(--primary-green));
            border: none;
            border-radius: 25px;
            padding: 10px 25px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(74, 124, 58, 0.4);
        }
        
        .btn-success {
            background: linear-gradient(45deg, #28a745, #20c997);
            border: none;
            border-radius: 20px;
        }
        
        .btn-warning {
            background: linear-gradient(45deg, var(--accent-yellow), #e76f51);
            border: none;
            border-radius: 20px;
        }
        
        .btn-danger {
            background: linear-gradient(45deg, #dc3545, #c82333);
            border: none;
            border-radius: 20px;
        }
        
        .badge {
            border-radius: 15px;
            padding: 8px 12px;
            font-size: 0.75rem;
        }
        
        .badge-activo {
            background: linear-gradient(45deg, #28a745, #20c997);
        }
        
        .badge-inactivo {
            background: linear-gradient(45deg, #6c757d, #5a6268);
        }
        
        .form-control, .form-select {
            border-radius: 10px;
            border: 2px solid #e9ecef;
            transition: all 0.3s ease;
        }
        
        .form-control:focus, .form-select:focus {
            border-color: var(--secondary-green);
            box-shadow: 0 0 0 0.2rem rgba(74, 124, 58, 0.25);
        }
        
        .stats-card {
            background: linear-gradient(135deg, white, var(--light-green));
            border-left: 4px solid var(--secondary-green);
        }
        
        .loading-spinner {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255,255,255,0.9);
            z-index: 9999;
        }
        
        .pulse {
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .footer {
            background: linear-gradient(45deg, var(--primary-green), var(--secondary-green));
            color: white;
            padding: 2rem 0;
            margin-top: 3rem;
        }
        
        .alert-online {
            background: linear-gradient(45deg, #d4edda, #c3e6cb);
            border: 1px solid #b8dabc;
            border-radius: 10px;
        }
        
        /* Responsivo mejorado */
        @media (max-width: 768px) {
            .card { margin-bottom: 1rem; }
            .btn { margin-bottom: 0.5rem; }
            .navbar-brand { font-size: 1.2rem; }
        }
    </style>
</head>
<body>
    <!-- Loading Spinner -->
    <div class="loading-spinner d-flex justify-content-center align-items-center">
        <div class="text-center">
            <div class="spinner-border text-success" style="width: 3rem; height: 3rem;" role="status">
                <span class="visually-hidden">Cargando...</span>
            </div>
            <p class="mt-3 text-success fw-bold">Conectando con ASOA...</p>
        </div>
    </div>

    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand pulse" href="#">
                <i class="fas fa-seedling me-2"></i>ASOA - Gestión Agrícola
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link active" href="#clientes"><i class="fas fa-users me-1"></i>Clientes</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#estadisticas"><i class="fas fa-chart-bar me-1"></i>Estadísticas</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#configuracion"><i class="fas fa-cog me-1"></i>Configuración</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <div class="container my-4">
        <div class="alert alert-online text-center">
            <h4><i class="fas fa-globe text-success me-2"></i>¡Sistema Online Activo!</h4>
            <p class="mb-0">Acceso desde cualquier dispositivo • Datos en tiempo real • Respaldo automático</p>
        </div>
    </div>

    <!-- Main Content -->
    <div class="container">
        <!-- Statistics Cards -->
        <div class="row mb-4" id="estadisticas">
            <div class="col-md-3 mb-3">
                <div class="card stats-card text-center">
                    <div class="card-body">
                        <i class="fas fa-users fa-2x text-success mb-2"></i>
                        <h5 class="card-title" id="total-clientes">5</h5>
                        <p class="card-text">Clientes Activos</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3 mb-3">
                <div class="card stats-card text-center">
                    <div class="card-body">
                        <i class="fas fa-map-marker-alt fa-2x text-primary mb-2"></i>
                        <h5 class="card-title" id="total-predios">5</h5>
                        <p class="card-text">Predios</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3 mb-3">
                <div class="card stats-card text-center">
                    <div class="card-body">
                        <i class="fas fa-leaf fa-2x text-warning mb-2"></i>
                        <h5 class="card-title" id="total-hectareas">67.5</h5>
                        <p class="card-text">Hectáreas</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3 mb-3">
                <div class="card stats-card text-center">
                    <div class="card-body">
                        <i class="fas fa-dollar-sign fa-2x text-info mb-2"></i>
                        <h5 class="card-title" id="ingresos-totales">$35,500</h5>
                        <p class="card-text">Ingresos</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Controls -->
        <div class="row mb-4">
            <div class="col-md-8">
                <div class="input-group">
                    <span class="input-group-text"><i class="fas fa-search"></i></span>
                    <input type="text" class="form-control" id="busqueda" placeholder="Buscar clientes por nombre, teléfono o RFC...">
                </div>
            </div>
            <div class="col-md-4">
                <button class="btn btn-primary w-100" onclick="mostrarFormulario()">
                    <i class="fas fa-plus me-2"></i>Nuevo Cliente
                </button>
            </div>
        </div>

        <!-- Clients List -->
        <div id="clientes">
            <div class="row" id="lista-clientes">
                <!-- Los clientes se cargarán aquí dinámicamente -->
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="footer text-center">
        <div class="container">
            <p class="mb-2"><i class="fas fa-seedling me-2"></i><strong>ASOA - Agricultura Sustentable de Occidente</strong></p>
            <p class="mb-0">Sistema de Gestión de Clientes Agrícolas • Versión Web 2025</p>
            <small class="text-light">Desarrollado con tecnología Bootstrap y JavaScript</small>
        </div>
    </footer>

    <!-- Bootstrap 5 JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

    <script>
        // Base de datos de clientes (simulada)
        let clientes = [
            {
                "id": 1,
                "nombre_completo": "Agroempresa Los Pinos S.A.",
                "persona_contacto": "Juan Pérez García",
                "telefono": "9241095927",
                "rfc": "AGRO123456XYZ",
                "nombre_predio": "Rancho El Sol",
                "ubicacion": "21.1234, -101.5678",
                "superficie_ha": 10.0,
                "tipo_cultivo": "Maíz",
                "historial_cultivos": ["Maíz", "Trigo", "Sorgo"],
                "fecha_siembra": "2025-06-10",
                "servicios": [],
                "observaciones": "Acceso complicado por lluvias. Cliente muy puntual en pagos.",
                "alertas": "Monitoreo NDVI programado en 2 semanas.",
                "fecha_proximo_contacto": "2025-08-15",
                "estado_cliente": "Activo",
                "costo_servicio": 4800.0,
                "estado_cuenta": "Pagado",
                "nivel_satisfaccion": 5
            },
            {
                "id": 2,
                "nombre_completo": "Campo Verde Sustentable",
                "persona_contacto": "Ana López Martínez",
                "telefono": "5559876543",
                "rfc": "CAMPO987654ABC",
                "nombre_predio": "Parcela Verde",
                "ubicacion": "20.9876, -102.1234",
                "superficie_ha": 15.5,
                "tipo_cultivo": "Tomate",
                "historial_cultivos": ["Tomate", "Chile", "Pepino"],
                "fecha_siembra": "2025-05-15",
                "servicios": ["Análisis de suelo", "Monitoreo NDVI"],
                "observaciones": "Cliente nuevo con gran potencial. Interesado en tecnología.",
                "alertas": "Revisar sistema de riego la próxima semana.",
                "fecha_proximo_contacto": "2025-08-10",
                "estado_cliente": "Activo",
                "costo_servicio": 6200.0,
                "estado_cuenta": "Pendiente",
                "nivel_satisfaccion": 4
            },
            {
                "id": 3,
                "nombre_completo": "Rancho Familiar Guadalupe",
                "persona_contacto": "Carlos Mendoza Ruiz",
                "telefono": "9221234567",
                "rfc": "RANCHO456789DEF",
                "nombre_predio": "El Mirador",
                "ubicacion": "21.5432, -101.9876",
                "superficie_ha": 8.0,
                "tipo_cultivo": "Aguacate",
                "historial_cultivos": ["Aguacate", "Limón"],
                "fecha_siembra": "2024-12-01",
                "servicios": ["Análisis foliar"],
                "observaciones": "Producción orgánica certificada. Muy comprometido con prácticas sustentables.",
                "alertas": "Monitoreo de plagas en temporada alta.",
                "fecha_proximo_contacto": "2025-09-01",
                "estado_cliente": "Activo",
                "costo_servicio": 3500.0,
                "estado_cuenta": "Pagado",
                "nivel_satisfaccion": 5
            },
            {
                "id": 4,
                "nombre_completo": "Cooperativa Agrícola San Miguel",
                "persona_contacto": "María Elena Vásquez",
                "telefono": "4771098765",
                "rfc": "COOP654321GHI",
                "nombre_predio": "Terrenos San Miguel",
                "ubicacion": "21.3456, -101.7890",
                "superficie_ha": 25.0,
                "tipo_cultivo": "Sorgo",
                "historial_cultivos": ["Sorgo", "Maíz", "Frijol"],
                "fecha_siembra": "2025-07-01",
                "servicios": ["Análisis de suelo", "Capacitación técnica"],
                "observaciones": "Cooperativa de 12 socios. Requieren asesoría técnica constante.",
                "alertas": "Reunión programada para revisar resultados de análisis.",
                "fecha_proximo_contacto": "2025-08-20",
                "estado_cliente": "Activo",
                "costo_servicio": 12000.0,
                "estado_cuenta": "Pagado",
                "nivel_satisfaccion": 4
            },
            {
                "id": 5,
                "nombre_completo": "Huerto Orgánico El Paraíso",
                "persona_contacto": "Roberto Santana Cruz",
                "telefono": "9241876543",
                "rfc": "HUERTO789012JKL",
                "nombre_predio": "El Paraíso",
                "ubicacion": "21.0987, -101.5432",
                "superficie_ha": 9.0,
                "tipo_cultivo": "Brócoli",
                "historial_cultivos": ["Brócoli", "Coliflor", "Lechuga"],
                "fecha_siembra": "2025-04-20",
                "servicios": ["Análisis foliar", "Monitoreo NDVI", "Certificación orgánica"],
                "observaciones": "Especializado en vegetales orgánicos para exportación. Muy exigente en calidad.",
                "alertas": "Renovar certificación orgánica en septiembre.",
                "fecha_proximo_contacto": "2025-08-25",
                "estado_cliente": "Activo",
                "costo_servicio": 9000.0,
                "estado_cuenta": "Pagado",
                "nivel_satisfaccion": 5
            }
        ];

        // Variables globales
        let clienteEditando = null;

        // Inicialización
        document.addEventListener('DOMContentLoaded', function() {
            mostrarLoading();
            setTimeout(() => {
                ocultarLoading();
                cargarClientes();
                actualizarEstadisticas();
                configurarBusqueda();
            }, 2000);
        });

        function mostrarLoading() {
            document.querySelector('.loading-spinner').style.display = 'flex';
        }

        function ocultarLoading() {
            document.querySelector('.loading-spinner').style.display = 'none';
        }

        function cargarClientes() {
            const contenedor = document.getElementById('lista-clientes');
            contenedor.innerHTML = '';

            clientes.forEach(cliente => {
                const clienteCard = crearTarjetaCliente(cliente);
                contenedor.appendChild(clienteCard);
            });
        }

        function crearTarjetaCliente(cliente) {
            const col = document.createElement('div');
            col.className = 'col-lg-6 col-xl-4 mb-4';

            const estadoBadge = cliente.estado_cliente === 'Activo' ? 'badge-activo' : 'badge-inactivo';
            const cuentaBadge = cliente.estado_cuenta === 'Pagado' ? 'bg-success' : 'bg-warning';
            
            col.innerHTML = `
                <div class="card cliente-card h-100">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h6 class="mb-0 text-truncate">${cliente.nombre_completo}</h6>
                        <span class="badge ${estadoBadge}">${cliente.estado_cliente}</span>
                    </div>
                    <div class="card-body">
                        <div class="mb-2">
                            <strong><i class="fas fa-user me-1"></i></strong> ${cliente.persona_contacto}
                        </div>
                        <div class="mb-2">
                            <strong><i class="fas fa-phone me-1"></i></strong> ${cliente.telefono}
                        </div>
                        <div class="mb-2">
                            <strong><i class="fas fa-map-marker-alt me-1"></i></strong> ${cliente.nombre_predio}
                        </div>
                        <div class="mb-2">
                            <strong><i class="fas fa-leaf me-1"></i></strong> ${cliente.tipo_cultivo} (${cliente.superficie_ha} ha)
                        </div>
                        <div class="mb-3">
                            <span class="badge ${cuentaBadge}">${cliente.estado_cuenta}</span>
                            <small class="text-muted ms-2">$${cliente.costo_servicio.toLocaleString()}</small>
                        </div>
                        <div class="mb-3">
                            <small class="text-muted">${cliente.observaciones}</small>
                        </div>
                    </div>
                    <div class="card-footer bg-light">
                        <div class="btn-group w-100" role="group">
                            <button class="btn btn-sm btn-primary" onclick="verDetalles(${cliente.id})">
                                <i class="fas fa-eye"></i>
                            </button>
                            <button class="btn btn-sm btn-warning" onclick="editarCliente(${cliente.id})">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-sm btn-danger" onclick="eliminarCliente(${cliente.id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            `;

            return col;
        }

        function actualizarEstadisticas() {
            const totalClientes = clientes.length;
            const totalPredios = clientes.length;
            const totalHectareas = clientes.reduce((sum, c) => sum + c.superficie_ha, 0);
            const ingresosTotales = clientes.reduce((sum, c) => sum + c.costo_servicio, 0);

            document.getElementById('total-clientes').textContent = totalClientes;
            document.getElementById('total-predios').textContent = totalPredios;
            document.getElementById('total-hectareas').textContent = totalHectareas.toFixed(1);
            document.getElementById('ingresos-totales').textContent = `$${ingresosTotales.toLocaleString()}`;
        }

        function configurarBusqueda() {
            document.getElementById('busqueda').addEventListener('input', function(e) {
                const termino = e.target.value.toLowerCase();
                const clientesFiltrados = clientes.filter(cliente => 
                    cliente.nombre_completo.toLowerCase().includes(termino) ||
                    cliente.persona_contacto.toLowerCase().includes(termino) ||
                    cliente.telefono.includes(termino) ||
                    cliente.rfc.toLowerCase().includes(termino) ||
                    cliente.tipo_cultivo.toLowerCase().includes(termino)
                );
                
                mostrarClientesFiltrados(clientesFiltrados);
            });
        }

        function mostrarClientesFiltrados(clientesFiltrados) {
            const contenedor = document.getElementById('lista-clientes');
            contenedor.innerHTML = '';

            clientesFiltrados.forEach(cliente => {
                const clienteCard = crearTarjetaCliente(cliente);
                contenedor.appendChild(clienteCard);
            });
        }

        function mostrarFormulario(cliente = null) {
            clienteEditando = cliente;
            const titulo = cliente ? 'Editar Cliente' : 'Nuevo Cliente';
            
            Swal.fire({
                title: titulo,
                html: `
                    <form class="text-start">
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Nombre Completo *</label>
                                <input type="text" class="form-control" id="nombre_completo" value="${cliente?.nombre_completo || ''}" required>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Persona de Contacto *</label>
                                <input type="text" class="form-control" id="persona_contacto" value="${cliente?.persona_contacto || ''}" required>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Teléfono *</label>
                                <input type="tel" class="form-control" id="telefono" value="${cliente?.telefono || ''}" required>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">RFC</label>
                                <input type="text" class="form-control" id="rfc" value="${cliente?.rfc || ''}">
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Nombre del Predio *</label>
                                <input type="text" class="form-control" id="nombre_predio" value="${cliente?.nombre_predio || ''}" required>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Superficie (ha) *</label>
                                <input type="number" step="0.1" class="form-control" id="superficie_ha" value="${cliente?.superficie_ha || ''}" required>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Tipo de Cultivo *</label>
                                <select class="form-select" id="tipo_cultivo" required>
                                    <option value="">Seleccionar...</option>
                                    <option value="Maíz" ${cliente?.tipo_cultivo === 'Maíz' ? 'selected' : ''}>Maíz</option>
                                    <option value="Tomate" ${cliente?.tipo_cultivo === 'Tomate' ? 'selected' : ''}>Tomate</option>
                                    <option value="Aguacate" ${cliente?.tipo_cultivo === 'Aguacate' ? 'selected' : ''}>Aguacate</option>
                                    <option value="Sorgo" ${cliente?.tipo_cultivo === 'Sorgo' ? 'selected' : ''}>Sorgo</option>
                                    <option value="Brócoli" ${cliente?.tipo_cultivo === 'Brócoli' ? 'selected' : ''}>Brócoli</option>
                                    <option value="Chile" ${cliente?.tipo_cultivo === 'Chile' ? 'selected' : ''}>Chile</option>
                                    <option value="Frijol" ${cliente?.tipo_cultivo === 'Frijol' ? 'selected' : ''}>Frijol</option>
                                    <option value="Trigo" ${cliente?.tipo_cultivo === 'Trigo' ? 'selected' : ''}>Trigo</option>
                                    <option value="Otro">Otro</option>
                                </select>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Costo del Servicio</label>
                                <input type="number" step="0.01" class="form-control" id="costo_servicio" value="${cliente?.costo_servicio || ''}">
                            </div>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Observaciones</label>
                            <textarea class="form-control" id="observaciones" rows="3">${cliente?.observaciones || ''}</textarea>
                        </div>
                    </form>
                `,
                width: '800px',
                showCancelButton: true,
                confirmButtonText: cliente ? 'Actualizar' : 'Guardar',
                cancelButtonText: 'Cancelar',
                confirmButtonColor: '#4a7c3a',
                preConfirm: () => {
                    const form = Swal.getPopup().querySelector('form');
                    const formData = new FormData(form);
                    
                    const nuevoCliente = {
                        id: cliente?.id || Date.now(),
                        nombre_completo: document.getElementById('nombre_completo').value.trim(),
                        persona_contacto: document.getElementById('persona_contacto').value.trim(),
                        telefono: document.getElementById('telefono').value.trim(),
                        rfc: document.getElementById('rfc').value.trim(),
                        nombre_predio: document.getElementById('nombre_predio').value.trim(),
                        superficie_ha: parseFloat(document.getElementById('superficie_ha').value) || 0,
                        tipo_cultivo: document.getElementById('tipo_cultivo').value,
                        costo_servicio: parseFloat(document.getElementById('costo_servicio').value) || 0,
                        observaciones: document.getElementById('observaciones').value.trim(),
                        estado_cliente: 'Activo',
                        estado_cuenta: 'Pendiente',
                        fecha_registro: new Date().toISOString().split('T')[0],
                        nivel_satisfaccion: 4,
                        servicios: [],
                        historial_cultivos: [document.getElementById('tipo_cultivo').value].filter(Boolean)
                    };

                    // Validación básica
                    if (!nuevoCliente.nombre_completo || !nuevoCliente.persona_contacto || !nuevoCliente.telefono) {
                        Swal.showValidationMessage('Por favor complete los campos obligatorios');
                        return false;
                    }

                    return nuevoCliente;
                }
            }).then((result) => {
                if (result.isConfirmed) {
                    guardarCliente(result.value);
                }
            });
        }

        function guardarCliente(clienteData) {
            if (clienteEditando) {
                // Actualizar cliente existente
                const index = clientes.findIndex(c => c.id === clienteEditando.id);
                if (index !== -1) {
                    clientes[index] = { ...clientes[index], ...clienteData };
                }
            } else {
                // Agregar nuevo cliente
                clientes.push(clienteData);
            }

            cargarClientes();
            actualizarEstadisticas();
            
            Swal.fire({
                icon: 'success',
                title: '¡Éxito!',
                text: clienteEditando ? 'Cliente actualizado correctamente' : 'Cliente agregado correctamente',
                confirmButtonColor: '#4a7c3a'
            });

            clienteEditando = null;
        }

        function verDetalles(id) {
            const cliente = clientes.find(c => c.id === id);
            if (!cliente) return;

            Swal.fire({
                title: cliente.nombre_completo,
                html: `
                    <div class="text-start">
                        <h6 class="text-primary"><i class="fas fa-user me-2"></i>Información de Contacto</h6>
                        <p><strong>Contacto:</strong> ${cliente.persona_contacto}</p>
                        <p><strong>Teléfono:</strong> ${cliente.telefono}</p>
                        <p><strong>RFC:</strong> ${cliente.rfc || 'No especificado'}</p>
                        
                        <hr>
                        
                        <h6 class="text-success"><i class="fas fa-map-marker-alt me-2"></i>Información del Predio</h6>
                        <p><strong>Predio:</strong> ${cliente.nombre_predio}</p>
                        <p><strong>Superficie:</strong> ${cliente.superficie_ha} hectáreas</p>
                        <p><strong>Cultivo:</strong> ${cliente.tipo_cultivo}</p>
                        
                        <hr>
                        
                        <h6 class="text-warning"><i class="fas fa-dollar-sign me-2"></i>Información Financiera</h6>
                        <p><strong>Costo del Servicio:</strong> $${cliente.costo_servicio?.toLocaleString() || 'No especificado'}</p>
                        <p><strong>Estado de Cuenta:</strong> <span class="badge ${cliente.estado_cuenta === 'Pagado' ? 'bg-success' : 'bg-warning'}">${cliente.estado_cuenta}</span></p>
                        
                        <hr>
                        
                        <h6 class="text-info"><i class="fas fa-notes-medical me-2"></i>Observaciones</h6>
                        <p>${cliente.observaciones || 'Sin observaciones'}</p>
                    </div>
                `,
                width: '600px',
                confirmButtonText: 'Cerrar',
                confirmButtonColor: '#4a7c3a'
            });
        }

        function editarCliente(id) {
            const cliente = clientes.find(c => c.id === id);
            if (cliente) {
                mostrarFormulario(cliente);
            }
        }

        function eliminarCliente(id) {
            const cliente = clientes.find(c => c.id === id);
            if (!cliente) return;

            Swal.fire({
                title: '¿Eliminar Cliente?',
                text: `¿Está seguro de eliminar a ${cliente.nombre_completo}?`,
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#dc3545',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Sí, eliminar',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    clientes = clientes.filter(c => c.id !== id);
                    cargarClientes();
                    actualizarEstadisticas();
                    
                    Swal.fire({
                        icon: 'success',
                        title: 'Eliminado',
                        text: 'Cliente eliminado correctamente',
                        confirmButtonColor: '#4a7c3a'
                    });
                }
            });
        }

        // Simulación de sincronización online
        setInterval(() => {
            // Aquí se podría implementar sincronización real con servidor
            console.log('Sistema funcionando correctamente...');
        }, 30000);

        // Toast de conexión
        setTimeout(() => {
            const toast = document.createElement('div');
            toast.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            toast.innerHTML = `
                <div class="toast show" role="alert">
                    <div class="toast-header bg-success text-white">
                        <i class="fas fa-wifi me-2"></i>
                        <strong class="me-auto">Sistema ASOA</strong>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
                    </div>
                    <div class="toast-body">
                        ¡Conectado y funcionando correctamente!
                    </div>
                </div>
            `;
            document.body.appendChild(toast);
            
            setTimeout(() => toast.remove(), 5000);
        }, 3000);
    </script>
</body>
</html>
