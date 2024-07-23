# FastAPI REST API Tutorial

Este repositorio contiene un ejemplo de cómo construir una API REST utilizando FastAPI. El tutorial cubre desde la configuración básica del proyecto hasta la implementación de pruebas unitarias y la configuración de Docker para el despliegue y la depuración.

## Estructura del Proyecto
fastapi-rest-api-tutorial/
│
├── qa_api/
│ ├── init.py
│ ├── main.py
│ ├── models.py
│ └── routes.py
├── tests/
│ ├── init.py
│ └── test_main.py
├── .vscode/
│ ├── launch.json
│ └── tasks.json
├── .gitignore
├── Dockerfile
├── LICENSE
├── README.md
└── requirements.txt

## Archivos Clave

### main.py

Este archivo contiene la configuración principal de la aplicación FastAPI, incluyendo la configuración del logger y la inclusión de las rutas.

### models.py
Este archivo contiene los modelos utilizados en la API, tanto los DTOs como las entidades de dominio.

### routes.py
Este archivo contiene las rutas de la API y la lógica para manejar las operaciones CRUD.

### test_main.py
Este archivo contiene las pruebas unitarias para los endpoints de la API.

# Ejecución y Depuración
## Localmente
Para ejecutar la aplicación localmente, selecciona la configuración QA API (Local) en Visual Studio Code y presiona F5.

## En Docker
Para ejecutar la aplicación en Docker, selecciona la configuración QA API (Docker) en Visual Studio Code y presiona F5. Esto construirá y ejecutará el contenedor Docker y adjuntará el depurador.

## Ejecutar Pruebas
Para ejecutar las pruebas, selecciona la configuración pytest QA API en Visual Studio Code y presiona F5.