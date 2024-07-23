# FastAPI REST API Tutorial

Este repositorio contiene un ejemplo de cómo construir una API REST utilizando FastAPI. El tutorial cubre desde la configuración básica del proyecto hasta la implementación de pruebas unitarias y la configuración de Docker para el despliegue y la depuración.

## Estructura del Proyecto
```plaintext

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
```

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

### Debugging con Docker Compose y Visual Studio Code

Para depurar la aplicación FastAPI utilizando Docker Compose y Visual Studio Code, sigue estos pasos:

1. **Ejecutar Docker Compose**:
   Navega a la raíz de tu proyecto y ejecuta el siguiente comando para construir y ejecutar los contenedores:
   ```sh
   docker-compose up --build
2. **Adjuntar el Depurador**:
- Abre Visual Studio Code.
- Ve a la pestaña de depuración.
- Selecciona la configuración QA API (Remote Attach).
- Presiona F5 para iniciar el depurador.

Esta configuración instalará debugpy, iniciará el servidor de desarrollo y esperará a que el depurador se adjunte en el puerto 5678.

Con esta configuración, puedes depurar tu aplicación FastAPI dentro de un contenedor Docker utilizando Visual Studio Code.