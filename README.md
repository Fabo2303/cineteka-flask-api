# Cineteka API - Agregador de Información de Cines

Este proyecto fue desarrollado como una solución moderna para obtener información actualizada de las principales cadenas de cines en Perú. La API utiliza técnicas de web scraping para recopilar datos de películas y horarios, proporcionando una interfaz unificada para acceder a esta información.

## Índice

1. [Características principales](#características-principales)
2. [Tecnologías utilizadas](#tecnologías-utilizadas)
3. [Prerrequisitos](#prerrequisitos)
4. [Instrucciones de uso](#instrucciones-de-uso)
   - [Paso 1: Clonar el repositorio](#paso-1-clonar-el-repositorio)
   - [Paso 2: Configurar el entorno](#paso-2-configurar-el-entorno)
   - [Paso 3: Instalar dependencias](#paso-3-instalar-dependencias)
   - [Paso 4: Ejecutar la aplicación](#paso-4-ejecutar-la-aplicación)
   - [Paso 5: Usar la API](#paso-5-usar-la-api)
5. [Endpoints de la API](#endpoints-de-la-api)
6. [Estructura del Proyecto](#estructura-del-proyecto)
7. [Consideraciones](#consideraciones)

## Características principales

- Scraping en tiempo real de múltiples cadenas de cines
- Normalización de datos para formato consistente
- Soporte para Docker
- API RESTful con endpoints unificados
- CORS habilitado para integración con frontends

## Tecnologías utilizadas

- **Backend Framework:** Flask (Python)
- **Web Scraping:** Playwright
- **Contenedorización:** Docker
- **Gestión de dependencias:** pip

## Prerrequisitos

- Python 3.x
- pip (gestor de paquetes de Python)
- Docker (opcional, para contenedorización)
- Navegador Chromium (instalado automáticamente por Playwright)

## Instrucciones de uso

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/Fabo2303/cineteka-flask-api.git
cd cineteka-flask-api
```

### Paso 2: Configurar el entorno
Crear un archivo `.env` con las siguientes variables:
```env
P=NOMBRE_DEL_CINE_P
M=NOMBRE_DEL_CINE_M
M_URL=LINK_DEL_CINE_M
P_URL=LINK_DEL_CINE_P
```

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
playwright install chromium
```

### Paso 4: Ejecutar la aplicación
```bash
python app.py
```

### Paso 5: Usar la API
La API estará disponible en `http://localhost:5000`

## Endpoints de la API

### GET /peliculas
Obtiene la lista de todas las películas en cartelera.

**Respuesta:**
```json
{
    "message": "Scraping completado.",
    "peliculas": [
        {
            "titulo": "Título de la película",
            "link": "URL de detalle",
            "imagen": "URL del póster",
            "type": "Identificador de cine"
        }
    ]
}
```

### GET /horarios
Obtiene los horarios de una película específica.

**Parámetros:**
- `type`: Identificador de la cadena de cine
- `url`: URL de la película

**Respuesta:**
```json
{
    "message": "Scraping completado.",
    "horarios": [
        {
            "sede": "Nombre de sede",
            "formato": "Formato de proyección",
            "tipo_sala": "Tipo de sala",
            "idioma": "Idioma de proyección",
            "horarios": ["14:30", "17:00", "19:30"]
        }
    ]
}
```

## Estructura del Proyecto
```
cineteka-flask-api/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias del proyecto
├── Dockerfile            # Configuración de Docker
├── scrapers/            
│   ├── m/               # Scraper primera cadena
│   │   ├── moviesscraper.py
│   │   └── schedulescraper.py
│   └── p/               # Scraper segunda cadena
│       ├── moviesscraper.py
│       └── schedulescraper.py
└── utils/
    └── formatter.py     # Utilidades de formateo
```

## Consideraciones

- La API utiliza web scraping, por lo que depende de la estructura HTML de los sitios objetivo
- Las respuestas pueden variar en tiempo según la velocidad de conexión
- Se debe respetar los términos de uso de los sitios objetivo
- Los identificadores de cines se manejan mediante variables de entorno por seguridad